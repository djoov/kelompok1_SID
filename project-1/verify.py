# Simpan sebagai verify.py di folder berisi ZIP kandidat dan .sha256
import hashlib
from pathlib import Path

for archive in Path(".").glob("sdi-*.zip"):
    expected = Path(str(archive) + ".sha256").read_text().split()[0]
    actual = hashlib.sha256(archive.read_bytes()).hexdigest()
    print(archive.name, "MATCH" if expected == actual else "MISMATCH")
