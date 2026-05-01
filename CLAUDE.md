# Project: Territory Dashboard

This repo contains a single self-contained HTML dashboard:
`Territory_Dashboard__Standalone_.html`. It's a React app whose source
code is gzipped + base64 encoded inside `<script type="__bundler/manifest">`
tags in that HTML file. **Do not try to edit the HTML file directly** —
search/replace will not find application code there.

## Editing workflow (every change uses this loop)

1. Run `python3 tools/unpack.py` to extract editable modules into `src/`.
2. Edit files in `src/`. Only these five are user code:
   - `src/data.js` — reference data, Go High Level (GHL) API integration,
     normalization helpers.
   - `src/App.js` — top-level shell, header, layout, settings modal.
   - `src/Sidebar.js` — `StatTile`, `CompanyCard`, `AddForm`.
   - `src/NationalMap.js` — US-wide map with radar sweep + pins.
   - `src/StateZoomMap.js` — drill-down state view with counties.
3. Run `python3 tools/repack.py` to fold the edits back into the HTML.
4. Open `Territory_Dashboard__Standalone_.html` in a browser to verify.
5. Commit the HTML file (the `src/` directory is gitignored — it is
   regeneratable from the HTML and not the source of truth).

## Important rules

- The five files above are JSX with React/D3 globals available; they're
  evaluated by Babel-standalone in the browser. Use `React.useState`
  patterns already in the file. Don't introduce ES modules / `import`.
- The other manifest entries (UUIDs not listed in `tools/unpack.py`) are
  vendor blobs — fonts, US topojson, React/D3/Babel runtimes. Do not
  unpack or edit those.
- Always run `python3 tools/repack.py` before committing. The `src/`
  directory is **not** committed; the HTML is the artifact.
- Never commit API keys. The GHL key is supplied at runtime via the in-app
  settings modal and stored in the user's localStorage.

## Quick preview

```
python3 -m http.server 8000
# open http://localhost:8000/Territory_Dashboard__Standalone_.html
```

## Common edits and where they live

| Want to change…                                    | File             |
|----------------------------------------------------|------------------|
| Header text, layout, stat tiles                    | `App.js`         |
| GHL endpoint, status filter, field mapping         | `data.js`        |
| Settings modal fields                              | `App.js`         |
| Add-record form fields                             | `Sidebar.js`     |
| Pin styling, radar animation, connection lines     | `NationalMap.js` |
| State zoom, county painting                        | `StateZoomMap.js`|
| Category colors, default categories                | `data.js`        |
