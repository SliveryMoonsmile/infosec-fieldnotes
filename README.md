# Information Security Fieldnotes

An eight-part information security publication adapted from Syed Hussain’s technical Notion journal. Includes a responsive website, source provenance, local examples, and a GitHub Pages workflow.

**Repository:** [SliveryMoonsmile/infosec-fieldnotes](https://github.com/SliveryMoonsmile/infosec-fieldnotes). This publication uses the included GitHub Actions workflow to build, validate, and deploy to GitHub Pages.

To update this repository, clone it, edit the article sources, and push to `main`. The first-publication instructions below also support publishing your own copy.

## Read locally

Open `docs/index.html`, or serve the publication:

```bash
python3 scripts/build.py
python3 -m http.server 8080 --directory docs --bind 127.0.0.1
```

Visit `http://127.0.0.1:8080`. All article text and navigation work without JavaScript. Search, subject filters, a light theme, code copying, and mobile navigation enhance the pages. The site uses relative links and works under a GitHub project path such as `/infosec-fieldnotes/`.

## The series

| Note | Subject | Page |
| --- | --- | --- |
| 01 | Threat modeling and incident reasoning | [Think in threats. Work in evidence.](docs/articles/threats-and-response.html) |
| 02 | SQL injection, XSS, and CSRF | [Three ways the web loses trust.](docs/articles/web-trust-boundaries.html) |
| 03 | Packets, ARP, DNSSEC, and VPNs | [Follow the packet.](docs/articles/packets-and-protocols.html) |
| 04 | Authorization and Kerberos | [Identity is the beginning of access.](docs/articles/identity-and-authorization.html) |
| 05 | Linux and tmux | [Make the lab reproducible.](docs/articles/linux-lab-notebook.html) |
| 06 | Vulnerability triage and memory safety | [A finding is a hypothesis.](docs/articles/vulnerability-analysis.html) |
| 07 | Cloud identity and delivery | [Ship less privilege.](docs/articles/cloud-and-delivery.html) |
| 08 | Research and technical writing | [Turn reading into evidence.](docs/articles/research-to-evidence.html) |

## Publish to GitHub Pages

1. Create an **empty** GitHub repository named `infosec-fieldnotes`. A public repository supports Pages on GitHub Free; private repository support depends on your plan.
2. From the extracted `infosec-fieldnotes` directory, run the commands below. Replace `YOUR_USERNAME` with the real account name.

```bash
git init -b main
git add .
git commit -m "Create information security fieldnotes publication"
git remote add origin https://github.com/YOUR_USERNAME/infosec-fieldnotes.git
git push -u origin main
```

3. In the repository, open **Settings → Pages → Build and deployment → Source**, and choose **GitHub Actions**.
4. In **Actions → Publish fieldnotes**, choose **Run workflow** on `main` if the first workflow ran before Pages was enabled.
5. Open the URL shown by the deployment. The normal project address is `https://YOUR_USERNAME.github.io/infosec-fieldnotes/`.

If Git asks for credentials, use GitHub’s supported Git credential manager or authenticated GitHub CLI. Do not put a token in a repository file or remote URL.

An alternative is **Deploy from a branch → main → /docs**. The generated pages are committed for this option. If you choose it, disable or remove `.github/workflows/pages.yml` to avoid maintaining two publication methods, and rebuild/commit `docs/` whenever content changes.

Current GitHub references: [custom Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages), [publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Edit or add an article

- Edit metadata and reference URLs in `content/articles.json`.
- Edit each article’s readable HTML fragment in `content/<slug>.html`.
- Add `<h2 id="a-unique-anchor">` headings for automatic table-of-contents links.
- The HTML fragments are trusted editorial source. Review any copied markup; the builder does not sanitize arbitrary HTML from outside sources.
- Update `content/source-map.json` when an article uses a new notebook source.
- Rebuild and validate:

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests -v
node --check assets/site.js
```

The builder requires Python 3.12 or newer. There are no pip or npm packages to install. Node is needed only for the JavaScript syntax check; it is available on GitHub-hosted Ubuntu runners.

## Repository layout

```text
content/                 Curated article HTML, metadata, source map
assets/                  Local styles, scripts, favicon
labs/                    Runnable SQLite example and editable templates
scripts/build.py         Standard-library static builder
scripts/check.py         Local link/fragment, metadata, and secret-pattern checks
tests/                   Publication and SQLite behavior checks
docs/                    Complete prebuilt GitHub Pages output
.github/workflows/       CI and Pages publication
PUBLISHING.md            Deployment and maintenance notes
SECURITY.md              Reporting and publication boundaries
```

## Provenance and limits

The Infosec view contained 32 entries; 23 relevant records were inspected for this series. The source map records treatment per record. Blank and image-only entries do not supply factual claims; the Application Hacking title supplies only a theme. Personal remarks and exam scores were omitted. Credential material was excluded entirely. Original screenshots were not redistributed or transcribed.

Technical explanations were rewritten and checked against primary references on 30 October 2026. Examples are fictional or proposed exercises, not claimed work history. This is a static snapshot, not an automatic Notion sync. Original source links may require Notion access.

The pattern scanner is a limited guardrail. It does not prove that source files contain no sensitive data, and it does not replace review. No license has been selected for the repository; choose one before inviting reuse.
