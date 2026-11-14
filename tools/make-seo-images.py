from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

NOTO = '/usr/share/fonts/truetype/noto/'
SERIF_B = NOTO + 'NotoSerifBengali-Bold.ttf'
SANS_B = NOTO + 'NotoSansBengali-Bold.ttf'
SANS_R = NOTO + 'NotoSansBengali-Regular.ttf'
DEJAVU_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def font(path, size):
    return ImageFont.truetype(path, size)

def fit_font(draw, text, path, start_size, max_w, min_size=20):
    size = start_size
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return font(path, min_size)


def is_bn(ch):
    o = ord(ch)
    return 0x0980 <= o <= 0x09FF

def runs(text):
    """Split text into (is_bengali, segment) runs; spaces join the preceding run."""
    out = []
    cur_bn = None
    cur = ''
    for ch in text:
        b = is_bn(ch) if ch != ' ' else cur_bn
        if cur_bn is None:
            cur_bn = b
        if b == cur_bn:
            cur += ch
        else:
            out.append((cur_bn, cur))
            cur_bn = b
            cur = ch
    if cur:
        out.append((cur_bn, cur))
    return out

def mixed_width(draw, text, f_bn, f_lat):
    return sum(draw.textlength(seg, font=(f_bn if bn else f_lat)) for bn, seg in runs(text))

def draw_mixed(draw, xy, text, f_bn, f_lat, fill):
    x, y = xy
    for bn, seg in runs(text):
        f = f_bn if bn else f_lat
        draw.text((x, y), seg, font=f, fill=fill)
        x += draw.textlength(seg, font=f)
    return x

def fit_mixed(draw, text, path_bn, path_lat, start_size, max_w, min_size=20):
    size = start_size
    while size > min_size:
        f_bn = font(path_bn, size)
        f_lat = font(path_lat, size)
        if mixed_width(draw, text, f_bn, f_lat) <= max_w:
            return f_bn, f_lat
        size -= 2
    return font(path_bn, min_size), font(path_lat, min_size)

# ---------- OG image 1200x630 ----------
W, H = 1200, 630
yy, xx = np.mgrid[0:H, 0:W]
t = (xx / W * 0.55 + yy / H * 0.45)
top = np.array([11, 30, 51], dtype=float)
bot = np.array([29, 78, 137], dtype=float)
arr = (top[None, None, :] * (1 - t[..., None]) + bot[None, None, :] * t[..., None]).astype('uint8')
img = Image.fromarray(arr, 'RGB').convert('RGBA')

# soft amber glow, top-right
glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([760, -160, 1340, 320], fill=(251, 191, 36, 55))
gd.ellipse([-220, 420, 320, 820], fill=(74, 124, 89, 45))
glow = glow.filter(ImageFilter.GaussianBlur(60))
img = Image.alpha_composite(img, glow)
d = ImageDraw.Draw(img)

AMBER = (251, 191, 36)
AMBER_L = (252, 211, 77)
WHITE = (255, 255, 255)
WHITE85 = (255, 255, 255, 217)

# faint giant SSC watermark, right side
wm = Image.new('RGBA', (W, H), (0, 0, 0, 0))
wd = ImageDraw.Draw(wm)
f_wm = font(DEJAVU_B, 300)
wd.text((860, 120), 'SSC', font=f_wm, fill=(255, 255, 255, 22))
wm = wm.filter(ImageFilter.GaussianBlur(2))
img = Image.alpha_composite(img, wm)
d = ImageDraw.Draw(img)

# title
f_title_bn, f_title_lat = fit_mixed(d, 'BOU SSC ২য় বর্ষ', SERIF_B, DEJAVU_B, 96, 1040)
draw_mixed(d, (80, 200), 'BOU SSC ২য় বর্ষ', f_title_bn, f_title_lat, WHITE)
# amber underline bar
d.rounded_rectangle([82, 315, 330, 327], radius=6, fill=AMBER)

# second line
f_sub_bn, f_sub_lat = fit_mixed(d, 'নোট  •  MCQ  •  ই-বুক', SANS_B, DEJAVU_B, 56, 1040)
draw_mixed(d, (80, 345), 'নোট  •  MCQ  •  ই-বুক', f_sub_bn, f_sub_lat, AMBER_L)

# stats
f_st_bn, f_st_lat = fit_mixed(d, '১৩টি বিষয়   •   ১৬৬টি Unit   •   ৬৬৪টি MCQ   •   ১৬৬টি ইনফোগ্রাফিক', SANS_B, DEJAVU_B, 34, 1040)
draw_mixed(d, (80, 420), '১৩টি বিষয়   •   ১৬৬টি Unit   •   ৬৬৪টি MCQ   •   ১৬৬টি ইনফোগ্রাফিক', f_st_bn, f_st_lat, WHITE85)

# divider + footer
d.line([80, 505, 1120, 505], fill=(255, 255, 255, 70), width=2)
f_ft_bn, f_ft_lat = fit_mixed(d, 'সম্পূর্ণ ফ্রি  •  bisnu-ssc-notes.vercel.app', SANS_B, DEJAVU_B, 30, 1040)
draw_mixed(d, (80, 528), 'সম্পূর্ণ ফ্রি  •  bisnu-ssc-notes.vercel.app', f_ft_bn, f_ft_lat, WHITE)
f_by = font(SANS_R, 28)
draw_mixed(d, (80, 570), 'তৈরি করেছেন: বিষ্ণু কুন্ডু', f_by, f_by, (255, 255, 255, 200))

img.convert('RGB').save('og-image.png', 'PNG')
print('og-image.png saved')

# ---------- Favicon 512x512 ----------
S = 512
fav = Image.new('RGBA', (S, S), (0, 0, 0, 0))
fd = ImageDraw.Draw(fav)
fd.rounded_rectangle([8, 8, S - 8, S - 8], radius=110, fill=(11, 30, 51, 255))
fd.rounded_rectangle([8, 8, S - 8, S - 8], radius=110, outline=(251, 191, 36, 255), width=10)
f_mono = font(SERIF_B, 300)
bbox = fd.textbbox((0, 0), 'ব', font=f_mono)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
fd.text(((S - tw) / 2 - bbox[0], (S - th) / 2 - bbox[1] - 14), 'ব', font=f_mono, fill=(251, 191, 36, 255))
fav.save('favicon.png', 'PNG')
print('favicon.png saved')

import os
print('og-image:', os.path.getsize('og-image.png'), 'bytes')
print('favicon:', os.path.getsize('favicon.png'), 'bytes')
