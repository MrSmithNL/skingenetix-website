#!/usr/bin/env python3
"""Tests for the filename parser in prepare-selected-for-upload.py.

Author: Claude Code, 2026-08-20.
Purpose: Malcolm marks a keeper `_name` and a publish pick `__name`. The parser
accepted `^_?` - at most ONE leading underscore - so every `__` file failed to
parse and was silently skipped with a warning, while the `_` keeps sailed
through. On the Copper Peptide Night cream that meant his eight chosen images
were the only ones NOT prepared, and the folder filled with the runners-up
instead. The failure announces itself only as "! could not parse" among other
output, and the counts still look plausible.

Run: python3 scripts/finals/test_prepare_selected.py
"""
import importlib.util
import pathlib
import unittest

_src = pathlib.Path(__file__).with_name("prepare-selected-for-upload.py")
_spec = importlib.util.spec_from_file_location("prepare_selected", _src)
prepare_selected = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(prepare_selected)

PAT = prepare_selected.PAT


def parse(name):
    m = PAT.match(name)
    return m.groupdict() if m else None


class MarkPrefixes(unittest.TestCase):
    BASE = "run-01__31_model_face_gpt_image_0.png"

    def test_unmarked_candidate_parses(self):
        self.assertIsNotNone(parse(self.BASE))

    def test_single_underscore_keep_parses(self):
        self.assertIsNotNone(parse("_" + self.BASE))

    def test_double_underscore_publish_pick_parses(self):
        # The regression. `__` is the mark that means PUBLISH; skipping it
        # prepared everything except the images actually wanted.
        self.assertIsNotNone(parse("__" + self.BASE))

    def test_all_three_prefixes_yield_identical_fields(self):
        a, b, c = (parse(p + self.BASE) for p in ("", "_", "__"))
        self.assertEqual(a, b)
        self.assertEqual(b, c)

    def test_fields_are_what_the_seo_name_is_built_from(self):
        g = parse("__" + self.BASE)
        self.assertEqual(g["run"], "run-01")
        self.assertEqual(g["n"], "31")
        self.assertEqual(g["shot"], "model_face")
        self.assertEqual(g["be"], "gpt_image")
        self.assertEqual(g["i"], "0")

    def test_shot_names_containing_a_backend_word_still_split_correctly(self):
        g = parse("__run-02__15_jar_on_cream_swirl_gpt_image_0.png")
        self.assertEqual(g["shot"], "jar_on_cream_swirl")
        self.assertEqual(g["be"], "gpt_image")

    def test_run_02_parses_as_readily_as_run_01(self):
        self.assertIsNotNone(parse("__run-02__10_open_jar_swatch_gpt_image_0.png"))

    def test_a_supplied_image_is_still_skipped(self):
        # Supplied images carry no run/backend, are added by add-supplied-image.py
        # and must not be double-processed here.
        self.assertIsNone(
            parse("__supplied-by-malcolm__33_applying_to_cheek_closeup_external_1.png"))

    def test_browser_named_variant_is_still_skipped(self):
        # "-2" variants are the sweep's job, not this script's.
        self.assertIsNone(parse("_run-01__02_three_quarter_brand_gradient_luma_1-2.png"))

    def test_jpg_and_webp_are_accepted(self):
        for ext in ("jpg", "jpeg", "webp"):
            self.assertIsNotNone(parse(f"__run-01__31_model_face_luma_0.{ext}"), ext)


if __name__ == "__main__":
    unittest.main(verbosity=2)
