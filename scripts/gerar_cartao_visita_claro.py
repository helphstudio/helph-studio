from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from reportlab.graphics.barcode import qr


ROOT = Path(__file__).resolve().parents[1]
VERSION = "2026-06-03-v2-claro"
SUFFIX = "v2-claro-20260603"
OUT = ROOT / "assets" / "img" / "cartao-visita" / VERSION
OUT.mkdir(parents=True, exist_ok=True)

DPI = 300
MM = DPI / 25.4
CARD_W_MM, CARD_H_MM = 90, 50
BLEED_MM = 3
A4_W_MM, A4_H_MM = 210, 297

CARD_W = round(CARD_W_MM * MM)
CARD_H = round(CARD_H_MM * MM)
BLEED = round(BLEED_MM * MM)
BLEED_W = CARD_W + BLEED * 2
BLEED_H = CARD_H + BLEED * 2
A4_W = round(A4_W_MM * MM)
A4_H = round(A4_H_MM * MM)

FONT_REG = "C:/Windows/Fonts/segoeui.ttf"
FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_DISPLAY = "C:/Windows/Fonts/bahnschrift.ttf"
FONT_BLACK = "C:/Windows/Fonts/ariblk.ttf"
LOGO_PATH = ROOT / "assets" / "img" / "marca" / "logos" / "helph-logo-horizontal.jpg"

COLORS = {
    "paper": (245, 244, 250),
    "paper2": (236, 234, 246),
    "panel": (255, 255, 255),
    "ink": (24, 24, 34),
    "muted": (98, 98, 122),
    "muted2": (128, 124, 150),
    "line": (215, 211, 231),
    "purple": (124, 92, 252),
    "purple2": (167, 139, 250),
    "blue": (46, 118, 178),
    "deep": (10, 10, 15),
    "white": (255, 255, 255),
}

DATA = {
    "brand": "Helph Studio",
    "tagline": "Sites e aplicativos para negócios",
    "name": "Pedro Henrique Pereira",
    "title": "Fundador & desenvolvedor web",
    "phone": "(21) 97134-9275",
    "phone_intl": "+5521971349275",
    "email": "helphstudio@gmail.com",
    "site": "helphstudio.com.br",
    "site_url": "https://helphstudio.com.br",
    "instagram": "@helphstudio",
    "instagram_url": "https://www.instagram.com/helphstudio/",
    "facebook": "facebook.com/helphstudio",
    "facebook_url": "https://www.facebook.com/helphstudio",
    "linktree": "linktr.ee/helphstudio",
    "linktree_url": "https://linktr.ee/helphstudio",
    "linkedin": "linkedin.com/in/pereirapedrohs",
    "linkedin_url": "https://www.linkedin.com/in/pereirapedrohs/",
    "whatsapp_url": "https://wa.me/5521971349275",
}

VCARD = f"""BEGIN:VCARD
VERSION:3.0
N:Pereira;Pedro;Henrique;;
FN:Pedro Henrique Pereira
ORG:Helph Studio
TITLE:Fundador & desenvolvedor web
TEL;TYPE=CELL,WHATSAPP:{DATA["phone_intl"]}
EMAIL:{DATA["email"]}
URL:{DATA["site_url"]}
X-SOCIALPROFILE;TYPE=instagram:{DATA["instagram_url"]}
X-SOCIALPROFILE;TYPE=linkedin:{DATA["linkedin_url"]}
END:VCARD
"""


def rgba(color, alpha=255):
    return (*color, alpha)


def font(size, weight="regular"):
    if weight == "display":
        return ImageFont.truetype(FONT_DISPLAY, size)
    if weight == "black":
        return ImageFont.truetype(FONT_BLACK if Path(FONT_BLACK).exists() else FONT_BOLD, size)
    if weight == "bold":
        return ImageFont.truetype(FONT_BOLD, size)
    return ImageFont.truetype(FONT_REG, size)


def text_size(d, text, fnt):
    box = d.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def fit_font(d, text, size, weight, max_w, min_size=8):
    while size >= min_size:
        fnt = font(size, weight)
        if d.textlength(text, font=fnt) <= max_w:
            return fnt
        size -= 1
    return font(min_size, weight)


def center_text(d, box, text, fnt, fill):
    x1, y1, x2, y2 = box
    tw, th = text_size(d, text, fnt)
    d.text((x1 + (x2 - x1 - tw) / 2, y1 + (y2 - y1 - th) / 2 - 1), text, font=fnt, fill=fill)


def wrap_lines(d, text, fnt, max_w):
    words = text.split()
    lines, line = [], ""
    for word in words:
        test = word if not line else f"{line} {word}"
        if d.textlength(test, font=fnt) <= max_w:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_wrapped(d, text, x, y, fnt, fill, max_w, gap=8):
    line_h = text_size(d, "Ag", fnt)[1] + gap
    for line in wrap_lines(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += line_h
    return y


def light_bg(w, h, accent=COLORS["purple"]):
    img = Image.new("RGBA", (w, h), rgba(COLORS["paper"], 255))
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle((0, 0, w, h), fill=rgba(COLORS["paper2"], 85))
    d.line((0, 0, int(w * 0.34), 0), fill=accent, width=max(4, w // 190))
    d.rounded_rectangle((-round(9 * MM), h - round(9 * MM), w + round(4 * MM), h + round(4 * MM)), radius=round(14 * MM), fill=rgba(COLORS["white"], 138))
    for scale, alpha in [(0.34, 34), (0.24, 22)]:
        rr = int(w * scale)
        d.ellipse((w - rr * 0.74, -rr * 0.48, w + rr * 0.28, rr * 0.54), outline=rgba(accent, alpha), width=max(1, w // 700))
    return Image.alpha_composite(img, layer)


def draw_logo_asset(img, x, y, w):
    logo = Image.open(LOGO_PATH).convert("RGB")
    ratio = logo.height / logo.width
    h = round(w * ratio)
    logo = logo.resize((w, h), Image.Resampling.LANCZOS)
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, w, h), radius=max(8, h // 7), fill=255)
    img.paste(logo, (x, y), mask)
    return h


def qr_image(data, size, fg=COLORS["ink"], bg=COLORS["white"], border=4):
    widget = qr.QrCodeWidget(data)
    enc = widget.qr
    enc.make()
    count = enc.moduleCount
    total = count + border * 2
    scale = max(1, size // total)
    actual = total * scale
    img = Image.new("RGB", (actual, actual), bg)
    d = ImageDraw.Draw(img)
    for row in range(count):
        for col in range(count):
            if enc.isDark(row, col):
                x = (col + border) * scale
                y = (row + border) * scale
                d.rectangle((x, y, x + scale - 1, y + scale - 1), fill=fg)
    if actual != size:
        img = img.resize((size, size), Image.Resampling.NEAREST)
    return img


def contact_chip(d, box, label, value, accent=COLORS["purple"], value_size=25):
    x1, y1, x2, y2 = box
    d.rounded_rectangle(box, radius=15, fill=COLORS["panel"], outline=COLORS["line"], width=2)
    d.rectangle((x1, y1 + 12, x1 + 5, y2 - 12), fill=accent)
    d.text((x1 + 18, y1 + 12), label.upper(), font=font(14, "bold"), fill=accent)
    value_f = fit_font(d, value, value_size, "bold", x2 - x1 - 36, 14)
    d.text((x1 + 18, y1 + 34), value, font=value_f, fill=COLORS["ink"])


def draw_social_line(d, x, y, w, include_linkedin=False):
    text = f"{DATA['instagram']}  ·  {DATA['facebook']}  ·  {DATA['linktree']}"
    if include_linkedin:
        text += f"  ·  {DATA['linkedin']}"
    fnt = fit_font(d, text, 15, "bold", w, 9)
    d.text((x, y), text, font=fnt, fill=COLORS["muted"])


def draw_personal_front(w=CARD_W, h=CARD_H, bleed=False):
    img = light_bg(w, h, COLORS["purple"])
    d = ImageDraw.Draw(img)
    margin = round(5.5 * MM) + (BLEED if bleed else 0)
    draw_logo_asset(img, margin, margin, round(34 * MM))
    d.text((margin, margin + round(12.8 * MM)), DATA["tagline"], font=font(19, "bold"), fill=COLORS["muted"])

    y = margin + round(20 * MM)
    d.text((margin, y), DATA["name"], font=fit_font(d, DATA["name"], 35, "display", round(67 * MM), 24), fill=COLORS["ink"])
    d.text((margin, y + round(7 * MM)), DATA["title"], font=font(20, "bold"), fill=COLORS["purple"])

    d.rounded_rectangle((margin, h - margin - round(8.4 * MM), w - margin, h - margin), radius=16, fill=COLORS["panel"], outline=rgba(COLORS["purple"], 155), width=2)
    center_text(d, (margin, h - margin - round(8.4 * MM), w - margin, h - margin), f"{DATA['phone']}  ·  {DATA['site']}", font(20, "bold"), COLORS["ink"])
    return img.convert("RGB")


def draw_personal_back(w=CARD_W, h=CARD_H, bleed=False):
    img = light_bg(w, h, COLORS["blue"])
    d = ImageDraw.Draw(img)
    margin = round(5.5 * MM) + (BLEED if bleed else 0)
    draw_logo_asset(img, margin, margin, round(26 * MM))

    qr_size = round(19 * MM)
    qx = w - margin - qr_size
    qy = margin
    d.rounded_rectangle((qx - 8, qy - 8, qx + qr_size + 8, qy + qr_size + 8), radius=13, fill=COLORS["white"], outline=COLORS["line"], width=1)
    img.paste(qr_image(DATA["site_url"], qr_size), (qx, qy))
    center_text(d, (qx - 10, qy + qr_size + 8, qx + qr_size + 10, qy + qr_size + 32), "site + portfólio", font(13, "bold"), COLORS["muted"])

    x = margin
    y = margin + round(12.5 * MM)
    chip_w = round(51 * MM)
    chip_h = round(6.8 * MM)
    gap = round(1.7 * MM)
    contact_chip(d, (x, y, x + chip_w, y + chip_h), "WhatsApp", DATA["phone"], COLORS["blue"], 22)
    y += chip_h + gap
    contact_chip(d, (x, y, x + chip_w, y + chip_h), "E-mail", DATA["email"], COLORS["blue"], 22)
    y += chip_h + gap
    contact_chip(d, (x, y, x + chip_w, y + chip_h), "Site", DATA["site"], COLORS["blue"], 22)

    draw_social_line(d, margin, h - margin - round(2.6 * MM), w - margin * 2, include_linkedin=False)
    return img.convert("RGB")


def draw_brand_front(w=CARD_W, h=CARD_H, bleed=False):
    img = light_bg(w, h, COLORS["purple"])
    d = ImageDraw.Draw(img)
    margin = round(6 * MM) + (BLEED if bleed else 0)
    draw_logo_asset(img, margin, margin, round(38 * MM))
    d.text((margin, margin + round(14 * MM)), DATA["tagline"], font=font(21, "bold"), fill=COLORS["muted"])

    y = margin + round(20 * MM)
    d.text((margin, y), "Sites, apps e presença digital", font=fit_font(d, "Sites, apps e presença digital", 34, "display", round(70 * MM), 22), fill=COLORS["ink"])
    d.text((margin, y + round(6.8 * MM)), "para negócios locais e profissionais liberais.", font=fit_font(d, "para negócios locais e profissionais liberais.", 20, "bold", round(70 * MM), 12), fill=COLORS["muted"])

    d.rounded_rectangle((margin, h - margin - round(8 * MM), w - margin, h - margin), radius=15, fill=COLORS["panel"], outline=rgba(COLORS["purple"], 150), width=2)
    center_text(d, (margin, h - margin - round(8 * MM), w - margin, h - margin), "Orçamento pelo WhatsApp", font(21, "bold"), COLORS["ink"])
    return img.convert("RGB")


def draw_brand_back(w=CARD_W, h=CARD_H, bleed=False):
    img = light_bg(w, h, COLORS["purple"])
    d = ImageDraw.Draw(img)
    margin = round(6 * MM) + (BLEED if bleed else 0)
    draw_logo_asset(img, margin, margin, round(29 * MM))
    d.text((margin, margin + round(12 * MM)), "Canais oficiais", font=font(18, "bold"), fill=COLORS["purple"])

    qr_size = round(20 * MM)
    qx = w - margin - qr_size
    qy = margin
    d.rounded_rectangle((qx - 8, qy - 8, qx + qr_size + 8, qy + qr_size + 8), radius=13, fill=COLORS["white"], outline=COLORS["line"], width=1)
    img.paste(qr_image(DATA["site_url"], qr_size), (qx, qy))

    contact_y = margin + round(18 * MM)
    chip_w = round(48 * MM)
    chip_h = round(7.2 * MM)
    contact_chip(d, (margin, contact_y, margin + chip_w, contact_y + chip_h), "WhatsApp", DATA["phone"], COLORS["purple"], 22)
    contact_y += round(8.8 * MM)
    contact_chip(d, (margin, contact_y, margin + chip_w, contact_y + chip_h), "Site", DATA["site"], COLORS["purple"], 22)

    draw_social_line(d, margin, h - margin - round(2.6 * MM), w - margin * 2, include_linkedin=True)
    return img.convert("RGB")


def draw_virtual_personal():
    w, h = 1080, 1920
    img = light_bg(w, h, COLORS["purple"])
    d = ImageDraw.Draw(img)
    margin = 74
    draw_logo_asset(img, margin, 72, 340)
    d.text((margin, 166), DATA["tagline"], font=font(28, "bold"), fill=COLORS["muted"])
    d.text((margin, 302), DATA["name"], font=fit_font(d, DATA["name"], 62, "display", 910, 38), fill=COLORS["ink"])
    d.text((margin, 374), DATA["title"], font=font(34, "bold"), fill=COLORS["purple"])
    d.line((margin, 432, margin + 240, 432), fill=COLORS["purple"], width=5)
    y = draw_wrapped(d, "Sites, aplicativos e presença digital para negócios que querem vender melhor sem complicar a vida.", margin, 495, font(35, "bold"), COLORS["ink"], 900, 14)

    qsize = 340
    qx, qy = margin, y + 70
    d.rounded_rectangle((qx - 18, qy - 18, qx + qsize + 18, qy + qsize + 18), radius=26, fill=COLORS["white"], outline=COLORS["line"], width=2)
    img.paste(qr_image(VCARD, qsize), (qx, qy))
    d.text((qx + qsize + 52, qy + 28), "Salvar contato", font=font(46, "display"), fill=COLORS["ink"])
    draw_wrapped(d, "Escaneie o QR ou envie o arquivo .vcf junto com este cartão.", qx + qsize + 52, qy + 88, font(28), COLORS["muted"], 455, 10)

    rows = [
        ("WhatsApp", DATA["phone"]),
        ("E-mail", DATA["email"]),
        ("Site", DATA["site"]),
        ("Instagram", DATA["instagram"]),
        ("Facebook", DATA["facebook"]),
        ("Linktree", DATA["linktree"]),
    ]
    y = qy + qsize + 95
    for label, value in rows:
        contact_chip(d, (margin, y, w - margin, y + 82), label, value, COLORS["purple"])
        y += 96
    d.rounded_rectangle((margin, h - 160, w - margin, h - 84), radius=18, fill=COLORS["deep"])
    center_text(d, (margin, h - 160, w - margin, h - 84), DATA["site"], font(34, "bold"), COLORS["white"])
    return img.convert("RGB")


def draw_crop_marks(d, x, y, w, h):
    mark = round(4 * MM)
    gap = round(1.5 * MM)
    color = (90, 90, 105)
    for cx, cy, sx, sy in [(x, y, -1, -1), (x + w, y, 1, -1), (x, y + h, -1, 1), (x + w, y + h, 1, 1)]:
        d.line((cx + sx * gap, cy, cx + sx * (gap + mark), cy), fill=color, width=2)
        d.line((cx, cy + sy * gap, cx, cy + sy * (gap + mark)), fill=color, width=2)


def make_a4_sheet(card_img, name):
    sheet = Image.new("RGB", (A4_W, A4_H), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    cols, rows = 2, 5
    gap_x = round(5 * MM)
    gap_y = round(4 * MM)
    total_w = cols * CARD_W + gap_x
    total_h = rows * CARD_H + (rows - 1) * gap_y
    start_x = (A4_W - total_w) // 2
    start_y = (A4_H - total_h) // 2
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * (CARD_W + gap_x)
            y = start_y + row * (CARD_H + gap_y)
            sheet.paste(card_img, (x, y))
            draw_crop_marks(d, x, y, CARD_W, CARD_H)
    save_image(sheet, name, pdf=True)
    return sheet


def make_duplex_pdf(front_sheet, back_sheet, stem):
    front_sheet.save(OUT / f"{stem}-{SUFFIX}.pdf", "PDF", resolution=DPI, save_all=True, append_images=[back_sheet])


def save_image(img, stem, pdf=False):
    png = OUT / f"{stem}-{SUFFIX}.png"
    jpg = OUT / f"{stem}-{SUFFIX}.jpg"
    img.save(png)
    img.save(jpg, quality=94, optimize=True)
    if pdf:
        img.save(OUT / f"{stem}-{SUFFIX}.pdf", "PDF", resolution=DPI)


def make_set(prefix, front_func, back_func):
    front = front_func()
    back = back_func()
    front_bleed = front_func(BLEED_W, BLEED_H, True)
    back_bleed = back_func(BLEED_W, BLEED_H, True)
    save_image(front, f"{prefix}-frente-90x50mm", pdf=True)
    save_image(back, f"{prefix}-verso-90x50mm", pdf=True)
    save_image(front_bleed, f"{prefix}-frente-com-sangria-96x56mm", pdf=True)
    save_image(back_bleed, f"{prefix}-verso-com-sangria-96x56mm", pdf=True)
    front_sheet = make_a4_sheet(front, f"folha-a4-{prefix}-frente-10-cartoes")
    back_sheet = make_a4_sheet(back, f"folha-a4-{prefix}-verso-10-cartoes")
    make_duplex_pdf(front_sheet, back_sheet, f"folha-a4-{prefix}-duplex-10-cartoes")


def write_files():
    (OUT / f"pedro-henrique-pereira-helph-studio-{SUFFIX}.vcf").write_text(VCARD, encoding="utf-8")
    html = f"""<!doctype html>
<html lang="pt-BR">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Pedro Henrique Pereira - Helph Studio</title>
<style>
body{{margin:0;min-height:100vh;display:grid;place-items:center;padding:24px;font-family:Segoe UI,Arial,sans-serif;background:#f5f4fa;color:#181822}}
main{{width:min(460px,100%);background:#fff;border:1px solid #d7d3e7;border-radius:24px;padding:28px;box-shadow:0 20px 60px rgba(50,40,90,.14)}}
h1{{margin:0 0 6px;font-size:34px}} h1 span{{color:#a78bfa}} .tag{{color:#62627a;font-weight:700;margin-bottom:28px}} h2{{font-size:28px;margin:0}} .role{{font-weight:800;color:#7c5cfc;margin:8px 0 20px}} p{{color:#62627a;line-height:1.55}}
a{{display:flex;justify-content:space-between;gap:14px;margin-top:12px;padding:14px 16px;border:1px solid #d7d3e7;border-radius:14px;color:#181822;text-decoration:none;font-weight:800;background:#faf9ff}} small{{color:#62627a;font-weight:700}}
</style></head>
<body><main>
<h1>Hel<span>ph</span> Studio</h1><div class="tag">{DATA["tagline"]}</div>
<h2>{DATA["name"]}</h2><div class="role">{DATA["title"]}</div>
<p>Sites, apps e presença digital para negócios locais, autônomos e profissionais liberais.</p>
<a href="{DATA["whatsapp_url"]}">WhatsApp <small>{DATA["phone"]}</small></a>
<a href="mailto:{DATA["email"]}">E-mail <small>{DATA["email"]}</small></a>
<a href="{DATA["site_url"]}">Site <small>{DATA["site"]}</small></a>
<a href="{DATA["instagram_url"]}">Instagram <small>{DATA["instagram"]}</small></a>
<a href="{DATA["facebook_url"]}">Facebook <small>/helphstudio</small></a>
<a href="{DATA["linktree_url"]}">Linktree <small>/helphstudio</small></a>
<a href="pedro-henrique-pereira-helph-studio-{SUFFIX}.vcf" download>Salvar contato <small>.vcf</small></a>
</main></body></html>"""
    (OUT / f"cartao-virtual-html-{SUFFIX}.html").write_text(html, encoding="utf-8")
    guide = f"""# Cartões de visita claros - Helph Studio

Versão: {VERSION}

Esta leva é mais econômica para impressão: fundo claro, menos área chapada de tinta e logo oficial aplicada em bloco reduzido.

## Cartão pessoal

- `cartao-pessoal-frente-*`
- `cartao-pessoal-verso-*`
- `folha-a4-cartao-pessoal-*`

## Cartão institucional / site

- `cartao-site-frente-*`
- `cartao-site-verso-*`
- `folha-a4-cartao-site-*`

## Digital

- `cartao-pessoal-virtual-whatsapp-*`: imagem para WhatsApp/Instagram.
- `pedro-henrique-pereira-helph-studio-*.vcf`: contato para salvar no celular.
- `cartao-virtual-html-*`: cartão clicável para hospedar futuramente.

Para gráfica, use os arquivos `com-sangria-96x56mm`.
Para imprimir em casa, use os PDFs `folha-a4-*-duplex-10-cartoes`.
"""
    (OUT / f"guia-cartao-visita-claro-{SUFFIX}.md").write_text(guide, encoding="utf-8")


def main():
    make_set("cartao-pessoal", draw_personal_front, draw_personal_back)
    make_set("cartao-site", draw_brand_front, draw_brand_back)
    save_image(draw_virtual_personal(), "cartao-pessoal-virtual-whatsapp")
    write_files()


if __name__ == "__main__":
    main()
