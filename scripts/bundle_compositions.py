"""The 14 bundle-set compositions that actually earned a selection — written once, reusable
for any bundle.

Importable module, not a script. Consumer: `scripts/build-bundle-set.py`.

WHY 14 AND NOT 51
The Copper Peptide run briefed 51 slots across 6 waves and produced 510 candidates. Malcolm
selected 36 and finally marked 12. **31 of the 51 slots earned no selection at all** — batch 6
alone was 11 slots and 110 candidates for three shortlist picks and zero final marks. Repeating
the full set nine more times would spend most of the budget on compositions already measured as
unwanted. What survives here is every composition that produced a FINAL MARK (12), plus two
that earned multiple shortlist picks: the two-jar tower and the styled oak shelf.

Dropped: the whole bathroom-environment family except the stone shelf; the eight unselected
hero-white variants; every model-in-frame slot; and all of batch 6's stacks bar the tower.

PLACEHOLDERS, BECAUSE A BUNDLE IS NOT ALWAYS THREE PRODUCTS
The Copper builders hardcoded "the day jar / the serum bottle / the night jar". Six of the nine
remaining bundles hold two products, and one holds no cream jar at all. So compositions address
products by placeholder:

    {A} {B} {C}   the bundle's products in registry order (bottles first, then jars)
    {BOTTLE}      the first bottle-form product
    {JAR} {JAR2}  the jar-form products, in order
    {ALL}         a natural-language list of every product in the bundle

`requires` filters a composition out of a bundle it cannot serve: the open-jar macros need a
jar to open, and the tower needs two jars to stack. Filtering is not optional — a brief that
tells an engine to open a jar in a bundle of two serum bottles invents one.

Author: Claude Code, 2026-09-11.
"""

#: id, requires, ARRANGEMENT, SCENE, FRAME.
#: `requires` keys: min_products (default 2), jars (default 0).
COMPOSITIONS = [
    dict(
        id="pyramid-blocks", requires=dict(),
        arrangement=(
            "ARRANGEMENT. The products are arranged as a clear triangle on stone cubes of "
            "different heights: {A} stands raised highest on the tallest cube, and "
            "{OTHERS} {SIT} lower and slightly forward beside it, their fronts "
            "turned a few degrees inward towards the camera. The silhouettes together read as "
            "a triangle with {A} at the top point. Every front label faces the camera and "
            "stays fully legible."),
        scene=(
            "SCENE. Pale cool-grey stone cubes of two heights on a matching stone surface, a "
            "soft cool mid-grey seamless background behind. Even diffused light from the front "
            "and slightly above with a gentle cool fill, so no container throws a shadow across "
            "another and every label stays open."),
        frame=(
            "FRAME. Camera slightly above the group, looking gently down so the pyramid reads "
            "clearly. Every product and the tops of the cubes are fully inside the frame with "
            "clear margin above and to both sides; nothing is cut by any edge. Square format. "
            "Sharp focus across every front label, every line legible."),
    ),
    dict(
        id="wet-slate-droplets", requires=dict(),
        arrangement=(
            "ARRANGEMENT. The products stand close together in a loose group, {A} at the back "
            "and slightly higher, {OTHERS} forward and apart at the front, one turned a few "
            "degrees further than the next. Every front label faces the camera and stays fully "
            "legible."),
        scene=(
            "SCENE. A dark blue-grey slate surface, wet, with fine water droplets beaded across "
            "the stone and clinging to the shoulders of the glass. A shallow film of water "
            "around the bases catches a cool reflection. Cool crisp light from the upper left, "
            "slightly harder than studio soft, so each droplet carries a tiny highlight and the "
            "wet stone reads as genuinely wet rather than merely dark. The background is a cool "
            "dark grey falling off gently."),
        frame=(
            "FRAME. Camera low, near the level of the lids, so the wet surface stretches away "
            "beneath the group. Every product is fully inside the frame with clear margin above "
            "and to both sides; nothing is cut by any edge. Square format. Sharp focus across "
            "every front label, every line legible."),
    ),
    dict(
        id="silk-drape-cluster", requires=dict(),
        arrangement=(
            "ARRANGEMENT. An asymmetric cluster rather than a row: {A} standing upright at the "
            "back left, {B} upright and forward at the right. {THIRD_LYING}Every front label "
            "stays readable. "
            "The products do not line up and do not sit at equal spacing. Every front label "
            "stays fully legible."),
        scene=(
            "SCENE. Cool pale grey silk with soft rolling folds, the fabric gathering into "
            "gentle shadowed troughs between and behind the products. A matching pale grey "
            "background out of focus behind. Soft diffused light from the upper right, gentle "
            "enough that the silk's folds read as soft gradients rather than hard creases."),
        frame=(
            "FRAME. Camera slightly above the group at a three-quarter angle. Every product is "
            "fully inside the frame with silk reaching every edge; nothing is cut by any edge. "
            "Square format. Sharp focus across every front label, every line legible."),
    ),
    dict(
        id="hard-shadow-colour-block", requires=dict(),
        arrangement=(
            "ARRANGEMENT. The products are staggered in depth rather than in a line: {A} "
            "nearest the camera at the left, {OTHERS} a clear step further back "
            "and to the right. Every front label faces the camera and stays fully legible."),
        scene=(
            "SCENE. A seamless saturated deep-blue ground and background of one flat colour, no "
            "horizon line visible. Hard directional light from the upper left, like clean "
            "midday sun, throwing long crisp-edged shadows across the ground to the lower "
            "right. No softening, no gradient, no props of any kind - the whole image is the "
            "products, one colour and their hard shadows."),
        frame=(
            "FRAME. Camera at eye level with the group. Every product and the full length of "
            "every shadow is fully inside the frame; nothing is cut by any edge. Square format. "
            "Sharp focus across every front label, every line legible."),
    ),
    dict(
        id="tilted-flatlay", requires=dict(),
        arrangement=(
            "ARRANGEMENT. Overhead. All the products lie flat on the surface on a loose "
            "diagonal running from the lower left to the upper right, each TILTED to a "
            "different angle rather than squared up to the frame, and spaced unevenly. Any jar "
            "lies label-up so its front label reads straight to the camera; any bottle lies on "
            "its side with its front label facing up and its pipette in line with the bottle. "
            "Nothing is parallel to the frame edge. Every front label stays fully legible."),
        scene=(
            "SCENE. A smooth cool pale-grey plaster surface with a faint matte texture, seen "
            "from directly above. Soft broad light from one side laying a short soft shadow "
            "beside each object. Nothing else on the surface - no leaves, no flowers, no "
            "towels, no tools, no scattered props."),
        frame=(
            "FRAME. Camera directly above, looking straight down. Every product is fully inside "
            "the frame with clear plaster margin reaching every edge; nothing is cut by any edge "
            "and nothing touches the frame. Square format. Sharp focus across every label, "
            "every line legible."),
    ),
    dict(
        id="low-hero-plinth", requires=dict(),
        arrangement=(
            "ARRANGEMENT. The products stand shoulder to shoulder in a tight group on one "
            "shared plinth, {A} {LEAD_POS} and {OTHERS} beside it, close enough that "
            "their silhouettes nearly touch. Every front label faces the camera and stays fully "
            "legible."),
        scene=(
            "SCENE. A single dark graphite stone plinth with a crisp square front edge, filling "
            "the lower part of the frame. Behind, a deep cool blue-grey gradient going darker "
            "towards the top. Cool key light from high and slightly left, raking down the front "
            "of the containers, with a cold soft fill from the right. The mood is architectural "
            "and still."),
        frame=(
            "FRAME. Camera LOW, below the level of the plinth top, angled slightly UP at the "
            "group so the products stand against the gradient and read as tall. Every product "
            "is fully inside the frame with clear space above; nothing is cut by any edge, "
            "including the bases. Square format. Sharp focus across every front label, every "
            "line legible."),
    ),
    dict(
        id="stone-shelf-shadow-play", requires=dict(),
        arrangement=(
            "ARRANGEMENT. The products stand well apart in a single row on a long narrow shelf, "
            "with clear space between each one so the shelf reads as sparse rather than "
            "stocked, {A} {LEAD_POS}. Every front label faces the camera and stays fully "
            "legible."),
        scene=(
            "SCENE. A single slim shelf of cool mid-grey honed stone cantilevered from a wall "
            "of the same cool grey microcement, no brackets visible. Hard cold light rakes in "
            "from one side through a window out of frame, throwing long crisp-edged shadows "
            "along the wall behind and a band of bright light across the shelf. No warm tone "
            "anywhere - the light is white-blue and the shadows are cool grey. The only objects "
            "in the picture are the products."),
        frame=(
            "FRAME. Camera square on and close, the shelf running across the frame and the "
            "shadowed wall filling the background. Every product and every one of their wall "
            "shadows is fully inside the frame; nothing is cut by any edge. Square format. "
            "Sharp focus across every front label, every line legible."),
    ),
    dict(
        id="row-contact-shadow", requires=dict(),
        arrangement=(
            "ARRANGEMENT. The products stand in a single straight row on one shared baseline, "
            "evenly spaced with a clear gap of white between each, {A} {LEAD_POS}. Each "
            "carries a SOFT SHORT CONTACT SHADOW directly beneath it, just enough to sit it on "
            "the ground, with no shadow reaching across to the next. Every front label faces "
            "the camera square on and stays fully legible."),
        scene=(
            "SCENE. The background is PURE WHITE, uniform and seamless, edge to edge - the same "
            "white in every corner, with no tone, no tint, no gradient, no texture, no "
            "vignette, no horizon line and no visible surface or backdrop seam anywhere. There "
            "is nothing in the picture but the products. The light is cool and neutral so the "
            "white stays white and the frosted glass keeps its own colour without any warm "
            "cast."),
        frame=(
            "FRAME. Camera straight on at the height of the labels. Every product is fully "
            "inside the frame with generous white margin above, below and to both sides; "
            "nothing is cut by any edge and nothing touches the frame. Square format. Sharp "
            "focus across every front label, every line legible."),
    ),
    dict(
        id="gloss-reflection", requires=dict(),
        arrangement=(
            "ARRANGEMENT. The products stand in a row on a glossy white surface that throws a "
            "soft vertical reflection of each downward beneath it, fading out cleanly within "
            "about a third of that container's own height. The surface itself is the same pure "
            "white as the background, visible only through the reflection. {A} is "
            "{LEAD_POS}. Every front label faces the camera and stays fully legible."),
        scene=(
            "SCENE. The background is PURE WHITE, uniform and seamless, edge to edge, with no "
            "tone, tint, gradient, texture, vignette or horizon line. Nothing is in the picture "
            "but the products and their reflections. Cool neutral light so the white stays "
            "white."),
        frame=(
            "FRAME. Camera straight on, just above the height of the labels. Every product AND "
            "its reflection is fully inside the frame with clear white margin all round; "
            "nothing is cut by any edge. Square format. Sharp focus across every front label, "
            "every line legible."),
    ),
    dict(
        id="oak-shelf-styled", requires=dict(),
        arrangement=(
            "ARRANGEMENT. The products stand together on a light oak floating shelf, grouped a "
            "little right of centre with {A} {LEAD_POS}. To their left on the same shelf "
            "stands a small matte beige ceramic bottle vase holding six slim natural reed "
            "diffuser sticks. To their right, leaning against the wall, a framed print - a "
            "black continuous-line drawing of a female figure on plain white, in a slim black "
            "frame. Every front label faces the camera and stays fully legible."),
        scene=(
            "SCENE. A wall of pale grey plaster with a fine sandy texture, and a light oak "
            "floating shelf with a square front edge and visible straight grain, cantilevered "
            "from it with no brackets. A round mirror with a slim brushed steel rim hangs on "
            "the wall above the shelf, partly in frame. Soft even daylight from the left. Calm, "
            "modern, styled and uncluttered."),
        frame=(
            "FRAME. Camera straight on at shelf height, close enough that the shelf runs across "
            "the lower third and the textured wall fills the upper frame. Every product is "
            "fully inside the frame; nothing is cut by any edge. Square format. Sharp focus "
            "across every front label, every line legible."),
    ),

    # ---- need a cream jar to open -------------------------------------------------
    dict(
        id="open-jar-swatch-model", requires=dict(jars=1),
        arrangement=(
            "ARRANGEMENT. EVERY PRODUCT IN THE BUNDLE IS IN FRAME TOGETHER as a set. {JAR} "
            "stands OPEN and nearest the camera, slightly right of centre and largest in frame, "
            "its front label square to the lens and fully legible; its lid lies flat on the "
            "surface behind and to the left of it, top face up. The other products stand CLOSED "
            "behind it, turned a few degrees inward, their own front labels facing the camera. "
            "On the surface in front of the open jar, a single generous SMEAR of that jar's own "
            "cream has been drawn across the stone with a palette knife, thick at one end and "
            "thinning to a tapered edge. Every front label stays legible."),
        scene=(
            "SCENE. A pale grey-white marble surface with fine soft veining. Behind it, thrown "
            "well out of focus, a bright modern bathroom: a brushed steel soap dispenser at the "
            "left, a small green plant in a white pot behind it, and further back a woman "
            "standing at a mirror with her fingertips at her cheek, so soft she reads as "
            "atmosphere rather than as a subject. Cool clean daylight, bright and airy."),
        frame=(
            "FRAME. Camera low and very close, at the height of the open jar's label. Every "
            "product is fully inside the frame with its whole label visible; nothing is cut by "
            "any edge. Everything behind is strongly out of focus while the open jar, its rim, "
            "the cream inside it and the smear in front are all razor sharp. Square format."),
    ),
    dict(
        id="open-jar-swatch-evening", requires=dict(jars=1),
        arrangement=(
            "ARRANGEMENT. EVERY PRODUCT IN THE BUNDLE IS IN FRAME TOGETHER as a set. {JAR} "
            "stands OPEN and nearest the camera, slightly right of centre and largest in frame, "
            "its front label square to the lens and fully legible; its lid lies flat on the "
            "surface behind and to the left of it, top face up. The other products stand CLOSED "
            "behind it, their own front labels facing the camera. On the surface in front of "
            "the open jar, a single generous SMEAR of that jar's own cream has been drawn "
            "across the stone with a palette knife, thick at one end and thinning to a tapered "
            "edge. Every front label stays legible."),
        scene=(
            "SCENE. A pale grey-white marble surface with fine soft veining. Behind it, thrown "
            "well out of focus, a calm modern bathroom in cooler evening light: a brushed steel "
            "soap dispenser at the left, a small green plant in a white pot behind it, and "
            "further back a woman standing at a mirror with her fingertips at her cheek, so "
            "soft she reads as atmosphere rather than as a subject. Cool, quiet, low-key but "
            "not dark."),
        frame=(
            "FRAME. Camera low and very close, at the height of the open jar's label. Every "
            "product is fully inside the frame with its whole label visible; nothing is cut by "
            "any edge. Everything behind is strongly out of focus while the open jar, its rim, "
            "the cream inside and the smear are razor sharp. Square format."),
    ),
    dict(
        id="open-jar-swatch-clean", requires=dict(jars=1),
        arrangement=(
            "ARRANGEMENT. EVERY PRODUCT IN THE BUNDLE IS IN FRAME TOGETHER as a set. {JAR} "
            "stands OPEN and nearest the camera {LEAD_POS}, largest in frame, its front "
            "label square to the lens and fully legible, its lid lying flat on the surface "
            "behind it. The other products stand CLOSED behind and to either side, their front "
            "labels facing the camera. A single SMEAR of that jar's own cream is drawn across "
            "the stone in front of it, and a second much smaller dab sits apart from it. Every "
            "front label stays legible."),
        scene=(
            "SCENE. A pale grey-white marble surface with fine soft veining, and behind it a "
            "plain bright bathroom wall thrown completely out of focus into a soft pale wash "
            "with no identifiable object in it at all. Cool clean daylight from the left, "
            "bright and airy."),
        frame=(
            "FRAME. Camera low and very close, at the height of the open jar's label. Every "
            "product is fully inside the frame with its whole label visible; nothing is cut by "
            "any edge. The open jar, its rim, the cream inside and the smear are razor sharp "
            "against a completely soft background. Square format."),
    ),

    # ---- needs two cream jars to stack --------------------------------------------
    dict(
        id="two-jar-tower", requires=dict(jars=2),
        arrangement=(
            "ARRANGEMENT. {JAR} and {JAR2} are STACKED ONE DIRECTLY ON TOP OF THE OTHER into a "
            "short tower: {JAR} on the bottom, {JAR2} squarely on top of it, both perfectly "
            "centred and axis-aligned, both front labels facing the camera and both fully "
            "legible. Where one sits on the other, its FLAT BASE rests directly ON the flat top "
            "face of the lid beneath it, the two in full contact with no gap and no visible "
            "support. They stay separate objects with a clear seam between them - never merged "
            "into one tall vessel. Any remaining product stands upright on the surface "
            "immediately beside the tower, close enough to touch it, its own label facing the "
            "camera."),
        scene=(
            "SCENE. A cool mid-grey seamless studio background and a matching matte surface, no "
            "horizon line visible. Soft cool key light from the upper left with a broad fill, "
            "and a single soft shadow pooling beneath the tower. Restrained and cold."),
        frame=(
            "FRAME. Camera straight on at the height of the seam between the two jars. "
            "Everything is fully inside the frame with clear margin above and to both sides; "
            "nothing is cut by any edge. Square format. Sharp focus across every front label, "
            "every line legible."),
    ),
]


def applicable(comp, n_products, n_jars):
    r = comp.get("requires", {})
    return n_products >= r.get("min_products", 2) and n_jars >= r.get("jars", 0)
