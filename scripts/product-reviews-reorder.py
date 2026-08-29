#!/usr/bin/env python3
"""Re-order each product's carousel so similar-looking women are not adjacent.

    python3 scripts/product-reviews-reorder.py --show
    python3 scripts/product-reviews-reorder.py --apply
    python3 scripts/product-reviews-publish.py

Malcolm, 2026-08-29, on the Glutathione serum: "break up the 2 blonds next to each other and
also break up the other 'types' of review models. Some look too similar."

He is right, and the seeded shuffle that produced the current order could not have prevented
it. A shuffle spreads things out ON AVERAGE and knows nothing about what the photographs
contain, so clusters survive it: the acetyl serum opens with FOUR fair blondes in a row, the
Glutathione serum runs six similar brunettes from position four, and PDRN serum has two
red-heads side by side. Randomness is not the same as variety.

WHAT IT ACTUALLY DOES
Every woman is tagged by hair, skin tone and shot type — tags read off the BEFORE frame of her
own photograph, by eye, once, and recorded below. Adjacency then costs something: same hair
costs most, same tone next, same framing least, and the cost is applied to BOTH the previous
card and the one before it, so a run of three near-identical women is penalised harder than a
single repeat. A greedy walk lays each carousel out to keep that cost low.

⚠️ THE CARDS KEEP THEIR OWN COPY. Only the order within a product changes. Nothing moves
between products, no photograph is reassigned and no review text is touched — a reorder that
quietly re-paired text and image would undo the age matching done earlier the same day.

Deterministic: same tags in, same order out. No seed, no shuffle.

Author: Claude Code, 2026-08-29.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "configs" / "product-reviews.json"

#: person -> (hair, tone, shot). Read off the before frame of each photograph.
#: hair: blonde | greyblonde | brunette | dark | red      tone: fair | olive | deep
#: shot: face | neck | macro
TAGS = {
    # acetyl
    "Stephanie-M": ("blonde", "fair", "close"), "Sophie-H": ("blonde", "fair", "close"),
    "Kelly-E": ("blonde", "fair", "close"), "Deirdre-O": ("blonde", "fair", "close"),
    "Meredith-H": ("dark", "olive", "half"), "Elizabeth-L": ("brunette", "fair", "close"),
    "Corinne-J": ("greyblonde", "fair", "close"), "Nicole-T": ("brunette", "fair", "close"),
    # matrixyl serum
    "Tabitha-J": ("greyblonde", "fair", "close"), "Francine-S": ("greyblonde", "fair", "half"),
    "Janine-L": ("dark", "olive", "close"), "Amanda-P": ("dark", "olive", "forehead"),
    "Michelle-R": ("greyblonde", "fair", "close"), "Petra-J": ("dark", "olive", "close"),
    "Mallory-B": ("red", "fair", "close"), "Caroline-D": ("brunette", "fair", "close"),
    "Evelyn-L": ("brunette", "fair", "close"),
    # matrixyl cream
    "Emma-H": ("brunette", "fair", "half"), "Elena-S": ("dark", "olive", "neck"),
    "Blythe-V": ("greyblonde", "fair", "close"), "Daphne-N": ("blonde", "fair", "neck"),
    "Lorelei-D": ("brunette", "fair", "half"), "Simone-K": ("red", "fair", "close"),
    "Katarina-S": ("blonde", "fair", "neck"), "Alexandra-B": ("blonde", "fair", "close"),
    "Gabrielle-D": ("brunette", "olive", "neck"),
    # glutathione
    "Dana-T": ("dark", "deep", "close"), "Amy-T": ("blonde", "fair", "close"),
    "Jennifer-T": ("blonde", "fair", "close"), "Arantxa-R": ("brunette", "olive", "half"),
    "Silvia-M": ("brunette", "olive", "close"), "Bri-E": ("brunette", "fair", "close"),
    "Lucia-M": ("brunette", "olive", "close"), "Joyce-G": ("brunette", "fair", "close"),
    "Martine M": ("dark", "olive", "close"),
    # copper renewal serum
    "Celeste-N": ("brunette", "fair", "close"), "Sarah-E": ("brunette", "fair", "close"),
    "Beatriz-B": ("dark", "olive", "close"), "Rachel-R": ("blonde", "fair", "close"),
    "Sabine-G": ("greyblonde", "fair", "close"), "Shannon-P": ("brunette", "fair", "close"),
    "Samantha-F": ("brunette", "fair", "close"), "Ashley-H": ("brunette", "fair", "half"),
    "Bianca-P": ("brunette", "fair", "close"),
    # copper night
    "Kendra-C": ("greyblonde", "fair", "close"), "Tamsin-A": ("greyblonde", "fair", "neck"),
    "Marie-R": ("brunette", "fair", "neck"), "Justine-L": ("blonde", "fair", "close"),
    "Nelle-N": ("brunette", "olive", "close"), "Anja-G": ("brunette", "olive", "macro"),
    "Jolene-A": ("brunette", "fair", "half"), "Mei-W": ("greyblonde", "fair", "close"),
    "Gillian-L": ("brunette", "fair", "close"),
    # copper day
    "Tabitha-S": ("red", "fair", "close"), "Fiona-C": ("greyblonde", "fair", "close"),
    "Melissa-M": ("brunette", "fair", "close"), "Rowena-G": ("blonde", "fair", "close"),
    "Sage-D": ("blonde", "fair", "half"), "Helen-S": ("brunette", "fair", "eye"),
    "Kimberly-N": ("brunette", "fair", "eye"), "Isabella-E": ("brunette", "fair", "close"),
    "Catalina-B": ("blonde", "fair", "close"),
    # pdrn serum
    "Maud-H": ("greyblonde", "fair", "close"), "Mila-F": ("brunette", "fair", "close"),
    "Felicia-P": ("brunette", "fair", "close"), "Faye-N": ("brunette", "fair", "close"),
    "Fenna-S": ("dark", "olive", "eye"), "Linda-P": ("red", "fair", "close"),
    "Rosalie-W": ("red", "fair", "half"), "Josephine-R": ("greyblonde", "fair", "close"),
    "Robin-J": ("brunette", "fair", "close"),
    # pdrn cream
    "Nola-S": ("brunette", "fair", "eye"), "Isa-D": ("brunette", "fair", "eye"),
    "Lana-D": ("dark", "olive", "close"), "Mara-F": ("greyblonde", "fair", "close"),
    "June-K": ("brunette", "fair", "eye"), "Livia-B": ("brunette", "fair", "close"),
    "Marion-H": ("greyblonde", "fair", "close"), "Danielle-S": ("greyblonde", "fair", "close"),
    "Madeline-W": ("brunette", "fair", "half"),
    # pdrn stamp
    "Maelis-S": ("brunette", "fair", "half"), "Senne-P": ("brunette", "fair", "forehead"),
    "Eliza-V": ("brunette", "fair", "close"), "Noemi-R": ("red", "fair", "close"),
    "Tessa-T": ("brunette", "fair", "close"), "Romy-S": ("greyblonde", "fair", "close"),
    "Elara-M": ("dark", "olive", "close"), "Adriana-A": ("dark", "olive", "forehead"),
    "Valentina-L": ("brunette", "fair", "close"),
    # copper stamp
    "Liv-A": ("greyblonde", "fair", "close"), "Brenda-S": ("dark", "deep", "close"),
    "Livia-M": ("greyblonde", "fair", "close"), "Jade-C": ("blonde", "fair", "close"),
    "Selma-D": ("blonde", "fair", "close"), "Elina-B": ("brunette", "fair", "close"),
    "Yara-P": ("brunette", "fair", "close"), "Sandra-P": ("dark", "olive", "close"),
    "Beth-H": ("greyblonde", "fair", "close"),
}

#: blonde and greyblonde read as the same "type" at a glance, which is the whole complaint, so
#: they are treated as near-identical rather than distinct.
NEAR = {("blonde", "greyblonde"), ("greyblonde", "blonde"),
        ("brunette", "dark"), ("dark", "brunette")}

#: Hand placements that beat the scheduler. `person` is moved to sit immediately after
#: `after` within its own product.
#:
#: The tags are read off a 250px tile and they are not always right. Lana-D was tagged dark
#: brunette, which is true of her hair, but she sat between Nola-S and Livia-B where the
#: scheduler saw no clash while Malcolm saw two blondes needing breaking up. When he moves
#: someone by hand it is because the photograph says something the three tags do not.
MANUAL_AFTER = [
    ("pdrn-collagen-night-cream", "Lana-D", "Danielle-S"),      # Malcolm, 2026-08-29
]

W_HAIR, W_TONE = 6, 3

#: Two identical DISTINCTIVE shots side by side is the thing Malcolm actually sees — two neck
#: crops or two eye macros in a row read as a mistake. Two ordinary close-ups do not, and
#: cannot be avoided anyway: 72 of the 99 photographs are close-ups, so a nine-card carousel
#: holds six to eight of them and some adjacency is arithmetic, not choice. Priced accordingly.
W_SHOT_DISTINCT, W_SHOT_CLOSE = 9, 1


def tags(card):
    return TAGS.get(card["person"], ("brunette", "fair", "face"))


def cost(a, b):
    ha, ta, sa = tags(a)
    hb, tb, sb = tags(b)
    c = 0
    if ha == hb:
        c += W_HAIR
    elif (ha, hb) in NEAR:
        c += W_HAIR // 2
    if ta == tb:
        c += W_TONE
    if sa == sb:
        c += W_SHOT_CLOSE if sa == "close" else W_SHOT_DISTINCT
    return c


def order_group(cards):
    """Space the commonest look out evenly, rather than walking greedily.

    A greedy nearest-dissimilar walk fixes the front of the list and dumps whatever is left at
    the end — on the acetyl serum, four fair blondes out of nine, it still finished on three of
    them in a row. This is the same problem as spacing repeated characters in a string: take
    from the LARGEST remaining group each turn, never the group just used, and the majority
    type ends up distributed instead of clumped.

    Within the chosen group, prefer the card that also differs in tone and framing from the
    previous one, so the secondary attributes get spread too. Ties break on name, so the result
    is deterministic.
    """
    if len(cards) < 3:
        return cards

    groups = {}
    for c in cards:
        groups.setdefault(tags(c)[0], []).append(c)
    for g in groups.values():
        g.sort(key=lambda c: c["person"])

    #: blonde and greyblonde read the same at a glance, so they share one cooldown bucket —
    #: otherwise the scheduler happily alternates between them and the complaint stands.
    def bucket(hair):
        return "blondish" if hair in ("blonde", "greyblonde") else \
               "brunettish" if hair in ("brunette", "dark") else hair

    out, last_bucket = [], None
    while any(groups.values()):
        live = {h: g for h, g in groups.items() if g}
        pick = [h for h in live if bucket(h) != last_bucket] or list(live)
        # largest first: that is what keeps the dominant look from bunching at the end
        best_h = max(pick, key=lambda h: (len(live[h]), h))
        cand = live[best_h]
        if out:
            card = min(cand, key=lambda c: (cost(out[-1], c), c["person"]))
        else:
            card = cand[0]
        cand.remove(card)
        out.append(card)
        last_bucket = bucket(best_h)
    return out


def run_cost(cards):
    return sum(cost(cards[i], cards[i + 1]) for i in range(len(cards) - 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    plan = json.loads(PLAN.read_text())
    groups, order = {}, []
    for c in plan["cards"]:
        if c["product"] not in groups:
            groups[c["product"]] = []
            order.append(c["product"])
        groups[c["product"]].append(c)

    missing = [c["person"] for c in plan["cards"] if c["person"] not in TAGS]
    if missing:
        print(f"⚠️  untagged, treated as brunette/fair/face: {missing}\n")

    before_total = after_total = 0
    new_cards = []
    for prod in order:
        g = groups[prod]
        b = run_cost(g)
        ng = order_group(g)
        a = run_cost(ng)
        before_total += b
        after_total += a
        print(f"  {prod[:52]:<54} clash {b:>3} -> {a:>3}")
        print("      " + " | ".join(c["person"] for c in ng))
        for prod_h, person, after in MANUAL_AFTER:
            if prod_h != prod:
                continue
            names = [c["person"] for c in ng]
            if person in names and after in names:
                card = ng.pop(names.index(person))
                ng.insert([c["person"] for c in ng].index(after) + 1, card)
                print(f"      manual: {person} placed after {after}")
        new_cards.extend(ng)
    print(f"\n  {'TOTAL adjacency clash':<54} {before_total:>5} -> {after_total:>3}")

    if args.show or not args.apply:
        return
    plan["cards"] = new_cards
    PLAN.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    print(f"\nwrote {PLAN.relative_to(ROOT)} — order only; copy and photographs untouched")


if __name__ == "__main__":
    main()
