#!/usr/bin/env python3
"""Exercise the file-size gate against real Git histories."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CHECK = Path(__file__).with_name("check-pr-file-sizes.py").resolve()
MIB = 1024 * 1024


class FileSizeGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_AUTHOR_NAME="test", GIT_AUTHOR_EMAIL="test@example.com",
                        GIT_COMMITTER_NAME="test", GIT_COMMITTER_EMAIL="test@example.com")
        self.git("init", "-q")
        self.write("baseline.txt", b"baseline")
        self.base = self.commit()

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, env=self.env,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.decode().strip()

    def write(self, name, content):
        (self.repo / name).write_bytes(content)

    def commit(self):
        self.git("add", "-A")
        tree = self.git("write-tree")
        parents = []
        try:
            parents = ["-p", self.git("rev-parse", "HEAD")]
        except subprocess.CalledProcessError:
            pass
        sha = self.git("commit-tree", tree, *parents, "-m", "test")
        self.git("update-ref", "HEAD", sha)
        return sha

    def check(self):
        return subprocess.run([sys.executable, str(CHECK), self.base, "HEAD"], cwd=self.repo,
                              env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def test_exact_git_limit_passes_with_warning(self):
        self.write("limit.bin", b"x" * (5 * MIB))
        self.commit()
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("::warning::", result.stdout)
        self.assertNotIn("::error::", result.stdout)

    def test_oversized_git_file_is_rejected_even_when_deleted_later(self):
        self.write("oversize.bin", b"x" * (5 * MIB + 1))
        self.commit()
        (self.repo / "oversize.bin").unlink()
        self.commit()
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("oversize.bin", result.stdout)

    def test_lfs_pointer_uses_original_size(self):
        pointer = ("version https://git-lfs.github.com/spec/v1\n"
                   + "oid sha256:" + "a" * 64 + "\nsize 52428801\n")
        self.write("asset.bin", pointer.encode())
        self.commit()
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("LFS object", result.stdout)

    def test_lfs_limit_is_inclusive(self):
        pointer = ("version https://git-lfs.github.com/spec/v1\n"
                   + "oid sha256:" + "b" * 64 + "\nsize 52428800\n")
        self.write("at-limit.bin", pointer.encode())
        self.commit()
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("::error::", result.stdout)

    def test_warning_threshold_is_inclusive(self):
        self.write("small.bin", b"x" * (2 * MIB))
        self.commit()
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("::warning::", result.stdout)
        self.write("small.bin", b"x" * (2 * MIB + 1))
        self.commit()
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("::warning::", result.stdout)

    def test_existing_large_blob_is_ignored_until_added_at_new_path(self):
        self.write("existing.bin", b"x" * (5 * MIB + 1))
        self.base = self.commit()
        self.write("small.txt", b"ok")
        self.commit()
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.write("copy.bin", b"x" * (5 * MIB + 1))
        self.commit()
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("copy.bin", result.stdout)

    def test_total_size_warning_does_not_block(self):
        for i in range(11):
            self.write(f"asset-{i}.bin", bytes([i]) * (5 * MIB))
        self.commit()
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("total 55.00 MiB", result.stdout)


if __name__ == "__main__":
    unittest.main()
