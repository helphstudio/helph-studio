from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from reportlab.graphics.barcode import qr


ROOT = Path(__file__).resolve().parents[1]
VERSION = "2026-06-03-v1"
SUFFIX = "v1-20260603"
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

FONT_REG = "C:/Windows/Fonts/arial.ttf"
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_BLACK = "C:/Windows/Fonts/ariblk.ttf"

COLORS = {
    "bg": (10, 10, 15),
    "bg2": (17, 17, 24),
    "panel": (24, 24, 31),
    "text": (240, 240, 245),
    "muted": (150, 150, 174),
    "muted2": (88, 88, 112),
    "purple": (124, 92, 252),
    "purple2": (167, 139, 250),
    "blue": (125, 211, 252),
    "white": (255, 255, 255),
    "paper": (255, 255, 255),
    "ink": (20, 20, 28),
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
END:VCARD
"""


def rgba(color, alpha=255):
    return (*color, alpha)


def font(size, weight="regular"):
    path = FONT_REG
    if weight == "bold":
        path = FONT_BOLD
    if weight == "black":
        path = FONT_BLACK if Path(FONT_BLACK).exists() else FONT_BOLD
    return ImageFont.truetype(path, size)


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
    lines = []
    line = ""
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


def card_bg(w, h, accent=COLORS["purple"]):
    img = Image.new("RGBA", (w, h), rgba(COLORS["bg"], 255))
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle((0, 0, w, h), fill=rgba(COLORS["bg2"], 45))
    d.line((0, 0, int(w * 0.36), 0), fill=accent, width=max(3, w // 180))
    for r in range(max(w, h), 0, -24):
        alpha = int(42 * (1 - r / max(w, h)) ** 2)
        d.ellipse((w * 0.58 - r, -h * 0.42 - r, w * 0.58 + r, -h * 0.42 + r), fill=rgba(accent, alpha))
    for scale, alpha in [(0.36, 33), (0.26, 22)]:
        rr = int(w * scale)
        d.ellipse((w - rr * 0.72, -rr * 0.50, w + rr * 0.28, rr * 0.50), outline=rgba(accent, alpha), width=max(1, w // 650))
    return Image.alpha_composite(img, layer)


def draw_logo(d, x, y, size):
    f = font(size, "black")
    d.text((x, y), "Hel", font=f, fill=COLORS["text"])
    x2 = x + d.textlength("Hel", font=f) - size * 0.08
    d.text((x2, y), "ph", font=f, fill=COLORS["purple2"])
    x3 = x2 + d.textlength("ph", font=f) + size * 0.16
    d.text((x3, y), "Studio", font=f, fill=COLORS["text"])


def draw_pill(d, x, y, text, accent, size=24):
    fnt = font(size, "bold")
    tw, th = text_size(d, text, fnt)
    pad_x, pad_y = int(size * 0.65), int(size * 0.35)
    box = (x, y, x + tw + pad_x * 2, y + th + pad_y * 2)
    d.rounded_rectangle(box, radius=int(size * 0.9), fill=rgba(accent, 30), outline=rgba(accent, 120), width=2)
    d.text((x + pad_x, y + pad_y - 1), text, font=fnt, fill=accent)


def qr_image(data, size, fg=COLORS["ink"], bg=COLORS["paper"], border=4):
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


def draw_contact_row(d, x, y, label, value, accent, max_w, size=29):
    label_f = font(size - 8, "bold")
    value_f = fit_font(d, value, size, "bold", max_w, 16)
    d.text((x, y), label.upper(), font=label_f, fill=accent)
    d.text((x, y + size - 2), value, font=value_f, fill=COLORS["text"])


def draw_print_front(w=CARD_W, h=CARD_H, bleed=False):
    img = card_bg(w, h)
    d = ImageDraw.Draw(img)
    margin = round(6 * MM) + (BLEED if bleed else 0)
    if bleed:
        trim = (BLEED, BLEED, w - BLEED, h - BLEED)
        d.rectangle(trim, outline=rgba(COLORS["white"], 24), width=1)

    draw_logo(d, margin, margin + round(2 * MM), 68 if not bleed else 72)
    d.text((margin, margin + round(17 * MM)), DATA["tagline"], font=font(28, "bold"), fill=COLORS["muted"])

    panel = (margin, h - margin - round(14 * MM), margin + round(61 * MM), h - margin - round(2 * MM))
    d.rounded_rectangle(panel, radius=18, fill=rgba(COLORS["panel"], 238), outline=rgba(COLORS["purple"], 140), width=2)
    center_text(d, panel, "Sites profissionais · Apps · WhatsApp", font(23, "bold"), COLORS["text"])
    d.text((margin, h - margin + round(3 * MM)), DATA["site"], font=font(19, "bold"), fill=COLORS["muted"])
    return img.convert("RGB")


def draw_print_back(w=CARD_W, h=CARD_H, bleed=False):
    img = card_bg(w, h, COLORS["blue"])
    d = ImageDraw.Draw(img)
    margin = round(6 * MM) + (BLEED if bleed else 0)
    if bleed:
        trim = (BLEED, BLEED, w - BLEED, h - BLEED)
        d.rectangle(trim, outline=rgba(COLORS["white"], 24), width=1)

    d.text((margin, margin + round(1 * MM)), DATA["name"], font=fit_font(d, DATA["name"], 40, "black", round(55 * MM), 26), fill=COLORS["text"])
    d.text((margin, margin + round(9 * MM)), DATA["title"], font=font(23, "bold"), fill=COLORS["blue"])
    d.line((margin, margin + round(15 * MM), margin + round(45 * MM), margin + round(15 * MM)), fill=COLORS["blue"], width=3)

    row_y = margin + round(18 * MM)
    draw_contact_row(d, margin, row_y, "WhatsApp", DATA["phone"], COLORS["blue"], round(52 * MM), 22)
    draw_contact_row(d, margin, row_y + round(9 * MM), "E-mail", DATA["email"], COLORS["blue"], round(52 * MM), 22)
    draw_contact_row(d, margin, row_y + round(18 * MM), "Site", DATA["site"], COLORS["blue"], round(52 * MM), 22)

    qr_size = round(21 * MM)
    qr_box_x = w - margin - qr_size
    qr_box_y = margin + round(8 * MM)
    d.rounded_rectangle((qr_box_x - 10, qr_box_y - 10, qr_box_x + qr_size + 10, qr_box_y + qr_size + 10), radius=14, fill=COLORS["paper"])
    qri = qr_image(DATA["site_url"], qr_size)
    img.paste(qri, (qr_box_x, qr_box_y))
    center_text(d, (qr_box_x - 12, qr_box_y + qr_size + 12, qr_box_x + qr_size + 12, qr_box_y + qr_size + 42), "site + portfólio", font(16, "bold"), COLORS["muted"])

    d.text((w - margin - round(30 * MM), h - margin - round(3 * MM)), DATA["instagram"], font=font(20, "bold"), fill=COLORS["muted"])
    return img.convert("RGB")


def draw_crop_marks(d, x, y, w, h):
    mark = round(4 * MM)
    gap = round(1.5 * MM)
    color = (45, 45, 55)
    width = 2
    corners = [
        (x, y, -1, -1),
        (x + w, y, 1, -1),
        (x, y + h, -1, 1),
        (x + w, y + h, 1, 1),
    ]
    for cx, cy, sx, sy in corners:
        d.line((cx + sx * gap, cy, cx + sx * (gap + mark), cy), fill=color, width=width)
        d.line((cx, cy + sy * gap, cx, cy + sy * (gap + mark)), fill=color, width=width)


def make_a4_sheet(card_img, name):
    sheet = Image.new("RGB", (A4_W, A4_H), COLORS["paper"])
    d = ImageDraw.Draw(sheet)
    cols, rows = 2, 5
    gap_x = round(5 * MM)
    gap_y = round(4 * MM)
    total_w = cols * CARD_W + (cols - 1) * gap_x
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


def make_duplex_pdf(front_sheet, back_sheet):
    path = OUT / f"folha-a4-duplex-10-cartoes-{SUFFIX}.pdf"
    front_sheet.save(path, "PDF", resolution=DPI, save_all=True, append_images=[back_sheet])


def make_print_files():
    front = draw_print_front()
    back = draw_print_back()
    front_bleed = draw_print_front(BLEED_W, BLEED_H, bleed=True)
    back_bleed = draw_print_back(BLEED_W, BLEED_H, bleed=True)

    save_image(front, "cartao-visita-frente-90x50mm", pdf=True)
    save_image(back, "cartao-visita-verso-90x50mm", pdf=True)
    save_image(front_bleed, "cartao-visita-frente-com-sangria-96x56mm", pdf=True)
    save_image(back_bleed, "cartao-visita-verso-com-sangria-96x56mm", pdf=True)

    front_sheet = make_a4_sheet(front, "folha-a4-frente-10-cartoes")
    back_sheet = make_a4_sheet(back, "folha-a4-verso-10-cartoes")
    make_duplex_pdf(front_sheet, back_sheet)


def make_virtual_card():
    w, h = 1080, 1920
    img = card_bg(w, h, COLORS["purple"])
    d = ImageDraw.Draw(img)
    margin = 74
    draw_logo(d, margin, 86, 58)
    d.text((margin, 158), DATA["tagline"], font=font(28, "bold"), fill=COLORS["muted"])

    y = 300
    d.text((margin, y), DATA["name"], font=fit_font(d, DATA["name"], 58, "black", 900, 36), fill=COLORS["text"])
    d.text((margin, y + 70), DATA["title"], font=font(32, "bold"), fill=COLORS["purple2"])
    d.line((margin, y + 124, margin + 220, y + 124), fill=COLORS["purple"], width=4)

    y = 475
    y = draw_wrapped(d, "Criação de sites, apps e presença digital para negócios que querem vender melhor.", margin, y, font(34, "bold"), COLORS["text"], 900, 12)
    y = draw_wrapped(d, "Atendimento direto pelo WhatsApp, orçamento sem compromisso e soluções sob medida para cada fase do negócio.", margin, y + 26, font(30), COLORS["muted"], 870, 14)

    qsize = 360
    qx, qy = margin, y + 82
    d.rounded_rectangle((qx - 18, qy - 18, qx + qsize + 18, qy + qsize + 18), radius=26, fill=COLORS["paper"])
    img.paste(qr_image(VCARD, qsize), (qx, qy))
    d.text((qx + qsize + 46, qy + 8), "Salvar contato", font=font(42, "black"), fill=COLORS["text"])
    draw_wrapped(d, "Escaneie o QR ou envie o arquivo .vcf junto com este cartão.", qx + qsize + 46, qy + 66, font(27), COLORS["muted"], 480, 10)

    contact_y = qy + qsize + 95
    rows = [
        ("WhatsApp", DATA["phone"]),
        ("E-mail", DATA["email"]),
        ("Site", DATA["site"]),
        ("Instagram", DATA["instagram"]),
    ]
    for label, value in rows:
        d.rounded_rectangle((margin, contact_y, w - margin, contact_y + 86), radius=18, fill=rgba(COLORS["panel"], 242), outline=rgba(COLORS["purple"], 85), width=1)
        d.text((margin + 28, contact_y + 17), label.upper(), font=font(17, "bold"), fill=COLORS["purple2"])
        d.text((margin + 28, contact_y + 42), value, font=fit_font(d, value, 30, "bold", 780, 20), fill=COLORS["text"])
        contact_y += 104

    d.rounded_rectangle((margin, h - 178, w - margin, h - 94), radius=18, fill=rgba(COLORS["panel"], 248), outline=rgba(COLORS["purple"], 220), width=2)
    center_text(d, (margin, h - 178, w - margin, h - 94), "helphstudio.com.br", font(34, "black"), COLORS["text"])

    save_image(img.convert("RGB"), "cartao-visita-virtual-whatsapp", pdf=False)


def make_virtual_html():
    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Pedro Henrique Pereira - Helph Studio</title>
  <style>
    :root {{ color-scheme: dark; --bg:#0a0a0f; --panel:#18181f; --text:#f0f0f5; --muted:#9696ae; --accent:#a78bfa; --accent2:#7c5cfc; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; min-height:100vh; display:grid; place-items:center; padding:24px; font-family:Arial, sans-serif; background:radial-gradient(circle at top,#201832 0,#0a0a0f 58%); color:var(--text); }}
    main {{ width:min(460px,100%); border:1px solid rgba(167,139,250,.28); border-radius:24px; padding:28px; background:rgba(24,24,31,.88); box-shadow:0 24px 80px rgba(0,0,0,.45); }}
    h1 {{ margin:0; font-size:34px; line-height:1; letter-spacing:-1px; }}
    .logo span {{ color:var(--accent); }}
    .tag {{ margin:8px 0 28px; color:var(--muted); font-weight:700; }}
    h2 {{ margin:0; font-size:28px; line-height:1.08; }}
    .role {{ margin:8px 0 22px; color:var(--accent); font-weight:800; }}
    p {{ color:var(--muted); line-height:1.6; }}
    a {{ display:flex; justify-content:space-between; align-items:center; gap:14px; padding:15px 16px; margin-top:12px; border:1px solid rgba(167,139,250,.24); border-radius:14px; color:var(--text); text-decoration:none; font-weight:800; background:#111118; }}
    a small {{ color:var(--muted); font-weight:700; }}
  </style>
</head>
<body>
  <main>
    <h1 class="logo">Hel<span>ph</span> Studio</h1>
    <div class="tag">{DATA["tagline"]}</div>
    <h2>{DATA["name"]}</h2>
    <div class="role">{DATA["title"]}</div>
    <p>Sites, apps e presença digital para negócios locais, autônomos e profissionais liberais.</p>
    <a href="{DATA["whatsapp_url"]}">WhatsApp <small>{DATA["phone"]}</small></a>
    <a href="mailto:{DATA["email"]}">E-mail <small>{DATA["email"]}</small></a>
    <a href="{DATA["site_url"]}">Site <small>{DATA["site"]}</small></a>
    <a href="{DATA["instagram_url"]}">Instagram <small>{DATA["instagram"]}</small></a>
    <a href="pedro-henrique-pereira-helph-studio-{SUFFIX}.vcf" download>Salvar contato <small>.vcf</small></a>
  </main>
</body>
</html>"""
    (OUT / f"cartao-virtual-html-{SUFFIX}.html").write_text(html, encoding="utf-8")


def save_image(img, stem, pdf=False):
    png = OUT / f"{stem}-{SUFFIX}.png"
    jpg = OUT / f"{stem}-{SUFFIX}.jpg"
    img.save(png)
    img.save(jpg, quality=94, optimize=True)
    if pdf:
        img.save(OUT / f"{stem}-{SUFFIX}.pdf", "PDF", resolution=DPI)


def write_vcard():
    (OUT / f"pedro-henrique-pereira-helph-studio-{SUFFIX}.vcf").write_text(VCARD, encoding="utf-8")


def write_guide():
    text = f"""# Cartão de visita - Helph Studio

Versão: {VERSION}

## Impressão

- `cartao-visita-frente-90x50mm-*` e `cartao-visita-verso-90x50mm-*`: cartão final no tamanho padrão 90x50 mm, 300 DPI.
- `cartao-visita-*-com-sangria-96x56mm-*`: versão com 3 mm de sangria para gráfica.
- `folha-a4-frente-10-cartoes-*` e `folha-a4-verso-10-cartoes-*`: folhas A4 com 10 cartões para imprimir e cortar.
- `folha-a4-duplex-10-cartoes-*`: PDF com duas páginas, frente e verso, para impressão duplex/manual.

## Digital

- `cartao-visita-virtual-whatsapp-*`: imagem vertical para enviar pelo WhatsApp ou Instagram.
- `pedro-henrique-pereira-helph-studio-*.vcf`: arquivo de contato para a pessoa salvar no celular.
- `cartao-virtual-html-*`: versão clicável, útil se futuramente quiser hospedar como página/link.

## Sugestões rápidas

- Envie a imagem virtual junto com o `.vcf` no WhatsApp.
- Use o QR do cartão impresso para levar a pessoa ao site/portfólio.
- Se for imprimir em gráfica, use a versão com sangria.
"""
    (OUT / f"guia-cartao-visita-{SUFFIX}.md").write_text(text, encoding="utf-8")


def main():
    make_print_files()
    make_virtual_card()
    make_virtual_html()
    write_vcard()
    write_guide()


if __name__ == "__main__":
    main()
