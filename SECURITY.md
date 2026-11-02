# Security and publication boundaries

This repository contains a static educational publication. It has no server, account system, analytics, or runtime Notion/AWS credentials. Browser scripts do not make remote data requests. The theme preference is saved only in the visitor’s local browser storage.

Report a publication defect through a repository issue after the GitHub repository is created. Do not include credentials, personal information, or private captures in an issue. For a sensitive issue, use GitHub’s private vulnerability reporting if enabled by the repository owner.

Before publication, review article fragments, metadata, examples, search indexes, downloads, and the Git diff. `scripts/check.py` checks a few recognizable secret patterns; it is not an exhaustive secret detector or a security audit. A credential exposed anywhere should be revoked or rotated and its use investigated.

The HTML Content Security Policy restricts script/style/image sources and disallows data connections, objects, base changes, and form submission. GitHub Pages controls HTTP headers; this meta policy does not provide header-only controls such as frame-ancestors. It is defense in depth, not a substitute for reviewed content. The builder accepts trusted authored HTML fragments and does not sanitize an untrusted Notion export.

Use exercises on owned or explicitly authorized systems. The included runnable lab is local, in memory, and requires no network access. Fictional policy examples and templates do not describe an assessed production environment.
