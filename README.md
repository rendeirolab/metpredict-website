# MetPredict Website

Static website for the [MetPredict project](https://metpredict.at/) — a WWTF-funded collaboration on prediction of metastatic potential.

Live at **[metpredict.at](https://metpredict.at/)**.

## Development

```bash
uv sync
uv run task serve     # dev server with live reload
uv run task build     # build static site to docs/
```

Content is managed via YAML files in `content/`. Templates use Jinja2.

## Deploying

Push to `main`. GitHub Pages serves from `docs/`.