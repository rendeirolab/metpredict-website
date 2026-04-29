#!/usr/bin/env python3

import argparse
from pathlib import Path
import shutil

import yaml
from jinja2 import Environment, FileSystemLoader


def load_config():
    return yaml.safe_load(Path("config.yaml").open().read())


def build(config=None):
    if config is None:
        config = load_config()
    template_dir = Path(config["template_dir"])
    content_dir = Path(config["content_dir"])
    build_dir = Path(config["build_dir"])
    build_dir.mkdir(exist_ok=True, parents=True)

    build_index(config, template_dir, content_dir, build_dir)
    copy_assets(build_dir)
    print("Build complete.")


def build_index(config, template_dir, content_dir, build_dir):
    environment = Environment(loader=FileSystemLoader(template_dir))

    content_file = content_dir / "index.yaml"
    content = yaml.safe_load(content_file.open().read())["index"]

    page_file = build_dir / config["pages"]["index"]["file"]
    page_file.parent.mkdir(exist_ok=True, parents=True)

    page_template = environment.from_string(
        (template_dir / config["pages"]["index"]["template"]).open().read()
    )

    html = page_template.render(
        page_url=config["deploy_url"] + config["pages"]["index"]["url"],
        **config,
        **content,
    )

    with page_file.open("w") as f:
        f.write(html)


def copy_assets(build_dir):
    if (build_dir / "assets").exists():
        shutil.rmtree(build_dir / "assets")
    shutil.copytree("assets", build_dir / "assets")


def serve():
    from livereload import Server

    config = load_config()
    build(config)

    build_dir = config["build_dir"]
    server = Server()

    # Watch templates, content, assets, config — rebuild on any change
    server.watch("templates/", lambda: build())
    server.watch("content/", lambda: build())
    server.watch("assets/", lambda: build())
    server.watch("config.yaml", lambda: build())

    print(f"Dev server at http://localhost:8000 — watching for changes...")
    server.serve(root=build_dir, port=8000, open_url_delay=1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true", help="Start dev server with live reload")
    args = parser.parse_args()

    if args.serve:
        serve()
    else:
        build()