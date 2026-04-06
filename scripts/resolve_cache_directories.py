#!/usr/bin/env python3
"""Build the cache directory list for this action.

We always include the rustdoc output directory, then merge any extra
``cache-directories`` entries from the workflow. Keeping that logic here makes
``action.yml`` smaller and easy to test.
"""

from __future__ import annotations

import ntpath
import os
import posixpath


def main() -> int:
    """Resolve cache directories and export them to GitHub Actions environment.

    Reads configuration from environment variables, builds the cache directory list,
    and either writes it to the GitHub environment file or prints to stdout.

    Returns:
        0 on success, non-zero on failure.
    """
    project_path = os.environ.get("INPUT_RUST_PROJECT_PATH", ".")
    target_triple = os.environ.get("INPUT_TARGET", "")
    extra_directories = os.environ.get("INPUT_CACHE_DIRECTORIES", "")
    github_env = os.environ.get("GITHUB_ENV")

    directories = resolve_cache_directories(
        project_path=project_path,
        target_triple=target_triple,
        extra_directories=extra_directories,
    )

    if github_env:
        write_github_env(github_env, directories)
    else:
        for directory in directories:
            print(directory)

    return 0


def resolve_cache_directories(
    project_path: str, target_triple: str, extra_directories: str
) -> list[str]:
    """Build the cache directory list for a Rust project.

    Always includes the rustdoc output directory, then merges any extra directories
    from the workflow input, deduplicating by qualified path.

    Arguments:
        project_path: Path to the Rust project root (relative or absolute).
        target_triple: Target triple for cross-compilation (e.g., "x86_64-unknown-linux-gnu").
        extra_directories: Newline-separated list of additional cache directories.

    Returns:
        List of qualified cache directory paths, with rustdoc directory first.
    """
    default_doc_dir = "target/doc"
    if target_triple:
        default_doc_dir = f"target/{target_triple}/doc"

    resolved: list[str] = [_qualify_path(default_doc_dir, project_path)]
    seen = set(resolved)

    for raw_line in extra_directories.splitlines():
        directory = raw_line.strip().rstrip("\r")
        if not directory:
            continue

        qualified = _qualify_path(directory, project_path)
        if qualified in seen:
            continue

        resolved.append(qualified)
        seen.add(qualified)

    return resolved


def write_github_env(env_file: str, directories: list[str]) -> None:
    """Export the resolved cache directories to a GitHub Actions environment file.

    Writes the directories as a multiline environment variable that downstream
    workflow steps can read from `RUST_CACHE_DIRECTORIES`.

    Arguments:
        env_file: Path to the GitHub environment file.
        directories: List of cache directory paths to export.
    """
    with open(env_file, "a", encoding="utf-8") as handle:
        handle.write("RUST_CACHE_DIRECTORIES<<EOF\n")
        for directory in directories:
            handle.write(f"{directory}\n")
        handle.write("EOF\n")


def _qualify_path(path: str, project_path: str) -> str:
    """Resolve a path relative to the Rust project root.

    Absolute paths are normalized as-is. Relative paths are joined with
    the project path and normalized.

    Arguments:
        path: The path to qualify (can be absolute or relative).
        project_path: The Rust project root path.

    Returns:
        Normalized path, or empty string if path is empty.
    """
    if not path:
        return ""

    normalized_for_check = path.replace("\\", "/")
    if posixpath.isabs(normalized_for_check) or ntpath.isabs(path):
        return _normalize_path(path)

    if project_path == ".":
        return _normalize_path(path)

    return _normalize_path(posixpath.join(project_path, path))


def _normalize_path(path: str) -> str:
    """Normalize a path using POSIX forward slashes.

    Converts backslashes to forward slashes and normalizes the path,
    but does not make it absolute.

    Arguments:
        path: The path to normalize.

    Returns:
        Normalized POSIX-style path.
    """
    path = path.replace("\\", "/")
    normalized = posixpath.normpath(path)
    if normalized == ".":
        return "."
    return normalized


if __name__ == "__main__":
    raise SystemExit(main())
