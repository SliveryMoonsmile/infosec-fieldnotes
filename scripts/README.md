# Publication commands

From the repository root, run `python3 scripts/build.py` to regenerate the static publication in `docs/`. Run `python3 -m unittest discover -s tests -v` to check local links, source mappings, escaped metadata, recognizable secret patterns, and the local SQLite example. Check browser-script syntax with `node --check assets/site.js`. The Python tools use the standard library and require Python 3.12 or newer.
