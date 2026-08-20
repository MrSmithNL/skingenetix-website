#!/usr/bin/env python3
"""Tests for the browse-folder collector in collect-all-candidates.py.

Author: Claude Code, 2026-08-20.
Purpose: the collector is re-run whenever a later run tops a product up (the
Gemini top-ups do exactly this). Malcolm marks his choices by renaming files in
that same folder, so a re-run must recognise a marked file as already collected.
Otherwise every image he has chosen comes back a second time under its original
unmarked name, and the folder fills with duplicates of exactly the images that
matter most.

Run: python3 scripts/finals/test_collect_candidates.py
"""
import importlib.util
import os
import pathlib
import shutil
import tempfile
import unittest

_src = pathlib.Path(__file__).with_name("collect-all-candidates.py")
_spec = importlib.util.spec_from_file_location("collect_candidates", _src)
collect_candidates = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(collect_candidates)

collect = collect_candidates.collect


class CollectIsIdempotentAcrossMarks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.run = os.path.join(self.tmp, "run-01")
        os.makedirs(os.path.join(self.run, "raw"))
        for n in ("shot_a_1_skingenetix.png", "shot_b_1_skingenetix.png"):
            with open(os.path.join(self.run, "raw", n), "wb") as fh:
                fh.write(b"png")
        self.dest = os.path.join(self.tmp, "ALL-product")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def images(self):
        return sorted(f for f in os.listdir(self.dest) if f.endswith(".png"))

    def test_first_collect_links_every_candidate(self):
        collect([self.run], self.dest, "Product")
        self.assertEqual(self.images(),
                         ["run-01__shot_a_1_skingenetix.png",
                          "run-01__shot_b_1_skingenetix.png"])

    def test_plain_rerun_adds_nothing(self):
        collect([self.run], self.dest, "Product")
        collect([self.run], self.dest, "Product")
        self.assertEqual(len(self.images()), 2)

    def test_rerun_does_not_resurrect_a_file_marked_keep(self):
        collect([self.run], self.dest, "Product")
        os.rename(os.path.join(self.dest, "run-01__shot_a_1_skingenetix.png"),
                  os.path.join(self.dest, "_run-01__shot_a_1_skingenetix.png"))
        collect([self.run], self.dest, "Product")
        self.assertEqual(self.images(),
                         ["_run-01__shot_a_1_skingenetix.png",
                          "run-01__shot_b_1_skingenetix.png"])

    def test_rerun_does_not_resurrect_a_file_marked_publish(self):
        collect([self.run], self.dest, "Product")
        os.rename(os.path.join(self.dest, "run-01__shot_a_1_skingenetix.png"),
                  os.path.join(self.dest, "__run-01__shot_a_1_skingenetix.png"))
        collect([self.run], self.dest, "Product")
        self.assertEqual(self.images(),
                         ["__run-01__shot_a_1_skingenetix.png",
                          "run-01__shot_b_1_skingenetix.png"])

    def test_a_topup_run_still_adds_its_new_images(self):
        collect([self.run], self.dest, "Product")
        os.rename(os.path.join(self.dest, "run-01__shot_a_1_skingenetix.png"),
                  os.path.join(self.dest, "__run-01__shot_a_1_skingenetix.png"))
        # Gemini top-up merges into the same run directory.
        with open(os.path.join(self.run, "raw", "shot_c_1_skingenetix.png"), "wb") as fh:
            fh.write(b"png")
        collect([self.run], self.dest, "Product")
        self.assertIn("run-01__shot_c_1_skingenetix.png", self.images())
        self.assertEqual(len(self.images()), 3)

    def test_verdict_sidecar_lists_the_marked_name_not_the_original(self):
        collect([self.run], self.dest, "Product")
        os.rename(os.path.join(self.dest, "run-01__shot_a_1_skingenetix.png"),
                  os.path.join(self.dest, "__run-01__shot_a_1_skingenetix.png"))
        collect([self.run], self.dest, "Product")
        sidecar = open(os.path.join(self.dest, "_qa-verdicts.txt")).read()
        self.assertIn("__run-01__shot_a_1_skingenetix.png", sidecar)
        self.assertNotIn(" run-01__shot_a_1_skingenetix.png", sidecar)


if __name__ == "__main__":
    unittest.main(verbosity=2)
