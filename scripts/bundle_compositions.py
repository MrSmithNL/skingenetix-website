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
            "SCENE. A seamless saturated {ACCENT} ground and background of one flat colour, no "
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


def applicable(comp, n_products, n_jars, n_bottles=0):
    """Can this composition serve a bundle of this shape?

    `bottles` matters as much as `jars`: the serum bridge lays a BOTTLE across two jars, and
    the Copper Peptide day+night duo is two jars with no bottle at all. Without this the
    builder emitted a brief naming a product the bundle does not contain - caught by the
    unresolved-placeholder guard rather than shipped, but the filter is where it belongs.
    """
    r = comp.get("requires", {})
    return (n_products >= r.get("min_products", 2)
            and n_jars >= r.get("jars", 0)
            and n_bottles >= r.get("bottles", 0))


# ---------------------------------------------------------------------------------------
# EVERYTHING ELSE WE HAVE SHOT, plus new types from the product-photography skill.
#
# Malcolm, 2026-09-12: "add the other shot types to the run - not only the ones that I selected
# for the finals last time. so the run should include all shot types we have created for the
# products so far. See also the 'Create Product Image' skill for other ideas. but only use image
# shot types where you can combine the multiple products in the one shot."
#
# So the selection filter from the Copper run is lifted. The ONE filter that stays is
# multi-product: a composition that can only hold a single item is not a bundle shot. That
# excludes exactly one thing we have shot - the model holding a single open jar with cream on
# her fingertip - and the skill's single-product macros (dropper tip, one lid crop).
#
# {ACCENT} and {ACCENT_PALETTE} resolve per bundle from the products' own label accent rules.
# ---------------------------------------------------------------------------------------
ADDITIONAL = [
    # ---- from batch 2 -----------------------------------------------------------------
    dict(id="black-glass-reflection", requires=dict(),
         arrangement="ARRANGEMENT. The products stand in a shallow arc, {A} a little forward of centre and the others set back and turned a few degrees inward, so the group has depth rather than sitting in a flat line. Every front label faces the camera and stays fully legible.",
         scene="SCENE. A polished black glass surface throwing a clean vertical mirror reflection of each product beneath it, fading to black. The background is deep graphite going to near-black at the corners. Cool rim light from behind and slightly above on both sides draws a bright edge down the flank of each container, with a soft frontal fill just strong enough to keep the labels readable.",
         frame="FRAME. Camera at the height of the labels. Every product AND its reflection is fully inside the frame, with dark margin above and to both sides; nothing is cut by any edge. Square format. Sharp focus across every front label."),
    dict(id="ice-and-glass", requires=dict(),
         arrangement="ARRANGEMENT. The products stand in a shallow group with {A} at the back and the others forward and apart, with clear angular blocks of ice set between and behind them at varying heights, none of the ice covering a label. Every front label faces the camera and stays fully legible.",
         scene="SCENE. A cool white surface with irregular clear ice blocks, some frosted and some glassy, a thin film of meltwater beneath catching a cold reflection. Crisp cool light from behind and above so the ice glows and refracts, with a clean frontal fill keeping the labels open.",
         frame="FRAME. Camera near eye level. Every product is fully inside the frame; nothing is cut by any edge and no ice block obscures any part of any label. Square format. Sharp focus across every front label."),
    dict(id="shallow-depth-cluster", requires=dict(),
         arrangement="ARRANGEMENT. A tight overlapping cluster seen at a three-quarter angle: {A} closest to the camera at the lower left with its front label square to the lens, the others rising behind and to the right, partly overlapped. The group fills much more of the frame than a catalogue shot would.",
         scene="SCENE. A dark cool blue-grey surface and background with no visible horizon, lit by a soft cool key from the upper left and a cold rim from behind the right so the rear product separates from the ground.",
         frame="FRAME. Camera close and at the height of the labels. {A}'s front label is in crisp sharp focus; each product behind it is progressively softer, a real shallow depth of field falling away through the group. Every product stays fully inside the frame. Square format."),
    # ---- from batch 3, the bathroom family --------------------------------------------
    dict(id="microcement-niche", requires=dict(),
         arrangement="ARRANGEMENT. The products stand together inside a shallow rectangular niche recessed into the wall, evenly spaced with a little air between them and above their tops. Every front label faces the camera and stays fully legible.",
         scene="SCENE. A seamless hand-troweled microcement wall in a cool mid-grey with a faint cloudy mottling and no beige, sand or yellow in it. The niche is cut straight into that microcement with soft rounded internal corners, no tile and no trim. A concealed strip light in the top lip washes cool light down the back wall and across the labels. The only objects in the picture are the products.",
         frame="FRAME. Camera square on at the height of the products, close enough that the niche opening fills most of the frame with a margin of plain wall around it. Nothing is cut by any edge. Square format."),
    dict(id="floating-vanity-edge", requires=dict(),
         arrangement="ARRANGEMENT. The products stand in a close group near the front edge of a floating vanity top, {A} slightly behind the others so the group has depth, all turned a few degrees towards the camera. Every front label stays fully legible.",
         scene="SCENE. A floating vanity top of cool pale grey honed limestone with a crisp square front edge and fine even grain, no warm or cream tone. Behind it a plain matte wall of the same cool grey. A slim matte-black wall-mounted spout is visible behind the group, softly out of focus. Cool even daylight from the left.",
         frame="FRAME. Camera low and close, almost level with the vanity top, so the stone edge runs across the bottom of the frame as a sharp horizontal line. Every product is fully inside the frame with clear space above. Square format."),
    dict(id="fluted-glass-backlit", requires=dict(),
         arrangement="ARRANGEMENT. The products stand in a close row directly in front of a fluted glass panel, {A} slightly forward. Every front label faces the camera and stays fully legible.",
         scene="SCENE. A floor-to-ceiling panel of cool clear reeded glass in fine vertical flutes, lit from behind by soft cool daylight so the panel glows pale blue-white and breaks the light into vertical bands. The products stand on a narrow shelf of cool pale grey honed stone. The light through the glass is cold and blue-white, never warm or amber.",
         frame="FRAME. Camera square on and close, the fluted panel filling the background. Every product is fully inside the frame and clear of the edges. The glass behind is softly out of focus while the products stay sharp. Square format."),
    dict(id="basin-rim-droplets", requires=dict(),
         arrangement="ARRANGEMENT. The products stand in a tight group on the stone surround immediately beside the rim of a basin, {A} just behind the others. Every front label faces the camera and stays fully legible.",
         scene="SCENE. A matte white stone basin with a thin square rim, set into a surround of cool mid-grey honed stone with no beige or cream. Fine water droplets are scattered across the stone and a few cling to the shoulders of the glass. A matte-black spout sits above and behind, well out of focus. Cool crisp daylight from the upper left so each droplet carries a small hard highlight.",
         frame="FRAME. Camera close and just above the level of the lids, looking slightly down across the wet stone. Every product is fully inside the frame. Square format."),
    dict(id="backlit-mirror-halo", requires=dict(),
         arrangement="ARRANGEMENT. The products stand in a close group on a narrow ledge directly beneath a round backlit mirror, {A} {LEAD_POS} and the others either side and a little forward. Every front label faces the camera and stays fully legible.",
         scene="SCENE. A round frameless mirror mounted flush to a wall of cool dark grey matte plaster, with a concealed cool-white LED halo behind it throwing a soft ring of cold light onto the wall. That halo is the main light and it is white-blue, never warm. The ledge is a slim slab of cool pale grey stone. The room falls into deep cool shadow at the edges.",
         frame="FRAME. Camera square on and close, the lower arc of the glowing mirror filling the upper frame behind the group. Every product is fully inside the frame. Square format."),
    dict(id="shower-ledge-steam", requires=dict(),
         arrangement="ARRANGEMENT. The products stand in a close row along a built-in shower ledge, evenly spaced with a little air between them, {A} {LEAD_POS}. Every front label faces the camera and stays fully legible.",
         scene="SCENE. A built-in ledge of cool grey honed stone along a wall of large-format matte pale-grey porcelain tiles with very fine grout lines. A faint cool haze of steam drifts across the upper frame and the vertical edge of a frameless glass screen catches a thin cold highlight at one side. Everything is cool and damp.",
         frame="FRAME. Camera square on and close, the ledge running across the frame and the tiled wall filling the background. Every product is fully inside the frame. Square format."),
    dict(id="low-key-dark-stone", requires=dict(),
         arrangement="ARRANGEMENT. The products stand in a tight overlapping group, {A} {LEAD_POS} and slightly forward, the others close beside and a little behind so their shoulders just overlap its flanks. Every front label faces the camera and stays fully legible.",
         scene="SCENE. A near-black honed stone surface and a near-black wall behind, both cool and blue-black rather than brown-black. A single narrow shaft of cold white light falls from high on one side, crossing the front labels and leaving the rest of the frame in deep shadow, with a faint cool bounce lifting the shadowed flanks enough to separate them from the background. Moody, matte, restrained.",
         frame="FRAME. Camera close and level with the labels. Every product is fully inside the frame with dark space above. The shaft of light falls squarely across every front label so each line stays legible. Square format."),
    dict(id="window-sill-daylight", requires=dict(),
         arrangement="ARRANGEMENT. The products stand in a relaxed close group on a deep window sill, unevenly spaced. Every front label faces the camera and stays fully legible.",
         scene="SCENE. A deep sill of cool pale grey honed stone in a reveal of the same cool grey plaster, with soft north daylight so the light is flat, cold and blue-white with no sun patch and no warm cast. A folded edge of pale cool-grey linen lies flat on the sill behind the group. The view beyond the window is blown out to plain soft white.",
         frame="FRAME. Camera close and square on, the sill running across the lower frame and the pale window light filling the background. Every product is fully inside the frame. Square format."),
    dict(id="mirror-doubled", requires=dict(),
         arrangement="ARRANGEMENT. The products stand in a close row directly against a mirror, so each is doubled by its own reflection immediately behind it. {A} is {LEAD_POS}. Every REAL front label faces the camera and stays fully legible.",
         scene="SCENE. A frameless mirror running the full width behind the group, meeting a vanity top of cool pale grey honed stone with no visible trim or joint. Cool even light from the front and slightly above, soft enough that the mirror shows no glare across the labels.",
         frame="FRAME. Camera square on and close, at the height of the labels, positioned so the camera itself does not appear in the mirror. Every product and its reflection is fully inside the frame. Square format."),
    # ---- from batch 4, the hero-white family ------------------------------------------
    dict(id="white-pyramid-silhouette", requires=dict(),
         arrangement="ARRANGEMENT. The products form a clear triangle: {A}, the tallest, {LEAD_POS}, with the others either side and slightly forward so their tops fall well below its shoulder. The outline of the group rises to a single point. A soft contact shadow sits under each. Every front label faces the camera and stays fully legible.",
         scene="SCENE. The background is PURE WHITE, uniform and seamless, edge to edge, with no tone, tint, gradient, texture, vignette or horizon line. Nothing is in the picture but the products. Cool neutral light so the white stays white.",
         frame="FRAME. Camera straight on at the height of the labels. Every product is fully inside the frame with clear white margin above the apex and to both sides. Square format."),
    dict(id="white-overlapping-three-quarter", requires=dict(),
         arrangement="ARRANGEMENT. A tight group seen at a gentle three-quarter angle, the products overlapping rather than standing apart, {A} nearest the camera with its front label square to the lens. One soft shadow pools beneath the whole group. Every front label stays fully legible.",
         scene="SCENE. The background is PURE WHITE, uniform and seamless, edge to edge, no tone, gradient, texture or horizon. Cool neutral light.",
         frame="FRAME. Camera slightly off-axis at the height of the labels. The group sits a little left of centre with more white to the right. Every product is fully inside the frame. Square format."),
    dict(id="white-staggered-depth", requires=dict(),
         arrangement="ARRANGEMENT. The products are staggered in depth rather than in a line: {A} nearest the camera at the left, {OTHERS} a clear step further back and to the right, each sitting slightly higher in the frame as receding objects do. A soft shadow falls beneath each, smaller and fainter the further back it stands. Every front label stays fully legible.",
         scene="SCENE. The background is PURE WHITE, uniform and seamless, edge to edge, no tone, gradient, texture or horizon. Cool neutral light.",
         frame="FRAME. Camera straight on and a little above so the depth reads. Every product is fully inside the frame with clear white margin all round. Square format."),
    dict(id="white-floating-shadowless", requires=dict(),
         arrangement="ARRANGEMENT. The products are presented in a straight row, evenly spaced, with ABSOLUTELY NO SHADOW OF ANY KIND - no contact shadow, no cast shadow, no reflection, and no visible point where any container meets a surface. Each simply sits against the white with clean crisp edges, the way a cut-out product listing image looks. Lighting is flat, even and shadowless from the front with just enough soft modelling to show the glass curve. Every front label faces the camera square on.",
         scene="SCENE. The background is PURE WHITE, uniform and seamless, edge to edge, with nothing in the picture but the products.",
         frame="FRAME. Camera straight on at the height of the labels. Every product is fully inside the frame with generous even white margin on every side. Square format."),
    dict(id="white-single-long-shadow", requires=dict(),
         arrangement="ARRANGEMENT. The products stand in a close row lit by one clean directional light from the upper left, so each casts a SINGLE LONG SOFT-EDGED SHADOW away to the lower right. The shadows run parallel and do not cross the containers. {A} is {LEAD_POS}. Every front label stays fully legible and open, not lost in shade.",
         scene="SCENE. The background is PURE WHITE, uniform and seamless, edge to edge. Nothing in the picture but the products and their shadows.",
         frame="FRAME. Camera straight on at the height of the labels, framed so the full length of every shadow is visible. Everything is fully inside the frame. Square format."),
    dict(id="white-lead-forward", requires=dict(),
         arrangement="ARRANGEMENT. {A} stands alone at the front and centre, closest to the camera and clearly the hero, reading slightly larger because it is nearer. {OTHERS} sit behind and well apart to either side, far enough out that {A} overlaps neither. A soft contact shadow sits under each. Every front label faces the camera and stays fully legible.",
         scene="SCENE. The background is PURE WHITE, uniform and seamless, edge to edge, with nothing else in the picture.",
         frame="FRAME. Camera straight on at the height of {A}'s label. Every product is fully inside the frame with clear white margin all round. Square format."),
    dict(id="white-airy-wide-spacing", requires=dict(),
         arrangement="ARRANGEMENT. The products stand in a single row spaced WIDE APART, with a broad band of clean white between each so the picture reads spare and unhurried rather than as a stocked shelf. The gap between neighbours is roughly the width of a container. A soft short contact shadow sits under each. Every front label faces the camera square on.",
         scene="SCENE. The background is PURE WHITE, uniform and seamless, edge to edge, nothing else in the picture.",
         frame="FRAME. Camera straight on at the height of the labels, framed wide so the white dominates and the products occupy a band across the middle. Everything fully inside the frame. Square format."),
    dict(id="white-elevated-compact", requires=dict(),
         arrangement="ARRANGEMENT. A compact group seen from slightly above, close together, {A} {LEAD_POS}, so the tops of any lids are just visible as shallow silver ellipses. A soft shadow pools beneath the group. Every front label is still turned up towards the camera and stays fully legible.",
         scene="SCENE. The background is PURE WHITE, uniform and seamless, edge to edge, nothing else in the picture.",
         frame="FRAME. Camera above the group looking gently down, high enough to show the lid tops and low enough that the front labels are not foreshortened into illegibility. Everything fully inside the frame. Square format."),
    # ---- from batch 5 / 6 --------------------------------------------------------------
    dict(id="oak-shelf-wider-room", requires=dict(),
         arrangement="ARRANGEMENT. The products stand together on a light oak floating shelf, small in the frame and about a third of the way in from the left, with a beige ceramic reed diffuser beside them and a framed black-line figure drawing leaning at the right. Every front label faces the camera and stays legible despite their size in frame.",
         scene="SCENE. A wider view of a calm modern bathroom: pale grey textured plaster walls, the light oak shelf, a round steel-rimmed mirror above it, and to one side a walk-in shower with a slim steel rain head and a frameless glass screen, all softly out of focus. Cool bright daylight.",
         frame="FRAME. Camera straight on, further back than a product shot, so the room reads and the shelf sits in the middle distance. The products stay sharp while the room falls gently out of focus. Everything fully inside the frame. Square format."),
    dict(id="precarious-offset-stack", requires=dict(jars=2),
         arrangement="ARRANGEMENT. {JAR} and {JAR2} are STACKED, {JAR} on the bottom, but the upper jar is ROTATED about thirty degrees around the vertical axis and pushed slightly off centre, so the tower reads deliberately, elegantly precarious rather than neatly squared up. Its FLAT BASE still rests directly ON the lid beneath it, in full contact, no gap, no visible support, the two staying separate objects with a clear seam. Both front labels stay fully legible. Any remaining product stands upright a little apart, straight and square.",
         scene="SCENE. A cool pale-grey seamless background and matching surface. ONE hard directional light from the upper left, so the tower throws a single long crisp-edged shadow to the lower right and the offset reads in that shadow too. Graphic and spare.",
         frame="FRAME. Camera straight on, slightly below the seam so the tower reads tall. The tower, any other product and the full shadow are fully inside the frame. Square format."),
    dict(id="three-tier-tower", requires=dict(min_products=3, jars=2, bottles=1),
         arrangement="ARRANGEMENT. All three products form ONE TOWER of three tiers: {JAR} on the bottom, {JAR2} squarely on top of it, and {BOTTLE} standing upright and centred on top. All three are axis-aligned. Where one sits on another its FLAT BASE rests directly ON the lid beneath, in full contact, no gap and no visible support; they stay separate objects with a clear seam and never merge into one vessel. Every front label faces the camera and stays fully legible.",
         scene="SCENE. A deep cool graphite background falling to near-black at the corners, and a dark matte surface beneath. Cool rim light from behind on both sides draws a bright edge down the flank of every tier, with a soft frontal fill keeping every label readable. Monumental and quiet.",
         frame="FRAME. Camera LOW, below the base of the tower, angled slightly UP. The whole tower from base to top is fully inside the frame with clear dark space above, and the BASE of the bottom product is not cut by the lower edge. Square format."),
    dict(id="levitating-column", requires=dict(),
         arrangement="ARRANGEMENT. The products FLOAT in a vertical column, one above the other with a clear gap of empty air between each, all level and axis-aligned as though a tower had been gently pulled apart. NOTHING supports them: no rod, no wire, no stand, no hand, no visible join. Every front label faces the camera and stays fully legible.",
         scene="SCENE. A soft cool pale-grey gradient background, lighter at the centre and falling away at the corners, with no horizon and no surface. A single soft elliptical shadow lies on the empty ground far below the lowest product, small and diffuse, so the height reads. Cool even light from the front.",
         frame="FRAME. Camera straight on at the height of the middle object. Every product and the ground shadow is fully inside the frame with clear margin top and bottom. Square format."),
    dict(id="tumbled-pile", requires=dict(),
         arrangement="ARRANGEMENT. The products are PILED loosely on each other, as if set down in a heap rather than arranged: one lies on its side at the bottom with its front label turned up, another rests ON it tilted at an angle and also label-up, and any third lies across them both. The pile is relaxed and slightly untidy, nothing is level, and every front label is still turned enough to be fully legible.",
         scene="SCENE. A cool pale-grey matte surface and a soft cool grey background, out of focus. Soft directional light from the upper left, the shadows between the piled containers left soft rather than crushed.",
         frame="FRAME. Camera above the pile at a three-quarter angle, looking down across it. Every product is fully inside the frame with clear surface visible around the pile. Square format."),
    dict(id="serum-bridge", requires=dict(jars=2, bottles=1),
         arrangement="ARRANGEMENT. {JAR} and {JAR2} stand upright and apart, a little further apart than the length of {BOTTLE}. {BOTTLE} LIES HORIZONTALLY ACROSS THE TOP OF BOTH, spanning the gap like a lintel, its base resting on one lid and its shoulder on the other, its front label turned up and towards the camera so it stays fully legible. Together they make a simple bridge shape with a clear opening beneath it.",
         scene="SCENE. A cool mid-grey seamless background and matching matte surface. Even cool light from the front and slightly above, with soft shadows under each jar and a gentle shadow cast into the opening beneath the bridge. Architectural and calm.",
         frame="FRAME. Camera straight on at the height of the jar lids, level with the span. Everything is fully inside the frame with clear margin above the bridge. Square format."),
    # ---- new, from the product-photography skill ---------------------------------------
    dict(id="brand-gradient-glow", requires=dict(),
         arrangement="ARRANGEMENT. The products stand together in a close group, {A} {LEAD_POS}, turned a few degrees towards the camera, with generous empty space above them. Every front label faces the camera and stays fully legible.",
         scene="SCENE. A smooth brand gradient background running from {ACCENT} at the base to a deeper, darker version of the same colour at the top, with a soft accent glow of that colour blooming softly behind the group. Rim light on both sides draws a clean bright edge down each container. The palette is {ACCENT_PALETTE}. Premium, campaign-grade, nothing else in frame.",
         frame="FRAME. Camera straight on at the height of the labels, framed with generous negative space above the group. Every product is fully inside the frame. Square format."),
    dict(id="colourblock-two-tone", requires=dict(),
         arrangement="ARRANGEMENT. The products stand in a row on the dividing line of a hard two-tone ground, so the lower half of the frame is one colour and the upper half another, the line running straight behind them. {A} is {LEAD_POS}. Every front label faces the camera and stays fully legible.",
         scene="SCENE. A hard-edged two-tone set: the lower band a saturated {ACCENT} and the upper band a clean pale neutral, meeting in a crisp straight horizontal with no gradient or blur at the join. Even frontal light, graphic and flat, no props. The palette is {ACCENT_PALETTE}.",
         frame="FRAME. Camera straight on at the height of the labels, the tone division running horizontally behind the group. Every product is fully inside the frame. Square format."),
    dict(id="water-ripple-scene", requires=dict(),
         arrangement="ARRANGEMENT. The products stand in shallow still water, close together, {A} {LEAD_POS}, with gentle concentric ripples spreading around their bases. The water rises only a centimetre or two up each container, well below every label. Every front label faces the camera, stays completely dry and stays fully legible.",
         scene="SCENE. A shallow pool of clear still water over a cool dark surface, with soft concentric ripples and a clean mirrored reflection of each container in the water. Cool directional light from above and slightly left, catching the ripple crests. The palette is {ACCENT_PALETTE}.",
         frame="FRAME. Camera low, just above the waterline, so the ripples spread away towards the viewer. Every product and its reflection is fully inside the frame; no label is touched by water. Square format."),
    dict(id="overhead-water-colourblock", requires=dict(),
         arrangement="ARRANGEMENT. Overhead. The products lie on their sides in very shallow coloured water, arranged on a loose diagonal and spaced unevenly, each with its front label turned up to the camera and clear of the water. Gentle ripples spread around them.",
         scene="SCENE. A shallow bath of {ACCENT} water seen from directly above, the colour even and saturated, with soft concentric ripples and a few scattered bubbles. Cool even light from above. The palette is {ACCENT_PALETTE}.",
         frame="FRAME. Camera directly above, looking straight down. Every product is fully inside the frame with coloured water reaching every edge; nothing is cut and no label is submerged. Square format."),
    dict(id="ingredient-hero", requires=dict(),
         arrangement="ARRANGEMENT. The products stand together in a close group at the centre, clearly the hero of the picture, with two or three raw ingredient elements arranged low around their bases - a few translucent gel droplets, a scatter of fine mineral crystals and a single smooth pale stone. Nothing overlaps or obscures any label, and the ingredients stay below the label line. Every front label faces the camera and stays fully legible.",
         scene="SCENE. A dark cool graphite ground with a soft pool of light on the group and the corners falling away. Moody three-point lighting, the ingredients catching a dewy highlight so they read alive rather than dry. A restrained {ACCENT} glow sits behind the group. The palette is {ACCENT_PALETTE}. No botanicals, no leaves, no flowers.",
         frame="FRAME. Camera slightly above the group. Every product is fully inside the frame and remains the dominant subject; the ingredients are supporting detail, never larger than a container. Square format."),
    dict(id="natural-surface-lifestyle", requires=dict(),
         arrangement="ARRANGEMENT. The products stand grouped a little off-centre on a natural stone surface, {A} {LEAD_POS}, with a folded edge of pale linen behind them and nothing else. Every front label faces the camera and stays fully legible.",
         scene="SCENE. A pale grey-white marble surface with soft natural veining, lit by a large soft window from one side so the light is directional but gentle, with a long soft shadow falling away from the group. A folded edge of pale grey-white linen lies behind. Calm, curated, minimal. The palette is {ACCENT_PALETTE}.",
         frame="FRAME. Camera slightly above at a gentle three-quarter angle, the group off-centre with clean surface to one side. Every product is fully inside the frame. Square format."),
    dict(id="packaging-macro-group", requires=dict(),
         arrangement="ARRANGEMENT. A very close view of the products standing shoulder to shoulder and almost touching, filling the frame so the frosted glass grain, the printed type and the brushed metal collars dominate. Each container is COMPLETE from side to side with its whole front label visible and nothing cut off at the left or right - close, but not cropped through any lettering. Every label line is sharp and fully legible.",
         scene="SCENE. Raking side light at a shallow angle across the frosted glass so the grain and the slight relief of the printing read, with a controlled specular strip on each metal collar. A cool dark ground falls away behind. The palette is {ACCENT_PALETTE}.",
         frame="FRAME. Camera very close and square on at label height, framed tight enough that the group fills nearly the whole picture with only a narrow margin of ground around it. Every product is fully inside the frame - nothing is cut by any edge. Square format. Every line of every label razor sharp."),
    dict(id="floating-droplet-spheres", requires=dict(),
         arrangement="ARRANGEMENT. The products stand in a close group, {A} {LEAD_POS}, with a sparse scatter of translucent liquid spheres suspended in the air around and between them at varying distances and sizes. The spheres are few and calm, never a dense cloud, and none covers a label. Every front label faces the camera and stays fully legible.",
         scene="SCENE. A smooth cool gradient background in {ACCENT_PALETTE}, darker at the corners. Cool backlight catching each suspended sphere so it glows and refracts, with a soft frontal fill keeping the labels open.",
         frame="FRAME. Camera straight on at the height of the labels. Every product is fully inside the frame; the spheres may sit anywhere but never obscure lettering. Square format."),
    dict(id="velvet-campaign", requires=dict(),
         arrangement="ARRANGEMENT. The products stand together on deep folded velvet, {A} {LEAD_POS}, close enough to read as a gift set. Every front label faces the camera and stays fully legible.",
         scene="SCENE. Deep {ACCENT} velvet, softly folded and falling away into shadow at the edges, its pile catching the light differently where it turns. Soft directional key from the upper left with a cool rim behind, and a scatter of gentle out-of-focus bokeh points in the far background. Rich and quiet. The palette is {ACCENT_PALETTE}.",
         frame="FRAME. Camera slightly above at a gentle three-quarter angle. Every product is fully inside the frame with folded velvet reaching every edge. Square format."),
    # ---- model, with the whole set in shot ---------------------------------------------
    dict(id="model-holding-set", requires=dict(), model=True,
         arrangement="ARRANGEMENT. {MODEL_HOLD} Every front label faces the camera square on and stays fully legible, and her fingers cover no lettering. She looks towards the camera, calm and at ease.",
         scene="SCENE. A calm modern bathroom thrown gently out of focus behind her: pale grey textured plaster and a round steel-rimmed mirror. Soft cool daylight from the left, even across her face and every product.",
         frame="FRAME. Camera at her chest height, framed from mid-chest to just above her head. Every product and her whole head are fully inside the frame; nothing is cut by any edge. Products and her eyes are sharp. Square format."),
    dict(id="model-vanity-set", requires=dict(), model=True,
         arrangement="ARRANGEMENT. The model stands behind a vanity top on which ALL the products stand side by side in the near foreground, closed, every front label square to the camera and fully legible. She rests one hand lightly on the counter beside them and looks down towards them. She is behind and above them, softer than they are.",
         scene="SCENE. A calm modern bathroom: a pale grey stone vanity top, pale grey textured plaster behind, a round steel-rimmed mirror on the wall. Soft cool daylight from the left. Bright and uncluttered.",
         frame="FRAME. Camera at counter height looking slightly up past the products to her. Every product is fully inside the frame and fully sharp in the foreground; she is behind them from the waist up, gently out of focus, her head fully inside the frame. Square format."),
]

COMPOSITIONS = COMPOSITIONS + ADDITIONAL
