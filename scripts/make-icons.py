"""Draws the app icon (a rosewood fretboard with a root/third/fifth chord shape) into docs/.

Run: python3 scripts/make-icons.py
"""
from PIL import Image, ImageDraw, ImageFilter
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'docs')
S = 1024  # draw large, then downsample for smooth edges

WOOD_TOP, WOOD_BOTTOM = (70, 44, 29), (36, 22, 14)
FRET, NUT, STRING_PLAIN, STRING_WOUND = (201, 205, 211), (236, 227, 204), (228, 231, 235), (214, 180, 124)
ROOT, THIRD, FIFTH, PEARL = (214, 69, 80), (226, 160, 18), (52, 125, 205), (245, 239, 224)


def fretboard(size, inset):
    """Fretboard art filling the square, with the motif kept inside `inset` (0..0.5) of each edge."""
    img = Image.new('RGB', (size, size))
    d = ImageDraw.Draw(img)
    for y in range(size):  # wood gradient
        t = y / (size - 1)
        d.line([(0, y), (size, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(WOOD_TOP, WOOD_BOTTOM)))
    lo, hi = size * inset, size * (1 - inset)
    span = hi - lo
    strings = [lo + span * (0.08 + i * 0.84 / 3) for i in range(4)]
    frets = [lo + span * (0.10 + i * 0.80 / 3) for i in range(4)]
    # nut on the left edge of the motif, frets after it
    d.rectangle([frets[0] - size * 0.022, 0, frets[0] + size * 0.006, size], fill=NUT)
    for x in frets[1:]:
        d.rectangle([x - size * 0.008, 0, x + size * 0.008, size], fill=FRET)
    for i, y in enumerate(strings):
        w = size * (0.006 + 0.003 * i)
        d.rectangle([0, y - w, size, y + w], fill=STRING_PLAIN if i < 2 else STRING_WOUND)
    # a pearl inlay between the 2nd and 3rd frets
    cx, cy, r = (frets[1] + frets[2]) / 2, (strings[1] + strings[2]) / 2, size * 0.035
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=tuple(round(c * 0.55 + w * 0.45) for c, w in zip(PEARL, WOOD_TOP)))
    # chord shape: fifth, third, root on three strings
    dot = size * 0.085
    for (fi, si, col) in [(2, 0, FIFTH), (1, 1, THIRD), (2, 3, ROOT)]:
        x = (frets[fi - 1] + frets[fi]) / 2 if fi > 0 else frets[0]
        y = strings[si]
        d.ellipse([x - dot - size * 0.012, y - dot - size * 0.012, x + dot + size * 0.012, y + dot + size * 0.012], fill=(255, 255, 255))
        d.ellipse([x - dot, y - dot, x + dot, y + dot], fill=col)
    return img


def save(img, name, px):
    img.resize((px, px), Image.LANCZOS).save(os.path.join(OUT, name), optimize=True)


os.makedirs(OUT, exist_ok=True)
regular = fretboard(S, 0.08)
# Rounded corners for the regular icon (browsers/launchers that don't mask)
mask = Image.new('L', (S, S), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=S * 0.2, fill=255)
rounded = Image.new('RGBA', (S, S))
rounded.paste(regular, (0, 0), mask)
save(rounded, 'icon-192.png', 192)
save(rounded, 'icon-512.png', 512)
# Maskable: full bleed, motif inside the central 80% safe zone
save(fretboard(S, 0.2), 'icon-maskable-512.png', 512)
# iOS home-screen icon: square, iOS rounds it itself
save(regular, 'icon-180.png', 180)
print('icons written to docs/')
