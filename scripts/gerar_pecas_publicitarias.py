from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
VERSION = "2026-06-03-v2"
FILE_SUFFIX = "v2-20260603"
OUT = ROOT / "assets" / "img" / "publicidade" / VERSION
OUT.mkdir(parents=True, exist_ok=True)

FONT_REG = "C:/Windows/Fonts/arial.ttf"
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_BLACK = "C:/Windows/Fonts/ariblk.ttf"

COLORS = {
    "bg": (10, 10, 15),
    "bg2": (17, 17, 24),
    "panel": (24, 24, 31),
    "panel2": (20, 20, 28),
    "text": (240, 240, 245),
    "muted": (150, 150, 174),
    "muted2": (88, 88, 112),
    "purple": (124, 92, 252),
    "purple2": (167, 139, 250),
    "blue": (125, 211, 252),
    "orange": (255, 107, 53),
    "orange2": (255, 140, 90),
    "white": (255, 255, 255),
}


def font(size, weight="regular"):
    path = FONT_REG
    if weight == "bold":
        path = FONT_BOLD
    if weight == "black":
        path = FONT_BLACK if Path(FONT_BLACK).exists() else FONT_BOLD
    return ImageFont.truetype(path, size)


def rgba(color, alpha=255):
    return (*color, alpha)


def text_size(d, text, fnt):
    box = d.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def fit_font(d, text, size, weight, max_w, min_size=12):
    while size > min_size:
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
            continue
        if line:
            lines.append(line)
        line = word
    if line:
        lines.append(line)
    return lines


def draw_wrapped(d, text, xy, fnt, fill, max_w, line_gap=10, align="left"):
    x, y = xy
    line_h = text_size(d, "Ag", fnt)[1] + line_gap
    for line in wrap_lines(d, text, fnt, max_w):
        lx = x
        if align == "center":
            lx = x + (max_w - d.textlength(line, font=fnt)) / 2
        d.text((lx, y), line, font=fnt, fill=fill)
        y += line_h
    return y


def base(w, h, accent_name):
    accent = COLORS[accent_name]
    img = Image.new("RGBA", (w, h), rgba(COLORS["bg"], 255))
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    d.rectangle((0, 0, w, h), fill=rgba(COLORS["bg2"], 36))
    d.line((0, 0, min(int(w * 0.38), 460), 0), fill=accent, width=max(4, w // 180))

    # Soft light, kept subtle so the ads remain premium rather than decorative.
    cx, cy = int(w * 0.52), int(-h * 0.12)
    max_r = max(w, h)
    for r in range(max_r, 0, -28):
        alpha = int(38 * (1 - r / max_r) ** 2)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=rgba(accent, alpha))

    for scale, alpha in [(0.34, 28), (0.25, 18)]:
        rr = int(w * scale)
        d.ellipse((w - rr * 0.68, -rr * 0.42, w + rr * 0.32, rr * 0.58), outline=rgba(accent, alpha), width=2)

    return Image.alpha_composite(img, layer)


def draw_brand(d, x, y, size=42, tagline=True):
    f = font(size, "black")
    d.text((x, y), "Hel", font=f, fill=COLORS["text"])
    x2 = x + d.textlength("Hel", font=f) - size * 0.08
    d.text((x2, y), "ph", font=f, fill=COLORS["purple2"])
    x3 = x2 + d.textlength("ph", font=f) + size * 0.15
    d.text((x3, y), "Studio", font=f, fill=COLORS["text"])
    if tagline:
        d.text((x, y + int(size * 1.18)), "Sites e aplicativos para negócios", font=font(max(15, int(size * 0.35)), "bold"), fill=COLORS["muted"])


def draw_price_panel(d, box, label, value, suffix, note, accent):
    x1, y1, x2, y2 = box
    d.rounded_rectangle((x1, y1 + 8, x2, y2 + 8), radius=24, fill=rgba((0, 0, 0), 92))
    d.rounded_rectangle(box, radius=24, fill=rgba(COLORS["panel"], 236), outline=rgba(accent, 125), width=2)
    d.rectangle((x1 + 2, y1 + 28, x1 + 7, y2 - 28), fill=accent)

    d.text((x1 + 34, y1 + 26), label, font=font(25, "bold"), fill=COLORS["muted"])
    value_f = fit_font(d, value, 62, "black", (x2 - x1) - 190, 42)
    vx = x1 + 34
    vy = y1 + 68
    d.text((vx, vy), value, font=value_f, fill=COLORS["text"])

    if suffix:
        suffix_f = font(26, "bold")
        d.text((vx + d.textlength(value, font=value_f) + 10, vy + 24), suffix, font=suffix_f, fill=COLORS["muted"])

    if note:
        d.text((x1 + 34, y2 - 40), note, font=font(22, "bold"), fill=accent)


def draw_cta(d, box, text, accent):
    x1, y1, x2, y2 = box
    h = y2 - y1
    radius = min(18, int(h * 0.24))
    d.rounded_rectangle((x1, y1 + 7, x2, y2 + 7), radius=radius, fill=rgba((0, 0, 0), 100))
    d.rounded_rectangle(box, radius=radius, fill=rgba(COLORS["panel"], 246), outline=rgba(accent, 220), width=2)
    d.rounded_rectangle((x1 + 2, y1 + 2, x1 + 11, y2 - 2), radius=5, fill=accent)

    arrow = int(h * 0.46)
    ax2 = x2 - 24
    ax1 = ax2 - arrow
    ay1 = y1 + (h - arrow) / 2
    ay2 = ay1 + arrow
    d.rounded_rectangle((ax1, ay1, ax2, ay2), radius=9, fill=rgba(accent, 42), outline=rgba(accent, 120), width=1)
    cy = (ay1 + ay2) / 2
    lw = max(2, int(h * 0.04))
    d.line((ax1 + arrow * 0.34, cy, ax2 - arrow * 0.34, cy), fill=accent, width=lw)
    d.line((ax2 - arrow * 0.42, cy - arrow * 0.18, ax2 - arrow * 0.28, cy, ax2 - arrow * 0.42, cy + arrow * 0.18), fill=accent, width=lw, joint="curve")

    fnt = fit_font(d, text, max(22, int(h * 0.36)), "bold", (x2 - x1) - arrow - 70, 18)
    text_box = (x1 + 28, y1, ax1 - 18, y2)
    center_text(d, text_box, text, fnt, COLORS["text"])


def phone_button(d, box, text, accent, fsize=13):
    d.rounded_rectangle(box, radius=(box[3] - box[1]) // 2, fill=accent)
    fnt = fit_font(d, text, fsize, "bold", (box[2] - box[0]) - 18, 9)
    center_text(d, box, text, fnt, COLORS["white"])


def draw_phone(d, x, y, w, h, accent, mode="site"):
    d.rounded_rectangle((x, y, x + w, y + h), radius=int(w * 0.14), fill=(14, 14, 24), outline=rgba(COLORS["white"], 42), width=3)
    d.rounded_rectangle((x + w * 0.34, y + 8, x + w * 0.66, y + 25), radius=8, fill=(6, 6, 12))

    sx, sy = x + int(w * 0.08), y + 42
    sw, sh = w - int(w * 0.16), h - 70
    d.rounded_rectangle((sx, sy, sx + sw, sy + sh), radius=18, fill=(22, 22, 36))

    if mode == "cardapio":
        local = COLORS["orange"]
        d.rectangle((sx, sy, sx + sw, sy + 56), fill=(26, 26, 46))
        fnt = fit_font(d, "Burguer House", 18, "bold", sw - 24, 12)
        d.text((sx + 12, sy + 16), "Burguer House", font=fnt, fill=COLORS["text"])

        labels = ["Lanches", "Bebidas", "Combos"]
        margin, gap = 12, 6
        tab_w = (sw - margin * 2 - gap * 2) / 3
        for i, label in enumerate(labels):
            tx1 = sx + margin + i * (tab_w + gap)
            tx2 = tx1 + tab_w
            fill = local if i == 0 else (43, 43, 59)
            d.rounded_rectangle((tx1, sy + 70, tx2, sy + 94), radius=12, fill=fill)
            fnt = fit_font(d, label, 10, "bold", tab_w - 8, 8)
            center_text(d, (tx1, sy + 70, tx2, sy + 94), label, fnt, COLORS["white"] if i == 0 else COLORS["muted"])

        items = [("Burger Duplo", "R$ 39,90"), ("Batata Frita", "R$ 22,90"), ("Combo Casa", "R$ 52,90")]
        for i, (name, price) in enumerate(items):
            yy = sy + 116 + i * 72
            d.rounded_rectangle((sx + 12, yy, sx + sw - 12, yy + 58), radius=14, fill=(19, 29, 49))
            d.rounded_rectangle((sx + 22, yy + 10, sx + 64, yy + 48), radius=10, fill=rgba(local, 100))
            text_x = sx + 75
            max_text = sx + sw - 22 - text_x
            d.text((text_x, yy + 10), name, font=fit_font(d, name, 12, "bold", max_text, 9), fill=COLORS["text"])
            d.text((text_x, yy + 32), price, font=fit_font(d, price, 12, "bold", max_text, 9), fill=local)

    elif mode == "booking":
        local = COLORS["blue"]
        d.text((sx + 18, sy + 18), "Agendar horário", font=fit_font(d, "Agendar horário", 21, "bold", sw - 36, 13), fill=COLORS["text"])
        for i, item in enumerate(["Corte de cabelo", "Barba completa", "Hidratação"]):
            yy = sy + 72 + i * 78
            outline = rgba(local, 100) if i == 0 else None
            d.rounded_rectangle((sx + 16, yy, sx + sw - 16, yy + 58), radius=14, fill=(22, 27, 45), outline=outline, width=2)
            d.text((sx + 30, yy + 12), item, font=fit_font(d, item, 14, "bold", sw - 76, 10), fill=COLORS["text"])
            d.text((sx + 30, yy + 34), "30 min · R$ 40", font=font(11), fill=COLORS["muted"])
        phone_button(d, (sx + 28, sy + sh - 78, sx + sw - 28, sy + sh - 34), "Confirmar horário", COLORS["purple"], 13)

    else:
        d.rectangle((sx, sy, sx + sw, sy + 74), fill=(20, 20, 34))
        d.text((sx + 18, sy + 18), "Seu negócio", font=fit_font(d, "Seu negócio", 23, "bold", sw - 36, 14), fill=COLORS["text"])
        d.text((sx + 18, sy + 48), "online e profissional", font=fit_font(d, "online e profissional", 13, "regular", sw - 36, 10), fill=COLORS["muted"])
        for i, frac in enumerate([0.76, 0.62, 0.54, 0.48]):
            yy = sy + 104 + i * 54
            d.rounded_rectangle((sx + 18, yy, sx + sw - 18, yy + 34), radius=10, fill=(35, 35, 48))
            d.rounded_rectangle((sx + 30, yy + 13, sx + 30 + (sw - 96) * frac, yy + 19), radius=3, fill=rgba(accent, 155))
        phone_button(d, (sx + 28, sy + sh - 78, sx + sw - 28, sy + sh - 34), "WhatsApp", accent, 13)


def draw_bullets(d, x, y, bullets, accent, size=23, gap=38):
    for item in bullets:
        d.ellipse((x, y + 9, x + 12, y + 21), fill=accent)
        d.text((x + 28, y), item, font=font(size, "bold"), fill=COLORS["text"])
        y += gap


def square_asset(filename, title, subtitle, price, bullets, accent_name="purple", mode="site"):
    accent = COLORS[accent_name]
    img = base(1080, 1080, accent_name)
    d = ImageDraw.Draw(img)

    draw_brand(d, 70, 62, 42)
    title_y = 205
    y = draw_wrapped(d, title, (70, title_y), font(66, "black"), COLORS["text"], 625, line_gap=8)
    y = draw_wrapped(d, subtitle, (70, y + 22), font(29), COLORS["muted"], 600, line_gap=13)

    price_y = max(592, min(650, y + 45))
    draw_price_panel(d, (70, price_y, 650, price_y + 182), *price, accent)
    draw_bullets(d, 80, price_y + 220, bullets[:3], accent)

    draw_phone(d, 725, 235, 255, 535, accent, mode)
    draw_cta(d, (70, 982, 535, 1050), "Chamar no WhatsApp", accent)
    d.text((715, 1008), "@helphstudio", font=font(25, "bold"), fill=COLORS["muted"])

    save_all(img, filename)


def story_asset(filename, title, subtitle, price, accent_name="purple", mode="site"):
    accent = COLORS[accent_name]
    img = base(1080, 1920, accent_name)
    d = ImageDraw.Draw(img)

    draw_brand(d, 74, 74, 50)
    y = draw_wrapped(d, title, (74, 260), font(80, "black"), COLORS["text"], 850, line_gap=10)
    y = draw_wrapped(d, subtitle, (74, y + 28), font(34), COLORS["muted"], 815, line_gap=16)

    price_y = max(720, y + 70)
    draw_price_panel(d, (74, price_y, 1000, price_y + 190), *price, accent)
    phone_x = 598 if mode != "cardapio" else 600
    draw_phone(d, phone_x, 930, 310, 620, accent, mode)

    draw_cta(d, (74, 1632, 1000, 1720), "Peça seu orçamento", accent)
    d.text((74, 1772), "helphstudio.com.br  ·  (21) 97134-9275", font=font(28, "bold"), fill=COLORS["muted"])

    save_all(img, filename)


def landscape_asset(filename, title, subtitle, price, accent_name="purple", mode="site"):
    accent = COLORS[accent_name]
    img = base(1200, 628, accent_name)
    d = ImageDraw.Draw(img)

    draw_brand(d, 58, 42, 36)
    y = draw_wrapped(d, title, (58, 155), font(56, "black"), COLORS["text"], 695, line_gap=5)
    draw_wrapped(d, subtitle, (58, y + 14), font(25), COLORS["muted"], 650, line_gap=10)
    d.text((58, 454), price, font=font(32, "black"), fill=accent)
    draw_cta(d, (58, 524, 405, 588), "Falar no WhatsApp", accent)

    draw_phone(d, 855, 82, 220, 430, accent, mode)
    save_all(img, filename)


def catalog_asset(filename, service, audience, price, features, accent_name="purple", mode="site"):
    accent = COLORS[accent_name]
    img = base(1080, 1080, accent_name)
    d = ImageDraw.Draw(img)

    draw_brand(d, 70, 62, 42)
    draw_phone(d, 726, 125, 220, 440, accent, mode)

    y = draw_wrapped(d, service, (70, 228), font(68, "black"), COLORS["text"], 610, line_gap=7)
    draw_wrapped(d, audience, (70, y + 20), font(29), COLORS["muted"], 575, line_gap=13)

    d.text((70, 612), price, font=fit_font(d, price, 50, "black", 660, 36), fill=accent)

    by = 696
    for feat in features:
        d.rounded_rectangle((70, by, 930, by + 56), radius=17, fill=rgba(COLORS["panel"], 238), outline=rgba(accent, 58), width=1)
        d.ellipse((99, by + 19, 119, by + 39), fill=rgba(accent, 42), outline=accent, width=2)
        d.line((104, by + 29, 110, by + 35, 117, by + 23), fill=accent, width=3)
        d.text((138, by + 13), feat, font=fit_font(d, feat, 24, "bold", 760, 16), fill=COLORS["text"])
        by += 68

    draw_cta(d, (70, 986, 545, 1052), "Solicitar proposta", accent)
    save_all(img, filename)


def save_all(img, stem):
    png = OUT / f"{stem}-{FILE_SUFFIX}.png"
    jpg = OUT / f"{stem}-{FILE_SUFFIX}.jpg"
    if img.mode == "RGBA":
        bg = Image.new("RGBA", img.size, rgba(COLORS["bg"], 255))
        img = Image.alpha_composite(bg, img)
    img = img.convert("RGB")
    img.save(png, quality=95)
    img.save(jpg, quality=92, optimize=True)


def write_guide():
    guide = OUT / f"guia-de-postagem-{FILE_SUFFIX}.md"
    guide.write_text(
        """# Guia de postagem - Helph Studio v2

Versão: 2026-06-03-v2

Esta leva remove textos internos como "feed", "stories", "Meta Business" e "catálogo" das artes finais. Os nomes dos arquivos continuam indicando o melhor uso.

## Arquivos

- `feed-*.png/.jpg`: 1080x1080, indicado para Instagram, Facebook e catálogo visual.
- `story-*.png/.jpg` e `status-*.png/.jpg`: 1080x1920, indicado para Stories, Reels estático e Status do WhatsApp.
- `facebook-*.png/.jpg`: 1200x628, indicado para anúncios horizontais e links patrocinados.
- `catalogo-*.png/.jpg`: 1080x1080, indicado para serviços no catálogo do WhatsApp Business.

## Observações

- Use JPG para upload rápido em redes sociais.
- Use PNG quando quiser preservar máxima nitidez.
- Esta pasta é versionada para não sobrescrever a leva anterior.
""",
        encoding="utf-8",
    )


def main():
    square_asset(
        "feed-site-profissional",
        "Seu negócio merece um site profissional.",
        "Design moderno, carregamento rápido e botão direto para WhatsApp.",
        ("Sites a partir de", "R$ 599,90", "", "Oferta de lançamento"),
        ["Mobile-first", "SEO básico", "Entrega em até 7 dias"],
        "purple",
        "site",
    )
    square_asset(
        "feed-pacote-profissional",
        "Pacote Profissional: presença digital completa.",
        "Ideal para autônomos, negócios locais e profissionais liberais.",
        ("A partir de", "R$ 999,90", "", "Mais pedido"),
        ["4 a 5 seções", "Formulário + WhatsApp", "3 meses de suporte"],
        "purple",
        "site",
    )
    square_asset(
        "feed-helph-booking",
        "Agenda cheia sem bagunça no WhatsApp.",
        "Sistema de agendamento online para negócios com hora marcada.",
        ("Mensalidade", "R$ 39,90", "/mês", "Sem fidelidade"),
        ["Instala no celular", "Funciona offline", "Painel de controle"],
        "blue",
        "booking",
    )
    square_asset(
        "feed-cardapio-digital",
        "Seu cardápio no celular. Pedido pelo WhatsApp.",
        "O cliente escolhe, monta o pedido e envia tudo formatado.",
        ("Mensalidade", "R$ 29,90", "/mês", "50% de desconto"),
        ["Instalável", "Sem App Store", "Atualização fácil"],
        "orange",
        "cardapio",
    )

    story_asset(
        "story-sites",
        "Ainda atende cliente só pelo improviso?",
        "Um site profissional organiza sua presença digital e passa confiança antes da primeira mensagem.",
        ("Sites a partir de", "R$ 599,90", "", "Oferta de lançamento"),
        "purple",
        "site",
    )
    story_asset(
        "story-booking",
        "Agendamentos online, sem perder mensagem.",
        "Para barbearias, salões, clínicas, pet shops e qualquer negócio com hora marcada.",
        ("Helph Booking", "R$ 39,90", "/mês", "Sem fidelidade"),
        "blue",
        "booking",
    )
    story_asset(
        "story-cardapio",
        "Transforme seu cardápio em app.",
        "O cliente acessa pelo celular, salva na tela inicial e manda o pedido pelo WhatsApp.",
        ("Cardápio Digital", "R$ 29,90", "/mês", "50% de desconto"),
        "orange",
        "cardapio",
    )
    story_asset(
        "status-orcamento",
        "Tem uma ideia de site ou app?",
        "Me chama no WhatsApp. Eu avalio o escopo e monto uma proposta sem compromisso.",
        ("Orçamento", "Personalizado", "", "Sem compromisso"),
        "purple",
        "site",
    )

    landscape_asset(
        "facebook-sites",
        "Sites profissionais para pequenos negócios.",
        "Entrega rápida, design exclusivo e atendimento direto pelo WhatsApp.",
        "A partir de R$ 599,90",
        "purple",
        "site",
    )
    landscape_asset(
        "facebook-apps",
        "Apps simples para vender e organizar melhor.",
        "Agendamento online, cardápio digital e soluções sob medida para o seu negócio.",
        "A partir de R$ 29,90/mês",
        "blue",
        "booking",
    )

    catalog_asset(
        "catalogo-sites",
        "Criação de Sites",
        "Sites profissionais para negócios locais, autônomos e freelancers.",
        "A partir de R$ 599,90",
        ["Design exclusivo", "WhatsApp integrado", "SEO básico", "Entrega em até 7 dias"],
        "purple",
        "site",
    )
    catalog_asset(
        "catalogo-helph-booking",
        "Helph Booking",
        "Agendamento online para negócios com hora marcada.",
        "R$ 39,90/mês",
        ["Sem fidelidade", "Instala no celular", "Funciona offline", "Painel admin"],
        "blue",
        "booking",
    )
    catalog_asset(
        "catalogo-cardapio-digital",
        "Cardápio Digital",
        "Cardápio instalável com pedido direto pelo WhatsApp.",
        "R$ 29,90/mês",
        ["Pedido formatado", "Delivery, retirada ou mesa", "Instalável", "Suporte via WhatsApp"],
        "orange",
        "cardapio",
    )
    write_guide()


if __name__ == "__main__":
    main()
