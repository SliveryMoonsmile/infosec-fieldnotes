# Validation record

Prepared 30 October 2026.

- Built 8 articles and 5 overview/resource pages with Python 3.12.
- Four unittest checks passed: parameter binding behavior, escaped metadata, generated release links/provenance, and generated secret-detector fixtures.
- All local HTML links and fragment targets resolved; project Pages paths use relative URLs.
- JavaScript syntax check passed with Node 24.
- The standalone local SQLite lab passed.
- Browser review: homepage layout, article layout, light/dark theme toggle, full-text search for Kerberos, combined topic filtering, empty-result state, and code-copy selection fallback.
- Original private screenshots were not transcribed or republished. Raw notebook content and credential values were not written to the repository.

The browser review used a desktop viewport. Responsive breakpoints are implemented; a separate mobile viewport was not exercised. The secret-pattern check detects only its documented formats. External links were used for reference verification during preparation; continuous external-link monitoring is not included.

The public repository was created on 2 November 2026 with GitHub Actions configured as the Pages publishing source. This record describes local validation; hosted build and deployment results are recorded in the repository's Publish fieldnotes workflow runs.
