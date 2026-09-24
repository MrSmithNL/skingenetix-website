"""Offline tests for scripts/generate-multi.py — the OpenAI model picker. No API calls.

Malcolm, 2026-09-24: the OpenAI image generator "should always be the latest one".
"""
import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("gm", ROOT / "scripts/generate-multi.py")
gm = importlib.util.module_from_spec(_s)
_s.loader.exec_module(gm)

LISTED_2026_09 = ["gpt-image-2.5-sunburst-2026-09-08", "gpt-image-2.5-flare-2026-09-08",
                  "gpt-image-2.5-sunburst", "gpt-image-2.5-flare", "gpt-image-2-2026-04-21",
                  "gpt-image-2", "chatgpt-image-latest", "gpt-image-1.5", "gpt-image-1-mini", "gpt-image-1",
                  "gpt-4o", "dall-e-3"]


def test_picks_the_newest_version_in_its_full_quality_variant():
    # flare is the small, speed-optimised variant; sunburst is the base model
    assert gm.pick_latest_image_model(LISTED_2026_09) == "gpt-image-2.5-sunburst"


def test_an_unsuffixed_release_beats_a_named_variant_of_the_same_version():
    assert gm.pick_latest_image_model(["gpt-image-3-flare", "gpt-image-3", "gpt-image-3-sunburst"]) == "gpt-image-3"


def test_a_newer_version_with_only_a_light_variant_does_not_displace_the_full_model():
    # a newer family that ships ONLY a light variant does not displace the current full-quality model
    assert gm.pick_latest_image_model(["gpt-image-2.5-sunburst", "gpt-image-3-mini"]) == "gpt-image-2.5-sunburst"


def test_version_numbers_compare_numerically_not_as_text():
    assert gm.pick_latest_image_model(["gpt-image-2.10", "gpt-image-2.9"]) == "gpt-image-2.10"


def test_falls_back_when_nothing_matches():
    assert gm.pick_latest_image_model(["dall-e-3"]) == gm.OPENAI_IMAGE_FALLBACK
