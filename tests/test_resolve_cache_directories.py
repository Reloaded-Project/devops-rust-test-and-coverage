import tempfile
import unittest
from pathlib import Path

from scripts.resolve_cache_directories import resolve_cache_directories
from scripts.resolve_cache_directories import write_github_env


class ResolveCacheDirectoriesTests(unittest.TestCase):
    def test_defaults_to_root_doc_directory(self) -> None:
        self.assertEqual(resolve_cache_directories(".", "", ""), ["target/doc"])

    def test_uses_target_specific_doc_directory(self) -> None:
        self.assertEqual(
            resolve_cache_directories("src", "x86_64-pc-windows-msvc", ""),
            ["src/target/x86_64-pc-windows-msvc/doc"],
        )

    def test_qualifies_relative_directories_from_project_root(self) -> None:
        self.assertEqual(
            resolve_cache_directories(
                "src",
                "x86_64-pc-windows-msvc",
                "ci-extra-cache\ntarget/custom-tool-cache\ngenerated-api\n",
            ),
            [
                "src/target/x86_64-pc-windows-msvc/doc",
                "src/ci-extra-cache",
                "src/target/custom-tool-cache",
                "src/generated-api",
            ],
        )

    def test_deduplicates_and_normalizes_paths(self) -> None:
        self.assertEqual(
            resolve_cache_directories(
                ".",
                "",
                "target/doc\n./extra\nfoo/./bar/\nfoo/bar\n",
            ),
            ["target/doc", "extra", "foo/bar"],
        )

    def test_preserves_posix_and_windows_absolute_paths(self) -> None:
        self.assertEqual(
            resolve_cache_directories(
                "src",
                "",
                "/tmp/cache-dir\nC:\\cache-dir\nrelative-cache\n",
            ),
            ["src/target/doc", "/tmp/cache-dir", "C:/cache-dir", "src/relative-cache"],
        )

    def test_writes_multiline_env_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            env_file = Path(temp_dir) / "github-env.txt"
            write_github_env(str(env_file), ["target/doc", "src/generated-api"])
            self.assertEqual(
                env_file.read_text(encoding="utf-8"),
                "RUST_CACHE_DIRECTORIES<<EOF\ntarget/doc\nsrc/generated-api\nEOF\n",
            )


if __name__ == "__main__":
    unittest.main()
