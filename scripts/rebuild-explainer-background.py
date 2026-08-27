"""Rebuild the causes frame's background: a smooth even field taken from the approach
frame's own fitted model, with the approach frame's REAL cast shadow transplanted under the
causes plate.

Deterministic. A plain background is retouched with arithmetic, never a masked AI edit.

Two variants are written so the choice happens in one round:
  A  smooth field + the cast shadow (matches the approach frame, which has one)
  B  smooth field only, no shadow at all (most literal reading of "even colour")
"""
import numpy as np
from PIL import Image
from scipy import ndimage

D = '/Users/malcolmsmith/Claude Code/Projects/skingenetix-website/assets/publish-ready/page-fine-lines-explainers/'
O = '/private/tmp/claude-501/-Users-malcolmsmith-Claude-Code-Projects-skingenetix-website/59d16b70-efc6-48c3-93d2-3fafe588e0a6/scratchpad/'
CAUSES = D + 'skingenetix-fine-lines-wrinkles-collagen-elastin-damage-cross-section.jpg'
APPROACH = D + 'skingenetix-peptide-approach-wrinkle-reduction-collagen-matrix-diagram.jpg'


def structure_mask(rgb, thr=0.035, close=25, dil=0):
    g = rgb.mean(2)
    gx = ndimage.sobel(g, 0); gy = ndimage.sobel(g, 1)
    edge = ndimage.gaussian_filter(np.hypot(gx, gy), 6)
    m = edge > edge.max() * thr
    m = ndimage.binary_closing(m, np.ones((close, close)))
    m = ndimage.binary_fill_holes(m)
    lbl, n = ndimage.label(m)
    if n:
        sizes = ndimage.sum(m, lbl, range(1, n + 1))
        m = lbl == (np.argmax(sizes) + 1)
    m = ndimage.binary_fill_holes(m)
    if dil:
        m = ndimage.binary_dilation(m, np.ones((dil, dil)))
    return m


def plate_geometry(mask):
    """The glass plate is the WIDEST part of the object. Taking the bottom-most row
    instead picked up a 120px sliver where the mask leaked into the cast shadow, which
    made the x-scale 12x. Search the lower half of the object for the widest row."""
    rows = np.where(mask.any(1))[0]
    y0, y1 = rows.min(), rows.max()
    lo = y0 + int((y1 - y0) * 0.55)
    widths = mask[lo:y1 + 1].sum(1)
    y_plate = lo + int(np.argmax(widths))
    cols = np.where(mask[y_plate])[0]
    # bottom of the plate = last row still at least 80% of the plate width
    wmax = widths.max()
    tail = np.where(mask[y_plate:y1 + 1].sum(1) >= 0.80 * wmax)[0]
    y_bot = y_plate + (tail.max() if len(tail) else 0)
    return y_bot, cols.min(), cols.max()


ap = np.asarray(Image.open(APPROACH).convert('RGB'), dtype=np.float64)
ca = np.asarray(Image.open(CAUSES).convert('RGB'), dtype=np.float64)
h, w, _ = ca.shape

fit_ap = np.load(O + 'fit_ap.npy')
shadow_ap = np.load(O + 'shadow_ap.npy')
sub_ap = np.load(O + 'sub_ap.npy')

sub_ca = structure_mask(ca)

ay, ax0, ax1 = plate_geometry(sub_ap)
cy, cx0, cx1 = plate_geometry(sub_ca)
print('approach plate: bottom y=%d  x %d..%d  (w=%d)' % (ay, ax0, ax1, ax1 - ax0))
print('causes   plate: bottom y=%d  x %d..%d  (w=%d)' % (cy, cx0, cx1, cx1 - cx0))

# --- move the approach shadow so it sits under the causes plate -----------------
sx_scale = (cx1 - cx0) / float(ax1 - ax0)
acx, ccx = (ax0 + ax1) / 2.0, (cx0 + cx1) / 2.0
print('shadow transplant: x-scale %.3f, centre %.0f -> %.0f, bottom %d -> %d' % (sx_scale, acx, ccx, ay, cy))

yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)

# Window the source shadow to the region that is genuinely the cast shadow, feathered to
# nothing at its borders. Without this the warp carries hard edges: the mask leak and the
# constant fill outside the source both land as straight lines in the result.
sy, sx = np.mgrid[0:h, 0:w].astype(np.float64)
def ramp(v, a, b):
    return np.clip((v - a) / float(b - a), 0, 1)
win = (ramp(sy, ay - 30, ay + 90)                      # nothing above the plate bottom
       * (1 - ramp(sy, ay + 520, ay + 760))            # fades out below
       * ramp(sx, ax0 - 300, ax0 - 40)                 # fades in left of the plate
       * (1 - ramp(sx, ax1 + 40, ax1 + 320)))          # fades out right of the plate
win = ndimage.gaussian_filter(win, 25)
shadow_src = 1.0 - (1.0 - shadow_ap) * win
print('windowed shadow: min %.3f  (raw min was %.3f)' % (shadow_src.min(), shadow_ap.min()))

src_x = (xx - ccx) / sx_scale + acx
src_y = (yy - cy) + ay
shadow_ca = ndimage.map_coordinates(shadow_src, [src_y, src_x], order=1, mode='constant', cval=1.0)
# an isolated BRIGHT hole survives inside the wedge where the approach mask leaked into
# its own shadow; a grey opening removes small bright details and leaves the wedge intact
shadow_ca = ndimage.grey_opening(shadow_ca, size=55)
# a hard top edge and a blocky right end made this read as a slab rather than a cast
# shadow; the wide blur is what turns it back into light falling off
shadow_ca = np.clip(ndimage.gaussian_filter(shadow_ca, 45), 0.0, 1.0)

from PIL import Image as _I
_v=((shadow_ca-shadow_ca.min())/(1-shadow_ca.min()+1e-6)*255).astype('uint8')
_I.fromarray(_v).resize((760,760)).save(O+'dbg-shadow-ca.png')
print('shadow_ca: min %.3f  frac<0.98 %.2f%%' % (shadow_ca.min(), (shadow_ca<0.98).mean()*100))

# --- smooth even field ----------------------------------------------------------
field = fit_ap.copy()

# --- feathered subject alpha ----------------------------------------------------
# The structure mask includes the bright halo ring that hugs the block, because the halo
# has a gradient too. Left in, that ring survives as a white fringe against the new field.
# Erode until the mask stops at the block's real edge, and check the erosion has not eaten
# into the block itself rather than assuming it.
ERODE = 13
core = ndimage.binary_erosion(sub_ca, np.ones((ERODE, ERODE)))
rows = np.where(sub_ca.any(1))[0]; cols = np.where(sub_ca.any(0))[0]
rows2 = np.where(core.any(1))[0]; cols2 = np.where(core.any(0))[0]
print('mask erosion %dpx: bbox x %d..%d -> %d..%d   y %d..%d -> %d..%d'
      % (ERODE, cols.min(), cols.max(), cols2.min(), cols2.max(),
         rows.min(), rows.max(), rows2.min(), rows2.max()))
alpha = ndimage.gaussian_filter(core.astype(np.float64), 2.0)
alpha = np.clip((alpha - 0.35) / 0.30, 0, 1)[:, :, None]


def compose(with_shadow):
    bg = field * (shadow_ca[:, :, None] if with_shadow else 1.0)
    out = ca * alpha + bg * (1 - alpha)
    return np.clip(out, 0, 255).astype(np.uint8)


for tag, ws in [('A-shadow', True), ('B-flat', False)]:
    img = compose(ws)
    Image.fromarray(img).save(O + f'rebuilt-{tag}.png')
    bgm = ~ndimage.binary_dilation(sub_ca, np.ones((25, 25)))
    L = img.astype(float).mean(2)
    print(f'{tag}: background L sd {L[bgm].std():.2f}  (original was 20.87)')

print('done')
