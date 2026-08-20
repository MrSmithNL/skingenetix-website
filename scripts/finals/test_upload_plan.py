#!/usr/bin/env python3
"""Tests for the upload plan resolver in shopify-replace-media.py.

Author: Claude Code, 2026-08-20.
Purpose: the resolver decides which live product image goes in which gallery
position and what its alt text says. Both are visible to customers and to search
engines, and the upload deletes the product's existing media, so a silent
mismatch here is a production defect that cannot be caught after the fact.

Run: python3 scripts/finals/test_upload_plan.py
"""
import importlib.util
import pathlib
import unittest

_src = pathlib.Path(__file__).with_name("shopify-replace-media.py")
_spec = importlib.util.spec_from_file_location("replace_media", _src)
replace_media = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(replace_media)

resolve_picks = replace_media.resolve_picks

PLAN = {
    "product_label": "Skingenetix Test Serum, 30ml",
    "order": [
        {"shot": "product_and_box_hero", "alt": "bottle beside its carton"},
        {"shot": "hands_only_dropper", "alt": "hands lifting the dropper"},
        {"shot": "pedestal_edge_hero", "alt": "bottle on a stone pedestal"},
    ],
}


def name(shot, n=1):
    return f"__test_serum_{shot}_{n}_skingenetix.jpg"


class ResolvePicks(unittest.TestCase):
    def test_returns_plan_order_not_alphabetical_order(self):
        # Deliberately passed in alphabetical order, which is NOT the plan order.
        files = sorted([name("product_and_box_hero"), name("hands_only_dropper"),
                        name("pedestal_edge_hero")])
        got = [p.shot for p in resolve_picks(files, PLAN)]
        self.assertEqual(got, ["product_and_box_hero", "hands_only_dropper",
                               "pedestal_edge_hero"])

    def test_alt_text_comes_from_the_plan_and_carries_the_product_label(self):
        picks = resolve_picks([name("hands_only_dropper")], PLAN)
        self.assertEqual(
            picks[0].alt,
            "Skingenetix Test Serum, 30ml — hands lifting the dropper")

    def test_a_shot_with_no_chosen_file_is_simply_skipped(self):
        picks = resolve_picks([name("hands_only_dropper")], PLAN)
        self.assertEqual([p.shot for p in picks], ["hands_only_dropper"])

    def test_file_matching_no_shot_is_an_error_not_a_silent_append(self):
        # The old code ranked unknowns last and gave them generic alt text, so a
        # renamed or mis-swept file would go live unnoticed.
        with self.assertRaises(ValueError) as e:
            resolve_picks([name("hands_only_dropper"), name("some_unplanned_shot")],
                          PLAN)
        self.assertIn("some_unplanned_shot", str(e.exception))

    def test_two_files_claiming_the_same_shot_is_an_error(self):
        with self.assertRaises(ValueError) as e:
            resolve_picks([name("hands_only_dropper", 1),
                           name("hands_only_dropper", 2)], PLAN)
        self.assertIn("hands_only_dropper", str(e.exception))

    def test_one_file_matching_two_shots_is_an_error(self):
        ambiguous = {"product_label": "X", "order": [
            {"shot": "edge_hero", "alt": "a"},
            {"shot": "pedestal_edge_hero", "alt": "b"}]}
        with self.assertRaises(ValueError) as e:
            resolve_picks([name("pedestal_edge_hero")], ambiguous)
        self.assertIn("matches 2 shots", str(e.exception))

    def test_underscore_marks_are_stripped_from_the_uploaded_filename(self):
        # Malcolm's marks are selection state; they must not become store URLs.
        picks = resolve_picks([name("hands_only_dropper")], PLAN)
        self.assertFalse(picks[0].upload_name.startswith("_"))
        self.assertEqual(picks[0].upload_name,
                         "test_serum_hands_only_dropper_1_skingenetix.jpg")

    def test_empty_selection_is_an_error(self):
        with self.assertRaises(ValueError):
            resolve_picks([], PLAN)


if __name__ == "__main__":
    unittest.main(verbosity=2)
