# Publishing and maintaining the series

## First publication

Use the README’s GitHub setup instructions. Publish the `docs/` artifact. Do not publish the repository root as a web artifact.

The Pages workflow runs on pull requests, pushes to main, and manual dispatches. Pull requests build and validate; only main can reach the deployment job. The build job has `contents: read`; the separate deployment job has `pages: write` and `id-token: write`. It uses the `github-pages` environment.

Action versions follow the major release tags documented by GitHub at creation time. Dependabot checks Actions weekly. For stricter dependency control, replace the action tags with independently verified full commit SHAs and keep them updated.

## Update a page

1. Edit the source fragment and metadata.
2. Preserve the slug if you want existing links to keep working.
3. Build and run the checks in README.
4. Review the diff, including generated downloads and search data.
5. Commit and push. The workflow rebuilds the artifact.

Source fragments are trusted HTML. Metadata is escaped. Content, citations, navigation, and the table of contents are generated before publication. The browser uses no Markdown renderer or external CDN.

## Change the repository name

Links and asset paths are relative, so project paths do not need a base-URL edit. Update the README’s example remote and expected URL. Custom domains may be configured later through GitHub Pages; no CNAME or domain ownership is assumed.

## Troubleshooting

- **Pages not enabled:** choose GitHub Actions in Settings → Pages, then rerun the workflow.
- **Repository plan or organization policy blocks Pages:** check your account/organization’s Pages availability and Actions permissions.
- **Blank site:** inspect the build/deploy jobs and ensure `docs/index.html` is in the uploaded artifact.
- **Old article on a branch deployment:** rebuild and commit `docs/` before pushing.
- **Search returns nothing:** clear both the query and subject filter. Search covers full article text; filters combine with the query.
- **Clipboard unavailable in a file preview:** use the selected text fallback and your keyboard to copy.

Local link validation covers generated HTML references and fragments. It does not assert that external reference sites are continuously available. GitHub Actions and remote publication still require execution in the target account.
