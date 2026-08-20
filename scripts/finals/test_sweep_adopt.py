#!/usr/bin/env python3
"""Tests for how the sweep derives a shot name when adopting a stray file.

Author: Claude Code, 2026-08-20.
Purpose: Malcolm drops files into the finals folder from two different places,
and each mangles the name its own way. A browser appends "-2" before the
extension; Finder appends " copy" when the name collides with a file already
there. The adopt regex knew about the first and not the second, so a Finder copy
lost its shot name entirely and was filed as "supplied_1" - which then reads as
a shot called "supplied" in the manifest, the alt text and eventually the store
URL. The mark survives, so the loss is quiet.

Run: python3 scripts/finals/test_sweep_adopt.py
"""
import importlib.util
import pathlib
import unittest

_src = pathlib.Path(__file__).with_name("sweep-finals-folder.py")
_spec = importlib.util.spec_from_file_location("sweep_finals", _src)
sweep_finals = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sweep_finals)

shot_from = sweep_finals.shot_from
marks = sweep_finals.marks

SEO = "copper_peptide_ghk_cu_advanced_day_repair_face_cream"


class ShotNameFromStrayFile(unittest.TestCase):
    def test_clean_name_on_convention(self):
        self.assertEqual(
            shot_from(f"{SEO}_silver_jar_dramatic_shadow_2_skingenetix", SEO),
            "silver_jar_dramatic_shadow")

    def test_browser_dash_suffix(self):
        self.assertEqual(
            shot_from(f"{SEO}_silver_jar_dramatic_shadow_2_skingenetix-2", SEO),
            "silver_jar_dramatic_shadow")

    def test_finder_copy_suffix(self):
        # The regression: Finder's " copy" when the name already exists.
        self.assertEqual(
            shot_from(f"{SEO}_silver_jar_dramatic_shadow_2_skingenetix copy", SEO),
            "silver_jar_dramatic_shadow")

    def test_finder_numbered_copy_suffix(self):
        self.assertEqual(
            shot_from(f"{SEO}_silver_jar_dramatic_shadow_2_skingenetix copy 3", SEO),
            "silver_jar_dramatic_shadow")

    def test_both_suffixes_together(self):
        self.assertEqual(
            shot_from(f"{SEO}_range_stacked_jars_1_skingenetix-2 copy", SEO),
            "range_stacked_jars")

    def test_shot_name_containing_digits_survives(self):
        self.assertEqual(
            shot_from(f"{SEO}_open_jar_swatch_10_skingenetix copy", SEO),
            "open_jar_swatch")

    def test_a_genuinely_foreign_name_still_falls_back(self):
        # An image with no relationship to the convention has no shot to recover.
        self.assertEqual(shot_from("IMG_4821", SEO), "supplied")

    def test_another_products_name_is_not_adopted_as_a_shot(self):
        self.assertEqual(
            shot_from("glutathione_2_percent_hero_white_bg_1_skingenetix", SEO),
            "supplied")


class MarksAreLeftAlone(unittest.TestCase):
    def test_no_mark(self):
        self.assertEqual(marks("name.jpg"), "")

    def test_keep_mark(self):
        self.assertEqual(marks("_name.jpg"), "_")

    def test_publish_mark(self):
        self.assertEqual(marks("__name.jpg"), "__")


if __name__ == "__main__":
    unittest.main(verbosity=2)
