import os
from typing import Any
from typing import Dict

import yaml
from jinja2 import Environment
from jinja2 import FileSystemLoader
from marko import convert

# Singular massive selection of emojis for chaos
EMOJIS = [
    "☠️",
    "🔥",
    "✨",
    "🤖",
    "🎨",
    "📖",
    "🚀",
    "💾",
    "🎭",
    "💃",
    "🛠",
    "⚙️",
    "🧰",
    "🧨",
    "⚡",
    "ϟ",
    "☣️",
    "🩸",
    "🖤",
    "🗡",
    "⚔️",
    "🚧",
    "📦",
    "📎",
    "✎",
    "🖋",
    "🧪",
    "🧬",
    "📐",
    "📈",
    "🎯",
    "🏴",
    "⏳",
    "♻️",
    "🧠",
    "🤯",
    "🐍",
    "👾",
    "🐙",
    "🕷",
    "🧱",
    "📡",
    "🛰",
    "🧿",
]


def markdown_filter(text: str) -> str:
    return convert(text)


def load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        content = yaml.safe_load(f)

    return content


def main() -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_data_file = os.path.join(base_dir, "data", "content.yaml")
    data = load_yaml(yaml_data_file)
    data["emojis"] = EMOJIS

    env = Environment(
        loader=FileSystemLoader(os.path.join(base_dir, "templates")), autoescape=True
    )
    env.filters["markdown"] = markdown_filter

    # Render template to root/index.html
    template = env.get_template("index.html")
    rendered = template.render(**data)

    with open(os.path.join(base_dir, "index.html"), "w") as f:
        f.write(rendered)


if __name__ == "__main__":
    main()
