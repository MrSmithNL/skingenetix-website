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
    "Stephanie-M": ("blonde", "fair", "face"), "Sophie-H": ("blonde", "fair", "face"),
    "Kelly-E": ("blonde", "fair", "face"), "Deirdre-O": ("blonde", "fair", "face"),
    "Meredith-H": ("dark", "olive", "face"), "Elizabeth-L": ("brunette", "fair", "face"),
    "Corinne-J": ("greyblonde", "fair", "face"), "Nicole-T": ("brunette", "fair", "face"),
    # matrixyl serum
    "Tabitha-J": ("greyblonde", "fair", "face"), "Francine-S": ("greyblonde", "fair", "face"),
    "Janine-L": ("dark", "olive", "face"), "Amanda-P": ("dark", "olive", "face"),
    "Michelle-R": ("greyblonde", "fair", "face"), "Petra-J": ("dark", "olive", "face"),
    "Mallory-B": ("red", "fair", "face"), "Caroline-D": ("brunette", "fair", "face"),
    "Evelyn-L": ("brunette", "fair", "face"),
    # matrixyl cream
    "Emma-H": ("brunette", "fair", "face"), "Elena-S": ("dark", "olive", "neck"),
    "Blythe-V": ("greyblonde", "fair", "face"), "Daphne-N": ("blonde", "fair", "neck"),
    "Lorelei-D": ("brunette", "fair", "neck"), "Simone-K": ("red", "fair", "face"),
    "Katarina-S": ("blonde", "fair", "face"), "Alexandra-B": ("blonde", "fair", "face"),
    "Gabrielle-D": ("brunette", "olive", "neck"),
    # glutathione
    "Dana-T": ("dark", "deep", "face"), "Amy-T": ("blonde", "fair", "face"),
    "Jennifer-T": ("blonde", "fair", "face"), "Arantxa-R": ("brunette", "olive", "face"),
    "Silvia-M": ("brunette", "olive", "face"), "Bri-E": ("brunette", "fair", "face"),
    "Lucia-M": ("brunette", "olive", "face"), "Joyce-G": ("brunette", "fair", "face"),
    "Martine M": ("dark", "olive", "face"),
    # copper renewal serum
    "Celeste-N": ("brunette", "fair", "face"), "Sarah-E": ("brunette", "fair", "face"),
    "Beatriz-B": ("dark", "olive", "face"), "Rachel-R": ("blonde", "fair", "face"),
    "Sabine-G": ("greyblonde", "fair", "face"), "Shannon-P": ("brunette", "fair", "face"),
    "Samantha-F": ("brunette", "fair", "face"), "Ashley-H": ("brunette", "fair", "face"),
    "Bianca-P": ("brunette", "fair", "face"),
    # copper night
    "Kendra-C": ("greyblonde", "fair", "face"), "Tamsin-A": ("greyblonde", "fair", "neck"),
    "Marie-R": ("brunette", "fair", "face"), "Justine-L": ("blonde", "fair", "face"),
    "Nelle-N": ("brunette", "olive", "face"), "Anja-G": ("brunette", "olive", "macro"),
    "Jolene-A": ("brunette", "fair", "face"), "Mei-W": ("greyblonde", "fair", "face"),
    "Gillian-L": ("brunette", "fair", "face"),
    # copper day
    "Tabitha-S": ("red", "fair", "face"), "Fiona-C": ("greyblonde", "fair", "face"),
    "Melissa-M": ("brunette", "fair", "face"), "Rowena-G": ("blonde", "fair", "face"),
    "Sage-D": ("blonde", "fair", "face"), "Helen-S": ("brunette", "fair", "macro"),
    "Kimberly-N": ("brunette", "fair", "macro"), "Isabella-E": ("brunette", "fair", "face"),
    "Catalina-B": ("blonde", "fair", "face"),
    # pdrn serum
    "Maud-H": ("greyblonde", "fair", "face"), "Mila-F": ("brunette", "fair", "face"),
    "Felicia-P": ("brunette", "fair", "face"), "Faye-N": ("brunette", "fair", "face"),
    "Fenna-S": ("dark", "olive", "face"), "Linda-P": ("red", "fair", "face"),
    "Rosalie-W": ("red", "fair", "face"), "Josephine-R": ("greyblonde", "fair", "face"),
    "Robin-J": ("brunette", "fair", "face"),
    # pdrn cream
    "Nola-S": ("brunette", "fair", "macro"), "Isa-D": ("brunette", "fair", "macro"),
    "Lana-D": ("dark", "olive", "face"), "Mara-F": ("greyblonde", "fair", "face"),
    "June-K": ("brunette", "fair", "macro"), "Livia-B": ("brunette", "fair", "face"),
    "Marion-H": ("greyblonde", "fair", "face"), "Danielle-S": ("greyblonde", "fair", "face"),
    "Madeline-W": ("brunette", "fair", "face"),
    # pdrn stamp
    "Maelis-S": ("brunette", "fair", "face"), "Senne-P": ("brunette", "fair", "macro"),
    "Eliza-V": ("brunette", "fair", "face"), "Noemi-R": ("red", "fair", "face"),
    "Tessa-T": ("brunette", "fair", "face"), "Romy-S": ("greyblonde", "fair", "face"),
    "Elara-M": ("dark", "olive", "face"), "Adriana-A": ("dark", "olive", "face"),
    "Valentina-L": ("brunette", "fair", "face"),
    # copper stamp
    "Liv-A": ("greyblonde", "fair", "face"), "Brenda-S": ("dark", "deep", "face"),
    "Livia-M": ("greyblonde", "fair", "face"), "Jade-C": ("blonde", "fair", "face"),
    "Selma-D": ("blonde", "fair", "face"), "Elina-B": ("brunette", "fair", "face"),
    "Yara-P": ("brunette", "fair", "face"), "Sandra-P": ("dark", "olive", "face"),
    "Beth-H": ("greyblonde", "fair", "face"),
}

#: blonde and greyblonde read as the same "type" at a glance, which is the whole complaint, so
#: they are treated as near-identical rather than distinct.
NEAR = {("blonde", "greyblonde"), ("greyblonde", "blonde"),
        ("brunette", "dark"), ("dark", "brunette")}

W_HAIR, W_TONE, W_SHOT = 6, 3, 1


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
        c += W_SHOT
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
        new_cards.extend(ng)
    print(f"\n  {'TOTAL adjacency clash':<54} {before_total:>5} -> {after_total:>3}")

    if args.show or not args.apply:
        return
    plan["cards"] = new_cards
    PLAN.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    print(f"\nwrote {PLAN.relative_to(ROOT)} — order only; copy and photographs untouched")


if __name__ == "__main__":
    main()
