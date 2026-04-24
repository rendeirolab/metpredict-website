#!/usr/bin/env python3

from pathlib import Path
import shutil

import yaml
from jinja2 import Environment, FileSystemLoader

config = yaml.safe_load(Path("config.yaml").open().read())
template_dir = Path(config["template_dir"])
content_dir = Path(config["content_dir"])
build_dir = Path(config["build_dir"])
build_dir.mkdir(exist_ok=True, parents=True)


def main():
    build_index()
    copy_assets()


def build_index():
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


def copy_assets():
    if (build_dir / "assets").exists():
        shutil.rmtree(build_dir / "assets")
    shutil.copytree("assets", build_dir / "assets")


if __name__ == "__main__":
    main()