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

    for page_key, page_cfg in config["pages"].items():
        build_page(page_key, page_cfg, config, template_dir, content_dir, build_dir)

    build_news_posts(config, template_dir, content_dir, build_dir)
    copy_assets(build_dir)
    print("Build complete.")


def make_environment(template_dir):
    env = Environment(loader=FileSystemLoader(template_dir))
    env.filters["asset_url"] = lambda url: url if url.startswith(("http://", "https://", "/")) else f"/{url}"
    return env


def build_page(page_key, page_cfg, config, template_dir, content_dir, build_dir):
    environment = make_environment(template_dir)

    content_file = content_dir / f"{page_key}.yaml"
    content = yaml.safe_load(content_file.open().read())[page_key]

    # Sort news posts by date, newest first
    if "posts" in content:
        content["posts"] = sorted(content["posts"], key=lambda p: p.get("date", ""), reverse=True)

    page_file = build_dir / page_cfg["file"]
    page_file.parent.mkdir(exist_ok=True, parents=True)

    page_template = environment.from_string(
        (template_dir / page_cfg["template"]).open().read()
    )

    html = page_template.render(
        page_url=config["deploy_url"] + page_cfg["url"],
        **config,
        **content,
    )

    with page_file.open("w") as f:
        f.write(html)


def build_news_posts(config, template_dir, content_dir, build_dir):
    environment = make_environment(template_dir)
    content_file = content_dir / "news.yaml"
    news_content = yaml.safe_load(content_file.open().read())["news"]

    post_template = environment.from_string(
        (template_dir / "news_post.html").open().read()
    )

    for post in news_content["posts"]:
        post_dir = build_dir / "news" / post["slug"]
        post_dir.mkdir(exist_ok=True, parents=True)

        html = post_template.render(
            page_url=config["deploy_url"] + f"/news/{post['slug']}/",
            **config,
            **post,
        )

        with (post_dir / "index.html").open("w") as f:
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