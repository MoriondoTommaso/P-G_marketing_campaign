"""Unpack the corrected release and point its two folder variables at local paths."""
from hashlib import sha256
from pathlib import Path
import sys
from zipfile import ZipFile
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def prepare(run):
    release = ROOT / "workflows/oral-b-italy.knwf"
    out = HERE / "local" / run
    out.mkdir(parents=True, exist_ok=False)
    results = out / "outputs"
    results.mkdir()
    with ZipFile(release) as z:
        z.extractall(out)
    digest = sha256(release.read_bytes()).hexdigest()
    (out / "release.sha256").write_text(f"{digest}  workflows/oral-b-italy.knwf\n")
    print("archive_sha256:", digest)
    source = out / "oral-b-italy"
    for i, dest in [(34, ROOT / "data"), (35, results)]:
        settings, = source.glob(f"*(#{i})/settings.xml")
        tree = ET.parse(settings)
        path, = [e for e in tree.iter() if e.get("key")=="path" and e.get("value","").startswith("/")]
        original = path.get("value")
        raw = settings.read_bytes()
        assert raw.count(original.encode()) == 1
        settings.write_bytes(raw.replace(original.encode(),escape(str(dest),{'"':"&quot;"}).encode()))
    print(source)


if __name__ == "__main__":
    prepare(sys.argv[1])
