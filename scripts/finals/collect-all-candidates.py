#!/usr/bin/env python3
"""Gather every generated image for a product into one folder to browse.

Malcolm's rule, 2026-08-20: all the results in the same folder, nothing
excluded, and he picks. So this takes EVERY candidate from EVERY run - QA
passes, QA failures, and anything the gate never judged. The QA verdict is
recorded alongside as a text file, for reference rather than as a filter.

Files are HARDLINKED, not copied: identical to real files in Finder, instant,
and no second copy of ~2GB on disk. The run is prefixed onto the name so two
runs of the same shot and engine cannot collide.
"""
import json
import os
import sys


def present_as(existing, name):
    """Return the name this candidate already has in the folder, or None.

    Malcolm marks a choice by prefixing the filename with '_' or '__' in place,
    so on a re-run - which happens every time a later run tops a product up -
    the collected file no longer has the name it was linked under. Matching only
    the bare name would link the original back and leave a duplicate of every
    image he has chosen. See memory/malcolm-picks-winners-by-underscore.md.
    """
    for variant in (name, "_" + name, "__" + name):
        if variant in existing:
            return variant
    return None


def collect(runs, dest, label):
    os.makedirs(dest, exist_ok=True)
    existing = set(os.listdir(dest))
    verdicts, linked, skipped = {}, 0, 0
    for run in runs:
        tag = os.path.basename(run.rstrip("/"))
        qa_path = os.path.join(run, "qa.json")
        qa = {}
        if os.path.exists(qa_path):
            with open(qa_path) as fh:
                qa = {r["path"]: r for r in json.load(fh).get("results", [])}
        raw = os.path.join(run, "raw")
        if not os.path.isdir(raw):
            continue
        for f in sorted(os.listdir(raw)):
            if not f.lower().endswith(".png"):
                continue
            src = os.path.join(raw, f)
            name = f"{tag}__{f}"
            already = present_as(existing, name)
            if already is None:
                try:
                    os.link(src, os.path.join(dest, name))
                except OSError:
                    import shutil
                    shutil.copy2(src, os.path.join(dest, name))
                existing.add(name)
                already = name
                linked += 1
            else:
                skipped += 1
            r = qa.get(src) or qa.get(os.path.relpath(src))
            # Keyed by the name on disk, marks included, so the sidecar can be
            # matched against the folder after Malcolm has been through it.
            verdicts[already] = (
                f"{r['verdict']}: {','.join(r['failed'])}" if r else "not judged")

    with open(os.path.join(dest, "_qa-verdicts.txt"), "w") as fh:
        fh.write(f"{label}\n{'=' * len(label)}\n\n")
        fh.write("Every image generated for this product, across all runs.\n")
        fh.write("Nothing is excluded - the verdict is information, not a filter.\n\n")
        for k in sorted(verdicts):
            fh.write(f"{verdicts[k]:<48} {k}\n")

    counts = {}
    for v in verdicts.values():
        counts[v.split(":")[0]] = counts.get(v.split(":")[0], 0) + 1
    print(f"{label}: {len(verdicts)} images  (+{linked} linked, {skipped} already there)")
    print(f"   {counts}")
    return len(verdicts)


if __name__ == "__main__":
    dest, label = sys.argv[1], sys.argv[2]
    collect(sys.argv[3:], dest, label)
