import hashlib
import json
import os
from pathlib import Path
import zipfile

version = Path("VERSION").read_text().strip()
commit = os.getenv("GITHUB_SHA", "local")
run = os.getenv("GITHUB_RUN_ID", "local")

out = Path("dist")
out.mkdir(exist_ok=True)
name = f"sdi-{version}-{commit[:12]}-{run}.zip"
manifest = {"version": version, "commit": commit, "build_run": run}

with zipfile.ZipFile(out / name, "w", zipfile.ZIP_DEFLATED) as z:
    z.write("app.py")
    z.write("VERSION")
    z.writestr("manifest.json", json.dumps(manifest, indent=2))

digest = hashlib.sha256((out / name).read_bytes()).hexdigest()
(out / f"{name}.sha256").write_text(f"{digest}  {name}\n")
print(name)
print(digest)
