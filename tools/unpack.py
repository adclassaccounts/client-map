#!/usr/bin/env python3
"""Extract editable JS modules from the bundled HTML into ./src/.

Run this once before making changes. Edit files in src/ with a normal editor
(or ask Claude Code to edit them), then run tools/repack.py to fold them
back into Territory_Dashboard__Standalone_.html.
"""
import base64, gzip, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "Territory_Dashboard__Standalone_.html")
SRC  = os.path.join(ROOT, "src")

# Only these UUIDs are user-editable application code. Everything else in
# the manifest (fonts, topojson, React/d3/Babel) is a vendor blob — don't
# touch it.
EDITABLE = {
    "06cbdab3-8eda-44d8-9eef-eca1f6cca15d": ("data.js",         "Reference data + Go High Level fetch helpers"),
    "b299a0ac-4cdc-4de2-bd07-e33d2cf7599a": ("NationalMap.js",  "US-wide map (pins, radar sweep, connections)"),
    "a47bf331-faac-45f1-ac78-a23404a75e1c": ("StateZoomMap.js", "Drill-down state view with counties"),
    "4ef3f597-be9d-4680-846f-a987530dfb89": ("Sidebar.js",      "StatTile, CompanyCard, AddForm"),
    "ddaa0900-473e-47f2-9a3c-17d0772d9d35": ("App.js",          "Top-level App shell (header, layout, settings)"),
}

def main():
    with open(HTML, "r", encoding="utf-8") as f:
        html = f.read()
    m = re.search(r'<script type="__bundler/manifest">(.*?)</script>', html, re.DOTALL)
    if not m:
        sys.exit("Could not find bundler manifest in HTML.")
    manifest = json.loads(m.group(1))

    os.makedirs(SRC, exist_ok=True)
    index_lines = ["# Editable source files", ""]
    for uuid, (name, desc) in EDITABLE.items():
        if uuid not in manifest:
            print(f"!! {uuid} not in manifest — skipping")
            continue
        entry = manifest[uuid]
        raw = base64.b64decode(entry["data"])
        if entry.get("compressed"):
            raw = gzip.decompress(raw)
        out = os.path.join(SRC, name)
        with open(out, "wb") as o:
            o.write(raw)
        print(f"  ↪ {name:18s}  ({len(raw):>6d} bytes)  {desc}")
        index_lines.append(f"- `{name}` — {desc}")

    # Map of filename → uuid so repack knows where each file goes back.
    map_path = os.path.join(SRC, ".bundle-map.json")
    with open(map_path, "w") as o:
        json.dump({name: uuid for uuid, (name, _) in EDITABLE.items()}, o, indent=2)
    print(f"\nUnpacked {len(EDITABLE)} files into {SRC}/")
    print("Edit any of them, then run:  python3 tools/repack.py")

if __name__ == "__main__":
    main()
