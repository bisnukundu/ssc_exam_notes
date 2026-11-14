#!/usr/bin/env python3
"""Generate static SEO pages for the BOU SSC Notes site.

Reads the verified notes JSON (db/notes-<code>.json) and the official
catalogue (db/ssc-2nd-year-new-version.json) and builds:
  - subjects/<code>-<slug>.html          (13 subject pages)
  - subjects/<code>/unit-<n>-<slug>.html (166 unit pages)
  - sitemap.xml (homepage + all 179 pages)

The SPA (index.html) keeps working as-is; static pages link back into it
via deep-links (/#s=<code> and /#s=<code>&u=<n>).

Rules (from the project skill):
  - Only verified facts: marks shown ONLY when the catalogue has a
    verified marks.total (2651, 2652). All other subjects: no marks.
  - Only 2651 Unit 1's 4 MCQs are the book's own; every other unit's
    questions are labelled Practice.
  - Bengali rendered from the notes JSON only; slugs are Latin
    transliterations (identifiers only — titles/meta carry the keywords).
"""
import html
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://bisnu-ssc-notes.vercel.app"
TODAY = "2026-11-14"

# ---------------------------------------------------------------- data ---
CATALOGUE = json.loads((ROOT / "db" / "ssc-2nd-year-new-version.json").read_text(encoding="utf-8"))
SUBJECTS = {s["code"]: s for s in CATALOGUE["subjects"]}

NOTES = {}
for code in SUBJECTS:
    NOTES[code] = json.loads((ROOT / "db" / f"notes-{code}.json").read_text(encoding="utf-8"))

# Hand-written subject slugs (official names, short + searchable).
SUBJECT_SLUGS = {
    "2651": "bangla-dwitiyo-potro",
    "2652": "english-second-paper",
    "2669": "sharirik-shikkha",
    "2671": "orthoniti",
    "2672": "pouroniti-o-nagorikota",
    "2673": "biggan",
    "2676": "finance-o-banking",
    "2679": "jibbiggan",
    "2680": "ucchotoro-gonit",
    "2681": "bangladesh-o-bishwoporichoy",
    "2685": "garhostho-biggan",
    "2686": "krishi-shikkha",
    "2358": "career-shikkha",
}
# Display name overrides (2652's catalogue title is Latin-only).
DISPLAY_NAME = {"2652": "English Two (ইংরেজি দ্বিতীয় পত্র)"}

SECTION_META = {
    "grammar": ("ব্যাকরণ (Grammar)", "blue"),
    "composition": ("নির্মিতি (Composition)", "green"),
    "writing": ("রাইটিং (Writing)", "green"),
    "units": ("ইউনিট (Units)", "green"),
    "chapters": ("অধ্যায় (Chapters)", "green"),
    "prose": ("গদ্য (Prose)", "blue"),
    "poetry": ("কবিতা (Poetry)", "green"),
}

# ------------------------------------------------------- transliteration ---
# Bengali -> Latin (slug identifiers only; romanization with the inherent
# vowel rule: a consonant takes 'o' unless a vowel sign or hasanta follows,
# or it directly follows a vowel at word end. Conjunct second members:
#  য-ফলা -> y (ya before a consonant),  ব-ফলা -> w (o at word end).)
BN_CONS = {
    "ক": "k", "খ": "kh", "গ": "g", "ঘ": "gh", "ঙ": "ng",
    "চ": "ch", "ছ": "chh", "জ": "j", "ঝ": "jh", "ঞ": "n",
    "ট": "t", "ঠ": "th", "ড": "d", "ঢ": "dh", "ণ": "n",
    "ত": "t", "থ": "th", "দ": "d", "ধ": "dh", "ন": "n",
    "প": "p", "ফ": "ph", "ব": "b", "ভ": "bh", "ম": "m",
    "য": "y", "র": "r", "ল": "l", "শ": "sh", "ষ": "sh", "স": "sh", "হ": "h",
    "য়": "y", "ড়": "r", "ঢ়": "rh", "ৎ": "t",
}
BN_VOWEL = {
    "অ": "o", "আ": "a", "ই": "i", "ঈ": "i", "উ": "u", "ঊ": "u", "ঋ": "ri",
    "এ": "e", "ঐ": "oi", "ও": "o", "ঔ": "ou",
}
BN_SIGN = {
    "া": "a", "ি": "i", "ী": "i", "ু": "u", "ূ": "u", "ৃ": "ri",
    "ে": "e", "ৈ": "oi", "ো": "o", "ৌ": "ou",
}
BN_NASAL = {"ং": "ng", "ঃ": "h", "ঁ": "n"}
BN_DIGIT = {"০": "0", "১": "1", "২": "2", "৩": "3", "৪": "4",
            "৫": "5", "৬": "6", "৭": "7", "৮": "8", "৯": "9"}


def _inherent(nxt, prev):
    """'o' after this consonant? nxt = next char, prev = previous char.
    A plain word-final consonant is bare ('কলম' -> kolom, 'প্রকরণ' ->
    prokoron); only a conjunct's final member keeps its vowel
    ('সারমর্ম' -> saromormo, 'তত্ত্ব' -> totto)."""
    if nxt is None or (nxt not in BN_SIGN and nxt != "্" and nxt not in BN_NASAL
                       and nxt not in BN_CONS):
        return "o" if prev == "্" else ""
    if nxt in BN_SIGN or nxt == "্":
        return ""
    return "o"


def transliterate(text):
    out = []
    chars = list(text)
    for i, ch in enumerate(chars):
        nxt = chars[i + 1] if i + 1 < len(chars) else None
        prev = chars[i - 1] if i > 0 else None
        if ch == "্":
            continue
        if ch in BN_SIGN:
            out.append(BN_SIGN[ch])
            continue
        if ch in BN_NASAL:
            out.append(BN_NASAL[ch])
            continue
        if ch in BN_VOWEL:
            out.append(BN_VOWEL[ch])
            continue
        if ch in BN_CONS:
            if prev == "্":
                if ch == "য":
                    out.append("ya" if nxt in BN_CONS else "y")
                elif ch == "ব":
                    out.append("o" if nxt is None else "w")
                elif ch == "র":
                    out.append("r" + _inherent(nxt, prev))
                else:
                    out.append(BN_CONS[ch] + _inherent(nxt, prev))
            else:
                out.append(BN_CONS[ch] + _inherent(nxt, prev))
            continue
        out.append(BN_DIGIT.get(ch, ch))
    return "".join(out)


def slugify(text):
    """Latin slug from a Bengali/English title."""
    text = transliterate(text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def clean_unit_title(title):
    """'Unit 5 — বাক্য প্রকরণ (পৃ. ১৩৬–১৮৮)' -> 'বাক্য প্রকরণ'."""
    t = re.sub(r"^Unit\s*\d+\s*[—–-]\s*", "", title)
    t = re.split(r"\s*[•(]\s*", t)[0]
    return t.strip()


def bn_digits(n):
    return str(n).translate(str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯"))


def esc(s):
    return html.escape(s or "", quote=True)


def plain_text(html_str):
    t = re.sub(r"<[^>]+>", " ", html_str or "")
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def short_desc(text, limit=135):
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut + "…"


def all_units(code):
    """All units of a subject in book order: (section_key, item, global_index)."""
    out = []
    for key, items in NOTES[code]["contents"].items():
        for item in items:
            out.append((key, item, len(out) + 1))
    return out

# ------------------------------------------------------------- templates ---
EXTRA_CSS = """
.static-wrap{max-width:960px;margin:0 auto;padding:96px 20px 80px}
.crumbs{font-size:13.5px;color:var(--text3);margin-bottom:18px;line-height:1.8}
.crumbs a{color:var(--accent);text-decoration:none;font-weight:600}
.crumbs a:hover{text-decoration:underline}
.static-hero{background:linear-gradient(115deg,#0b1e33 0%,#14335e 48%,#1d4e89 100%);border-radius:24px;padding:34px 30px;margin-bottom:28px;color:#fff;box-shadow:0 20px 50px rgba(11,30,51,.35)}
.static-hero h1{font-family:'Noto Serif Bengali',serif;font-size:32px;line-height:1.4;margin:12px 0 10px}
.static-hero p{color:rgba(255,255,255,.85);line-height:1.8;margin:0 0 8px}
.static-hero .pill{display:inline-block;background:rgba(251,191,36,.14);border:1px solid rgba(251,191,36,.45);color:#fcd34d;border-radius:20px;padding:6px 14px;font-size:13px;font-weight:700}
.static-stats{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}
.static-stats span{background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.16);border-radius:12px;padding:8px 14px;font-size:13.5px;font-weight:600}
.static-stats b{color:#fcd34d}
a.choice-unit-row{text-decoration:none;color:inherit}
.unit-list-title{font-size:22px;font-weight:800;margin:6px 0 16px;color:var(--text)}
.app-cta{display:inline-block;background:var(--amber,#f59e0b);color:#1a1a1a;font-weight:800;text-decoration:none;border-radius:14px;padding:12px 22px;margin-top:18px;box-shadow:0 8px 20px rgba(245,158,11,.35)}
.app-cta:hover{filter:brightness(1.05)}
.prev-next{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-top:36px}
.prev-next a{background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:12px 16px;text-decoration:none;color:var(--text2);font-weight:700;font-size:14px;line-height:1.5;max-width:46%}
.prev-next a:hover{border-color:var(--accent);color:var(--accent)}
.prev-next a span{display:block;font-size:12px;color:var(--text3);font-weight:600}
.practice-note{margin-top:20px;padding:12px 16px;background:var(--bg3);border:1px dashed var(--border);border-radius:12px;font-size:13px;color:var(--text3);line-height:1.8}
.static-footer{max-width:960px;margin:0 auto;padding:0 20px 48px;text-align:center;color:var(--text3);font-size:13.5px;line-height:1.9}
.static-footer a{color:var(--accent);text-decoration:none;font-weight:600}
.topbar .topbar-logo a{text-decoration:none;color:inherit}
.creator-strip{background:linear-gradient(115deg,#0b1e33 0%,#14335e 48%,#1d4e89 100%);border-radius:22px;padding:24px 26px;margin:36px 0 8px;display:flex;align-items:center;gap:22px;color:#fff;box-shadow:0 16px 40px rgba(11,30,51,.3);position:relative;overflow:hidden}
.creator-strip::before{content:'';position:absolute;right:-50px;top:-50px;width:170px;height:170px;background:radial-gradient(circle,rgba(251,191,36,.22),transparent 70%)}
.creator-strip img{width:96px;height:96px;object-fit:cover;border-radius:16px;border:3px solid rgba(251,191,36,.7);box-shadow:0 8px 20px rgba(0,0,0,.35);flex-shrink:0;position:relative;z-index:1}
.creator-strip .cs-photo-link{display:block;flex-shrink:0;position:relative;z-index:1;line-height:0}
.creator-strip .cs-info{flex:1;position:relative;z-index:1}
.creator-strip .cs-label{display:inline-block;background:rgba(251,191,36,.14);border:1px solid rgba(251,191,36,.45);color:#fcd34d;border-radius:20px;padding:4px 12px;font-size:12px;font-weight:700;margin-bottom:8px}
.creator-strip .cs-name{font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;font-size:23px;font-weight:800;color:#fff;line-height:1.2;text-decoration:none}
.creator-strip a.cs-name:hover{text-decoration:underline}
.creator-strip .cs-link svg{width:15px;height:15px;vertical-align:-2px;margin-right:6px}
.creator-strip .cs-role{font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;font-size:13.5px;color:#fcd34d;font-weight:700;margin-top:3px}
.creator-strip .cs-desc{font-size:13px;color:rgba(255,255,255,.85);line-height:1.8;margin-top:6px}
.creator-strip .cs-links{display:flex;flex-direction:column;gap:8px;flex-shrink:0;position:relative;z-index:1}
.creator-strip .cs-link{display:inline-block;text-decoration:none;text-align:center;font-weight:700;font-size:13px;border-radius:12px;padding:9px 16px}
.creator-strip .cs-link.fb{background:#1877f2;color:#fff}
.creator-strip .cs-link.web{background:#f59e0b;color:#1a1a1a}
@media (max-width:640px){.creator-strip{flex-direction:column;text-align:center;padding:26px 20px}.creator-strip .cs-links{flex-direction:row;flex-wrap:wrap;justify-content:center}}
"""

TOPBAR = """
<header class="topbar">
  <div class="topbar-logo"><a href="/">Bisnu <span>SSC Notes</span></a></div>
  <div class="topbar-actions"><a class="theme-btn" href="/" style="text-decoration:none">🏠 হোম</a></div>
</header>
"""

FOOTER = """
<footer class="static-footer">© 2026 Bisnu SSC Notes | Designed &amp; Developed by <a href="https://bisnukundu.netlify.app/">Bishnu Kundu</a><br>তথ্য: BOU SSC বই।</footer>
<a class="wa-float" href="https://wa.me/bisnukundu?text=%E0%A6%86%E0%A6%B8%E0%A6%B8%E0%A6%BE%E0%A6%B2%E0%A6%BE%E0%A6%AE%E0%A7%81%20%E0%A6%86%E0%A6%B2%E0%A6%BE%E0%A6%87%E0%A6%95%E0%A7%81%E0%A6%AE%2C%20%E0%A6%86%E0%A6%AE%E0%A6%BF%20Bisnu%20SSC%20Notes%20%E0%A6%A5%E0%A7%87%E0%A6%95%E0%A7%87%20%E0%A6%AE%E0%A7%87%E0%A6%B8%E0%A7%87%E0%A6%9C%20%E0%A6%95%E0%A6%B0%E0%A6%9B%E0%A6%BF%E0%A5%A4" target="_blank" rel="noopener" aria-label="WhatsApp-এ মেসেজ করুন" title="WhatsApp-এ মেসেজ করুন"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg></a>
<span class="wa-tip">WhatsApp-এ মেসেজ করুন</span>
"""

CREATOR_STRIP = """
<div class="creator-strip">
  <a class="cs-photo-link" href="https://bisnukundu.netlify.app/" target="_blank" rel="noopener" title="Bishnu Kundu — Portfolio"><img src="/bisnu-avatar.webp" alt="Bishnu Kundu — এই প্ল্যাটফর্মের নির্মাতা" loading="lazy"></a>
  <div class="cs-info">
    <span class="cs-label">✦ নির্মাতা</span>
    <a class="cs-name" href="https://bisnukundu.netlify.app/" target="_blank" rel="noopener">Bishnu Kundu</a>
    <div class="cs-role">Web Developer &amp; Freelancer</div>
    <div class="cs-desc">এই নোটসগুলো তৈরি করেছেন বিষ্ণু কুন্ডু — BOU SSC ২য় বর্ষের পরীক্ষার্থীদের জন্য।</div>
  </div>
  <div class="cs-links">
    <a class="cs-link fb" href="https://facebook.com/freelancerbisnu" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>Facebook</a>
    <a class="cs-link web" href="https://bisnukundu.netlify.app/" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>Portfolio</a>
  </div>
</div>
"""


def head(title, desc, canonical, og_type, og_image, json_ld):
    return f"""<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="keywords" content="BOU SSC, SSC ২য় বর্ষ, SSC নোট, MCQ, সৃজনশীল, Bisnu SSC Notes, bisnu ssc note, উন্মুক্ত বিশ্ববিদ্যালয়">
<meta name="author" content="Bishnu Kundu">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{esc(canonical)}">
<meta name="theme-color" content="#0b1e33">
<link rel="icon" type="image/png" href="/favicon.png">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Bisnu SSC Notes">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{esc(og_image)}">
<meta property="og:locale" content="bn_BD">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{esc(og_image)}">
<script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False)}</script>
<link rel="stylesheet" href="/index.css">
<style>{EXTRA_CSS}</style>
</head>
<body>
{TOPBAR}
"""


def crumbs(items):
    """items: list of (label, href or None)."""
    parts = []
    for label, href in items:
        if href:
            parts.append(f'<a href="{esc(href)}">{esc(label)}</a>')
        else:
            parts.append(f"<span>{esc(label)}</span>")
    return '<nav class="crumbs">' + " › ".join(parts) + "</nav>"


# --------------------------------------------------- unit card (SPA port) ---
def unit_card(code, section_key, item, idx, subject):
    label, color = SECTION_META.get(section_key, ("ইউনিট (Units)", "green"))
    title = item["title"]
    genre = item.get("genre") or label
    parts = [f'<article class="card visible">']
    parts.append(
        f'<div class="card-header {color}"><span class="card-no">{bn_digits(idx)}</span>'
        f'<span class="card-title">{esc(title)}</span>'
        f'<span class="genre-badge">{esc(genre)}</span></div>'
    )
    parts.append('<div class="card-body">')
    parts.append(f'<div class="summary-box summary-box-{color}">{item.get("summary") or ""}</div>')
    info = item.get("infographic")
    if info:
        alt = item.get("infographic_alt") or f"{title} — ইনফোগ্রাফিক"
        parts.append(
            f'<div class="infographic-wrap"><img class="unit-infographic" src="/{esc(info)}" '
            f'alt="{esc(alt)}" loading="lazy">'
            f'<div class="infographic-caption">📊 ইনফোগ্রাফিক — এক নজরে Unit-টি</div></div>'
        )
    creative = item.get("creative") or {}
    if creative.get("question"):
        ans = creative.get("answer") or {}
        cells = "".join(
            f'<div class="point-item"><span class="point-dot">{k}</span>'
            f'<div><div class="point-title">{esc(v)}</div></div></div>'
            for k, v in ans.items()
            if v and k in ("ক", "খ", "গ", "ঘ")
        )
        parts.append(
            f'<div class="creative-block"><div class="box-label" style="margin-top:8px">✍️ সৃজনশীল প্রশ্ন</div>'
            f'<div class="creative-question">{esc(creative["question"])}</div>'
            f'<div class="points-grid">{cells}</div></div>'
        )
    mcqs = item.get("mcq") or []
    if mcqs:
        rows = []
        for i, q in enumerate(mcqs, 1):
            opts = "".join(
                f'<span class="mcq-opt">{esc(o)}</span>' for o in (q.get("options") or [])
            )
            rows.append(
                f'<div class="mcq-item"><div class="mcq-q">{bn_digits(i)}. {esc(q.get("question") or "")}</div>'
                f'<div class="mcq-opts">{opts}</div>'
                f'<div class="mcq-ans">✅ সঠিক উত্তর: <b>{esc(q.get("answer") or "")}</b></div></div>'
            )
        parts.append(
            f'<div class="mcq-section"><div class="mcq-header-bar"><span class="mcq-title">❓ MCQ — অনুশীলনী</span>'
            f'<span class="mcq-count">{bn_digits(len(mcqs))}টি প্রশ্ন</span></div>'
            + "".join(rows)
            + "</div>"
        )
    parts.append("</div></article>")
    return "".join(parts)


def practice_note(code, idx):
    if code == "2651" and idx == 1:
        return ("📖 এই Unit-এর ৪টি MCQ বইয়ের নিজস্ব পাঠোত্তর মূল্যায়ন (পৃ. ২) থেকে নেওয়া।")
    return ("📝 এই পেজের MCQ ও সৃজনশীল প্রশ্ন অনুশীলনী (Practice) — বইয়ের নিজস্ব প্রশ্ন নয়, "
            "Unit-এর বিষয়বস্তুর উপর তৈরি।")


# ------------------------------------------------------------ page builders ---
def subject_page(code, paths=None):
    sub = SUBJECTS[code]
    name = DISPLAY_NAME.get(code, sub["title_bn"])
    slug = SUBJECT_SLUGS[code]
    path = f"/subjects/{code}-{slug}.html"
    units = all_units(code)
    n = len(units)
    total_mcq = sum(len(u.get("mcq") or []) for _, u, _ in units)
    title = f"{name} নোট, MCQ ও সৃজনশীল প্রশ্ন | Bisnu SSC Notes"
    desc = (f"BOU SSC ২য় বর্ষের {name} ({sub['title_en']})-এর {bn_digits(n)}টি Unit-এর ফ্রি শর্ট নোট, "
            f"{bn_digits(total_mcq)}টি MCQ, {bn_digits(n)}টি সৃজনশীল প্রশ্ন ও ইনফোগ্রাফিক — Bisnu SSC Notes।")
    marks = sub.get("marks") or {}
    marks_line = ""
    if marks.get("total"):
        marks_line = (f"<p>📝 মোট {bn_digits(marks['total'])} নম্বর "
                      f"(সৃজনশীল {bn_digits(marks.get('creative', ''))} + MCQ {bn_digits(marks.get('mcq', ''))}) — "
                      f"BOU বই থেকে যাচাইকৃত।</p>")
    rows = []
    for key, item, idx in units:
        upath = unit_path(code, item, idx, paths)
        rows.append(
            f'<a class="choice-unit-row" href="{esc(upath)}">'
            f'<span class="choice-unit-no">{bn_digits(idx)}</span>'
            f'<span class="choice-unit-name">{esc(item["title"])}</span>'
            f'<span class="choice-unit-arrow">›</span></a>'
        )
    json_ld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": desc,
        "inLanguage": "bn",
        "author": {"@type": "Person", "name": "Bishnu Kundu"},
        "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "হোম", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": SITE + path},
        ]},
        "mainEntity": {"@type": "Course", "name": f"SSC {name}",
                       "provider": {"@type": "Organization", "name": "Bisnu SSC Notes"}},
    }
    body = (
        head(title, desc, SITE + path, "website", SITE + "/og-image.png", json_ld)
        + '<div class="static-wrap">'
        + crumbs([("🏠 হোম", "/"), (name, None)])
        + '<div class="static-hero"><span class="pill">🎓 BOU • SSC ২য় বর্ষ — নতুন ভার্সন</span>'
        f'<h1>{esc(name)} — সম্পূর্ণ নোট</h1>'
        f'<p>{esc(sub["title_en"])} • BOU SSC ২য় বর্ষ • নতুন ভার্সন</p>'
        f"{marks_line}"
        f'<div class="static-stats"><span><b>{bn_digits(n)}</b>টি Unit</span>'
        f'<span><b>{bn_digits(total_mcq)}</b>টি MCQ</span>'
        f'<span><b>{bn_digits(n)}</b>টি সৃজনশীল</span>'
        f'<span><b>{bn_digits(n)}</b>টি ইনফোগ্রাফিক</span></div>'
        f'<a class="app-cta" href="/#s={code}">📱 অ্যাপে পড়ুন →</a></div>'
        f'<h2 class="unit-list-title">📚 সব Unit — এক নজরে</h2>'
        + "".join(rows)
        + f'<p class="practice-note">{esc(practice_note_note(code))}</p>'
        + CREATOR_STRIP
        + "</div>" + FOOTER + "\n</body>\n</html>\n"
    )
    return path, body


def practice_note_note(code):
    return ("এই বিষয়ের MCQ ও সৃজনশীল প্রশ্ন অনুশীলনী (Practice) — বইয়ের নিজস্ব প্রশ্ন নয়, "
            "Unit-এর বিষয়বস্তুর উপর তৈরি। শুধু বাংলা দ্বিতীয় পত্র (SSC-2651) Unit 1-এর ৪টি MCQ বইয়ের নিজস্ব (পৃ. ২)।")


def unit_path(code, item, idx, paths=None):
    if paths and idx in paths:
        return paths[idx]
    slug = slugify(clean_unit_title(item["title"])) or f"unit-{idx}"
    return f"/subjects/{code}/unit-{idx}-{slug}.html"


def unit_page(code, section_key, item, idx, prev_u, next_u, paths=None):
    sub = SUBJECTS[code]
    name = DISPLAY_NAME.get(code, sub["title_bn"])
    slug = SUBJECT_SLUGS[code]
    path = unit_path(code, item, idx, paths)
    clean = clean_unit_title(item["title"])
    title = f"{clean} — {name} নোট | Bisnu SSC Notes"
    desc = short_desc(plain_text(item.get("summary") or "")) + " | Bisnu SSC Notes"
    info = item.get("infographic")
    og_image = SITE + "/" + info if info else SITE + "/og-image.png"
    sub_path = f"/subjects/{code}-{slug}.html"
    json_ld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": desc,
        "inLanguage": "bn",
        "author": {"@type": "Person", "name": "Bishnu Kundu"},
        "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "হোম", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": SITE + sub_path},
            {"@type": "ListItem", "position": 3, "name": clean, "item": SITE + path},
        ]},
        "mainEntity": {"@type": "Article", "headline": title, "inLanguage": "bn",
                       "author": {"@type": "Person", "name": "Bishnu Kundu"},
                       "about": {"@type": "Course", "name": f"SSC {name}"}},
    }
    nav = []
    if prev_u:
        nav.append(f'<a href="{esc(unit_path(code, prev_u[1], prev_u[2], paths))}"><span>← আগের Unit</span>'
                   f'{esc(clean_unit_title(prev_u[1]["title"]))}</a>')
    else:
        nav.append(f'<a href="{esc(sub_path)}"><span>← বিষয়ের সব Unit</span>{esc(name)}</a>')
    if next_u:
        nav.append(f'<a href="{esc(unit_path(code, next_u[1], next_u[2], paths))}"><span>পরের Unit →</span>'
                   f'{esc(clean_unit_title(next_u[1]["title"]))}</a>')
    else:
        nav.append(f'<a href="{esc(sub_path)}"><span>বিষয়ের সব Unit →</span>{esc(name)}</a>')
    body = (
        head(title, desc, SITE + path, "article", og_image, json_ld)
        + '<div class="static-wrap">'
        + crumbs([("🏠 হোম", "/"), (name, sub_path), (clean, None)])
        + unit_card(code, section_key, item, idx, sub)
        + f'<a class="app-cta" href="/#s={code}&amp;u={idx}">📱 অ্যাপে এই Unit পড়ুন →</a>'
        + '<nav class="prev-next">' + "".join(nav) + "</nav>"
        + f'<p class="practice-note">{esc(practice_note(code, idx))}</p>'
        + CREATOR_STRIP
        + "</div>" + FOOTER + "\n</body>\n</html>\n"
    )
    return path, body

# ------------------------------------------------------------------ main ---
def main():
    warnings = []
    pages = []  # (relative_path, url_path, priority, changefreq)
    out_root = ROOT / "subjects"

    for code in SUBJECTS:
        units = all_units(code)
        # Final unit paths first (with duplicate-slug de-dup), so every
        # link, canonical and OG URL agrees on one path per unit.
        paths = {}
        used = {}
        for key, item, idx in units:
            base = slugify(clean_unit_title(item["title"])) or f"unit-{idx}"
            slug = base
            if slug in used:
                warnings.append(f"duplicate slug {code} unit {idx}: '{slug}' -> '{slug}-2'")
                slug = f"{base}-2"
            used[slug] = idx
            paths[idx] = f"/subjects/{code}/unit-{idx}-{slug}.html"

        sub_path, sub_body = subject_page(code, paths)
        dest = ROOT / sub_path.lstrip("/")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(sub_body, encoding="utf-8")
        pages.append((sub_path, 0.8, "weekly"))

        for i, (key, item, idx) in enumerate(units):
            prev_u = units[i - 1] if i > 0 else None
            next_u = units[i + 1] if i + 1 < len(units) else None
            path, body = unit_page(code, key, item, idx, prev_u, next_u, paths)
            dest = ROOT / path.lstrip("/")
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(body, encoding="utf-8")
            pages.append((path, 0.6, "monthly"))
        print(f"{code}: {len(units)} units -> {sub_path}")

    # Sitemap: homepage + all static pages.
    urls = [(SITE + "/", "1.0", "weekly")]
    for path, prio, freq in pages:
        urls.append((SITE + path, str(prio), freq))
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, prio, freq in urls:
        sitemap.append(
            f"<url><loc>{esc(url)}</loc><lastmod>{TODAY}</lastmod>"
            f"<changefreq>{freq}</changefreq><priority>{prio}</priority></url>"
        )
    sitemap.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")

    print(f"\nTotal pages: {len(pages)} static + 1 home = {len(urls)} URLs in sitemap")
    if warnings:
        print("Warnings:")
        for w in warnings:
            print(" -", w)
    else:
        print("No slug warnings.")


if __name__ == "__main__":
    main()
