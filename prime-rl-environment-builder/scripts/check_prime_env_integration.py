#!/usr/bin/env python3
"""Verify Prime environment metadata and pulled-source installability."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11 fallback
    import tomli as tomllib  # type: ignore


PLACEHOLDER_DESCRIPTION = "Your environment description here"


class IntegrationError(RuntimeError):
    """Raised when an integration check fails."""


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check Prime environment metadata and source install behavior.",
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--env-dir", type=Path, help="Local environment directory")
    source.add_argument(
        "--env-id",
        help="Published environment ID in owner/name or owner/name@version form",
    )
    parser.add_argument(
        "--load-name",
        help="Environment name to pass to verifiers.load_environment(). Defaults to project.name.",
    )
    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help="Keep temporary pull and venv directories for inspection.",
    )
    return parser.parse_args()


def run(
    cmd: Iterable[str],
    *,
    cwd: Path | None = None,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        list(cmd),
        cwd=str(cwd) if cwd else None,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise IntegrationError(
            "\n".join(
                [
                    f"Command failed: {' '.join(cmd)}",
                    f"Exit code: {completed.returncode}",
                    f"STDOUT:\n{completed.stdout.strip() or '(empty)'}",
                    f"STDERR:\n{completed.stderr.strip() or '(empty)'}",
                ]
            )
        )
    return completed


def locate_env_dir(base: Path) -> Path:
    if (base / "pyproject.toml").exists() and (base / "README.md").exists():
        return base

    candidate_dirs: list[Path] = []
    for child in base.iterdir():
        if child.is_dir() and (child / "pyproject.toml").exists() and (child / "README.md").exists():
            candidate_dirs.append(child)

    if len(candidate_dirs) == 1:
        return candidate_dirs[0]

    for match in base.rglob("pyproject.toml"):
        parent = match.parent
        if (parent / "README.md").exists():
            return parent

    raise IntegrationError(f"Could not locate env root under {base}")


def load_pyproject(pyproject_path: Path) -> dict:
    with pyproject_path.open("rb") as handle:
        return tomllib.load(handle)


def validate_project_metadata(project: dict) -> list[CheckResult]:
    checks: list[CheckResult] = []

    def add(name: str, ok: bool, detail: str = "") -> None:
        checks.append(CheckResult(name=name, ok=ok, detail=detail))

    name = project.get("name")
    add("project.name", bool(name), repr(name))

    version = project.get("version")
    add("project.version", bool(version), repr(version))

    description = project.get("description")
    add(
        "project.description",
        bool(description) and description != PLACEHOLDER_DESCRIPTION,
        repr(description),
    )

    tags = project.get("tags")
    add("project.tags", bool(tags), repr(tags))

    readme = project.get("readme")
    add("project.readme", bool(readme), repr(readme))

    license_value = project.get("license")
    add("project.license", bool(license_value), repr(license_value))

    return checks


def assert_checks(checks: list[CheckResult]) -> None:
    failures = [check for check in checks if not check.ok]
    if failures:
        lines = ["Metadata validation failed:"]
        for failure in failures:
            lines.append(f"- {failure.name}: {failure.detail or 'missing'}")
        raise IntegrationError("\n".join(lines))


def venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def main() -> int:
    args = parse_args()
    temp_root = Path(tempfile.mkdtemp(prefix="prime_env_check_"))
    results: list[CheckResult] = []

    def record(name: str, ok: bool, detail: str = "") -> None:
        results.append(CheckResult(name=name, ok=ok, detail=detail))

    try:
        if args.env_dir:
            env_dir = args.env_dir.expanduser().resolve()
            if not env_dir.exists():
                raise IntegrationError(f"--env-dir does not exist: {env_dir}")
            record("env source", True, str(env_dir))
        else:
            pull_target = temp_root / "pulled-env"
            run(["prime", "env", "pull", args.env_id, "--target", str(pull_target)])
            env_dir = locate_env_dir(pull_target)
            record("prime env pull", True, f"{args.env_id} -> {env_dir}")

        readme_path = env_dir / "README.md"
        pyproject_path = env_dir / "pyproject.toml"
        record("README.md exists", readme_path.exists(), str(readme_path))
        record("pyproject.toml exists", pyproject_path.exists(), str(pyproject_path))
        if not readme_path.exists() or not pyproject_path.exists():
            raise IntegrationError(f"Missing README.md or pyproject.toml in {env_dir}")

        pyproject = load_pyproject(pyproject_path)
        project = pyproject.get("project", {})
        metadata_checks = validate_project_metadata(project)
        results.extend(metadata_checks)
        assert_checks(metadata_checks)

        load_name = args.load_name or project["name"]

        venv_dir = temp_root / ".venv"
        run(["uv", "venv", str(venv_dir)])
        record("uv venv", True, str(venv_dir))

        py_bin = venv_python(venv_dir)
        run(["uv", "pip", "install", "--python", str(py_bin), str(env_dir)])
        record("source install", True, str(env_dir))

        probe = "\n".join(
            [
                "from verifiers import load_environment",
                f"env = load_environment({load_name!r})",
                "print(type(env).__name__)",
                "print(hasattr(env, 'tools'))",
            ]
        )
        completed = run([str(py_bin), "-c", probe])
        record(
            "load_environment()",
            True,
            completed.stdout.strip().replace("\n", " | "),
        )

        print("Prime env integration check: PASS")
        for result in results:
            status = "PASS" if result.ok else "FAIL"
            detail = f" - {result.detail}" if result.detail else ""
            print(f"[{status}] {result.name}{detail}")
        return 0
    except IntegrationError as exc:
        print("Prime env integration check: FAIL", file=sys.stderr)
        for result in results:
            status = "PASS" if result.ok else "FAIL"
            detail = f" - {result.detail}" if result.detail else ""
            print(f"[{status}] {result.name}{detail}", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 1
    finally:
        if args.keep_temp:
            print(f"Temporary files kept at: {temp_root}")
        else:
            shutil.rmtree(temp_root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
