#!/usr/bin/env python3
"""Tests for matching marked run-output files back to their manifest records.

Author: Claude Code, 2026-08-21.
Purpose: Malcolm has started marking winners directly in the fan-out's own
output folder, where files already carry their SEO name, rather than in the
ALL-<product> browse folder where they carry `run-01__NN_shot_engine_N`. The
existing prepare script only understands the second form.

Two things make the match fragile:

  * renaming in Finder to add an underscore can EAT the first character - the
    2026-08-21 Matrixyl run contains `_atrixyl_..._minimal_shelf_soft_2_...`,
    which is `matrixyl` with the m consumed. Dropping that file would silently
    lose one of his picks;
  * the marks themselves are not part of the recorded name.

Getting this wrong loses a chosen image or, worse, attributes it to the wrong
engine - and engine attribution is the number the whole pipeline rebuild exists
to answer.

Run: python3 scripts/finals/test_run_output_marks.py
"""
import importlib.util
import pathlib
import unittest

_src = pathlib.Path(__file__).with_name("prepare-marked-run-output.py")
_spec = importlib.util.spec_from_file_location("prep_marked", _src)
prep_marked = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(prep_marked)

match_record = prep_marked.match_record

STEM = "matrixyl_3000_pro_collagen_10_percent_firming_repair_skin_serum"
INDEX = {
    f"{STEM}_hero_white_bg_1_skingenetix.png": {"backend": "luma", "shot_name": "hero_white_bg"},
    f"{STEM}_minimal_shelf_soft_2_skingenetix.png": {"backend": "seedream", "shot_name": "minimal_shelf_soft"},
    f"{STEM}_water_ripple_scene_2_skingenetix.png": {"backend": "nbp_pro", "shot_name": "water_ripple_scene"},
}


class MatchMarkedFile(unittest.TestCase):
    def test_single_underscore_keep(self):
        rec, name = match_record(f"_{STEM}_hero_white_bg_1_skingenetix.png", INDEX)
        self.assertEqual(rec["backend"], "luma")
        self.assertEqual(name, f"{STEM}_hero_white_bg_1_skingenetix.png")

    def test_double_underscore_publish(self):
        rec, _ = match_record(f"__{STEM}_water_ripple_scene_2_skingenetix.png", INDEX)
        self.assertEqual(rec["backend"], "nbp_pro")

    def test_finder_ate_the_first_character(self):
        # "_atrixyl_..." - the m was consumed when the underscore was typed.
        rec, name = match_record(f"_atrixyl_3000_pro_collagen_10_percent_firming_repair_skin_serum"
                                 f"_minimal_shelf_soft_2_skingenetix.png", INDEX)
        self.assertEqual(rec["backend"], "seedream")
        self.assertEqual(name, f"{STEM}_minimal_shelf_soft_2_skingenetix.png")

    def test_finder_ate_several_characters(self):
        rec, _ = match_record(f"__ixyl_3000_pro_collagen_10_percent_firming_repair_skin_serum"
                              f"_hero_white_bg_1_skingenetix.png", INDEX)
        self.assertEqual(rec["backend"], "luma")

    def test_a_file_that_matches_nothing_raises(self):
        with self.assertRaises(KeyError):
            match_record("__something_entirely_unrelated.png", INDEX)

    def test_an_ambiguous_suffix_raises_rather_than_guessing(self):
        # Two records ending the same way must never be silently resolved to one.
        idx = dict(INDEX)
        idx[f"other_{STEM}_hero_white_bg_1_skingenetix.png"] = {"backend": "flux2"}
        with self.assertRaises(KeyError):
            match_record(f"_ero_white_bg_1_skingenetix.png", idx)

    def test_exact_match_wins_over_suffix_recovery(self):
        idx = dict(INDEX)
        idx[f"x{STEM}_hero_white_bg_1_skingenetix.png"] = {"backend": "WRONG"}
        rec, _ = match_record(f"_{STEM}_hero_white_bg_1_skingenetix.png", idx)
        self.assertEqual(rec["backend"], "luma")


class MarkPrefix(unittest.TestCase):
    def test_marks_are_reported_for_restoration(self):
        self.assertEqual(prep_marked.marks("__a.png"), "__")
        self.assertEqual(prep_marked.marks("_a.png"), "_")
        self.assertEqual(prep_marked.marks("a.png"), "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
