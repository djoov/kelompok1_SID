"""SDI classroom lab: local blue-green deployment. Python 3.10+, stdlib only."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import zipfile

ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / 'artifacts'
STATE = ROOT / 'runtime'
PORTS = {'blue': 8101, 'green': 8102, 'public': 8100}


def write_json(path, value):
    path.parent.mkdir(exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, indent=2), encoding='utf-8')
    temp.replace(path)


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def prepare():
    ARTIFACTS.mkdir(exist_ok=True)
    for version in ['1.0.0', '1.1.0']:
        source = '''def biaya(amount):
    if type(amount) is not int or amount < 0:
        raise ValueError("amount harus integer nonnegatif")
    return min(amount // 100, 5000)
'''
        if version == '1.1.0':
            source += '\ndef currency():\n    return "IDR"\n'
        payload = io.BytesIO()
        with zipfile.ZipFile(payload, 'w', zipfile.ZIP_DEFLATED) as z:
            for name, text in {
                'app.py': source,
                'VERSION': version + '\n',
                'manifest.json': json.dumps({
                    'version': version,
                    'source_sha256': hashlib.sha256(source.encode()).hexdigest(),
                    'build_run': 'classroom-prebuilt',
                    'note': 'Local package; no GitHub CI run claimed',
                }, indent=2),
            }.items():
                info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, text)
        data = payload.getvalue()
        path = ARTIFACTS / ('sdi-' + version + '.zip')
        if path.exists():
            if path.read_bytes() != data:
                raise ValueError('Existing artifact differs; restore starter in new folder')
        else:
            path.write_bytes(data)
        digest = hashlib.sha256(data).hexdigest()
        path.with_suffix('.zip.sha256').write_text(digest + '  ' + path.name + '\n')
        print(path.name, digest)


def load_package(path):
    data = path.read_bytes()
    expected = path.with_suffix('.zip.sha256').read_text().split()[0]
    digest = hashlib.sha256(data).hexdigest()
    if digest != expected:
        raise ValueError('Artifact checksum mismatch: ' + path.name)
    # Execute only classroom-owned source. This is not a sandbox for untrusted ZIPs.
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        source = z.read('app.py')
        manifest = json.loads(z.read('manifest.json'))
    if hashlib.sha256(source).hexdigest() != manifest['source_sha256']:
        raise ValueError('Source hash mismatch')
    namespace = {}
    exec(compile(source, str(path) + '/app.py', 'exec'), namespace)
    return namespace, manifest, digest


def request_json(target, path):
    url = 'http://127.0.0.1:' + str(PORTS[target]) + path
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as exc:
        return exc.code, json.load(exc)


def check(target, verbose=True):
    failures = 0
    for amount, expected in [(0, 0), (100000, 1000), (1000000, 5000), (-1, None)]:
        status, body = request_json(target, '/quote?amount=' + str(amount))
        ok = (status == 400 if expected is None else
              status == 200 and body.get('fee') == expected)
        failures += int(not ok)
        if verbose:
            print('PASS' if ok else 'FAIL', 'amount=', amount,
                  'expected=', expected, 'status=', status, 'fee=', body.get('fee'),
                  'slot=', body.get('slot'))
    if verbose:
        print('GATE:', 'PASS' if failures == 0 else 'FAIL')
    return failures == 0


def handler_for(slot, package=None):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def send_json(self, status, body):
            data = json.dumps(body).encode()
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if slot == 'router':
                selected = read_json(STATE / 'route.json')['active']
                try:
                    status, body = request_json(selected, self.path)
                    self.send_json(status, body)
                except (OSError, ValueError):
                    self.send_json(502, {'error': 'backend unavailable', 'slot': selected})
                return
            config = read_json(STATE / (slot + '.json'))
            functions, manifest, digest = package
            base = {'slot': slot, 'version': manifest['version'],
                    'artifact_sha256': digest, 'environment': config['environment'],
                    'config_revision': config['revision']}
            url = urllib.parse.urlparse(self.path)
            if url.path == '/health':
                self.send_json(200, {**base, 'status': 'up'})
                return
            if url.path != '/quote':
                self.send_json(404, {**base, 'error': 'not found'})
                return
            try:
                amount = int(urllib.parse.parse_qs(url.query)['amount'][0])
                fee = functions['biaya'](amount)
            except (KeyError, ValueError, IndexError):
                self.send_json(400, {**base, 'error': 'invalid amount'})
                return
            # Simulates a faulty external/config-driven override AFTER correct app logic.
            if config['fault'] and amount == 100000:
                fee = 5000
            body = {**base, 'amount': amount, 'fee': fee}
            if 'currency' in functions:
                body['currency'] = functions['currency']()
            self.send_json(200, body)
    return Handler


def run():
    if not (ARTIFACTS / 'sdi-1.0.0.zip').exists():
        raise ValueError('Run prepare first')
    STATE.mkdir(exist_ok=True)
    write_json(STATE / 'route.json', {'active': 'blue'})
    for slot, version, environment in [('blue', '1.0.0', 'production'),
                                       ('green', '1.1.0', 'staging')]:
        write_json(STATE / (slot + '.json'),
                   {'environment': environment, 'revision': 1, 'fault': False})
    servers = []
    try:
        for slot, version in [('blue', '1.0.0'), ('green', '1.1.0')]:
            package = load_package(ARTIFACTS / ('sdi-' + version + '.zip'))
            server = ThreadingHTTPServer(('127.0.0.1', PORTS[slot]), handler_for(slot, package))
            servers.append(server)
        servers.append(ThreadingHTTPServer(('127.0.0.1', PORTS['public']), handler_for('router')))
        for server in servers:
            threading.Thread(target=server.serve_forever, daemon=True).start()
        print('RUNNING: blue 8101, green 8102, public 8100. Stop: Ctrl+C', flush=True)
        while True:
            time.sleep(.2)
    except KeyboardInterrupt:
        print('Stopped')
    finally:
        for server in servers:
            server.server_close()


def switch(target, approved):
    if not approved:
        raise ValueError('Human approval missing: use --approve after reviewing evidence')
    if not check(target):
        raise ValueError('Switch rejected: business gate failed')
    config = read_json(STATE / (target + '.json'))
    config['environment'] = 'production'
    config['revision'] += 1
    write_json(STATE / (target + '.json'), config)
    write_json(STATE / 'route.json', {'active': target})
    print('TRAFFIC ->', target)
    print('Post-switch validation:')
    if not check('public'):
        raise ValueError('Post-switch gate failed: investigate and recover')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('prepare')
    sub.add_parser('run')
    for action in ['check', 'health', 'measure']:
        command = sub.add_parser(action)
        command.add_argument('--target', choices=PORTS, default='public')
    command = sub.add_parser('switch')
    command.add_argument('target', choices=['blue', 'green'])
    command.add_argument('--approve', action='store_true')
    command = sub.add_parser('fault')
    command.add_argument('mode', choices=['on', 'off'])
    args = parser.parse_args()
    try:
        if args.command == 'prepare':
            prepare()
        elif args.command == 'run':
            run()
        elif args.command == 'check':
            if not check(args.target):
                raise SystemExit(1)
        elif args.command == 'health':
            status, body = request_json(args.target, '/health')
            print(status, json.dumps(body, indent=2))
        elif args.command == 'switch':
            switch(args.target, args.approve)
        elif args.command == 'fault':
            config = read_json(STATE / 'green.json')
            config['fault'] = args.mode == 'on'
            config['revision'] += 1
            write_json(STATE / 'green.json', config)
            print('Green runtime fault:', args.mode, '(artifact unchanged)')
        elif args.command == 'measure':
            failure = 0
            values = [0, 100000, 1000000, 100000, 0, 1000000, 100000, 0, 1000000, 0]
            for amount in values:
                status, body = request_json(args.target, '/quote?amount=' + str(amount))
                failure += int(status != 200 or body.get('fee') != min(amount // 100, 5000))
            print('Business failures:', failure, '/ 10 =', failure * 10, '%')
            print('Evidence: fee correctness, not HTTP status alone')
    except (OSError, ValueError, KeyError) as exc:
        print('ERROR:', exc)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
