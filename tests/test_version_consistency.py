# SPDX-License-Identifier: MIT
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _pyproject_version() -> str:
    with (ROOT / "pyproject.toml").open("rb") as file:
        return tomllib.load(file)["project"]["version"]


def test_pyproject_and_plugin_versions_match() -> None:
    plugin_yaml_content = (ROOT / "plugin.yaml").read_text(encoding="utf-8")
    match = re.search(r"^version:\s*(\S+)", plugin_yaml_content, re.MULTILINE)
    assert match is not None, "plugin.yaml has no version field"

    plugin_yaml_version = match.group(1)

    assert _pyproject_version() == plugin_yaml_version


def test_pyproject_version_matches_package_version() -> None:
    import hermes_nanogpt_provider

    assert hermes_nanogpt_provider.__version__ == _pyproject_version()
