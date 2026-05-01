#!/usr/bin/env python3
"""Fold edited modules in ./src/ back into Territory_Dashboard__Standalone_.html.

Run this after editing any file in src/. The script gzips + base64-encodes
each module and replaces the matching entry in the bundler manifest. The
rest of the HTML is left byte-identical.
"""
import base64, gzip, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "Territory_Dashboard__Standalone_.html")
SRC  = os.path.join(ROOT, "src")
MAP  = os.path.join(SRC, ".bundle-map.json")

def main():
    if not os.path.exists(MAP):
        sys.exit("src/.bundle-map.json missing — run tools/unpack.py first.")
    with open(MAP) as f:
        bundle_map = json.load(f)

    with open(HTML, "r", encoding="utf-8") as f:
        html = f.read()
    m = re.search(r'(<script type="__bundler/manifest">)(.*?)(</script>)', html, re.DOTALL)
    if not m:
        sys.exit("Could not find bundler manifest in HTML.")
    manifest = json.loads(m.group(2))

    changed = 0
    for name, uuid in bundle_map.items():
        path = os.path.join(SRC, name)
        if not os.path.exists(path):
            print(f"!! {name} missing — skipping")
            continue
        with open(path, "rb") as f:
            raw = f.read()
        gz  = gzip.compress(raw, compresslevel=9, mtime=0)
        b64 = base64.b64encode(gz).decode("ascii")
        if manifest[uuid].get("data") == b64:
            continue  # no change
        manifest[uuid]["data"] = b64
        manifest[uuid]["compressed"] = True
        print(f"  ↪ {name:18s}  raw={len(raw)} gz={len(gz)}")
        changed += 1

    if not changed:
        print("No changes detected.")
        return

    new_manifest = json.dumps(manifest, separators=(",", ":"))
    new_html = html[:m.start(2)] + new_manifest + html[m.end(2):]
    with open(HTML, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"\nRepacked {changed} file(s) into Territory_Dashboard__Standalone_.html")
    print("Refresh the browser to see your changes.")

if __name__ == "__main__":
    main()
