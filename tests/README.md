# Publication checks

Run `python3 -m unittest discover -s tests -v` from the repository root after building the publication. The tests check bound SQLite values, escaped metadata, local release links and source mappings, and generated secret-pattern fixtures. They do not perform an external security assessment or guarantee that every possible secret format is detected.
