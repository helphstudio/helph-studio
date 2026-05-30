# Helph Studio — Site Institucional

Site da **Helph Studio**, agência de criação de sites profissionais para negócios locais, profissionais liberais, freelancers e empreendedores individuais.

🌐 **URL de produção:** [helphstudio.com.br](https://www.helphstudio.com.br)

---

## Sobre o projeto

Landing page estática (HTML + CSS + JS puro) focada em conversão. O visitante conhece o serviço, vê o portfólio, tira dúvidas e solicita orçamento diretamente pelo WhatsApp.

**Stack:** HTML5 · CSS3 · JavaScript vanilla · Python HTTP server (dev)

---

## Estrutura

```
/
├── index.html          # Página principal
├── musicas.html        # Página de curadoria musical
├── assets/
│   └── img/
│       ├── helph-logo.png
│       ├── pedro.png               # Foto do fundador
│       └── parperfeito-preview.jpg # Screenshot do portfólio
└── CNAME               # Domínio customizado (GitHub Pages)
```

---

## Seções da página

| Seção | Descrição |
|---|---|
| Hero | Headline, subtítulo, CTAs e stats animados |
| Por que investir | 6 cards com benefícios de ter um site |
| Como funciona | Processo em 4 etapas |
| Portfólio | Cases com preview real + hover scroll |
| Orçamento | Proposta personalizada + promoção de lançamento |
| FAQ | 7 perguntas frequentes |
| Formulário | Orçamento via WhatsApp com campos pré-preenchidos |
| Quem está por trás | Fundador Pedro Henrique |

---

## Desenvolvimento local

Requer Python 3.x instalado.

```bash
python -m http.server 3000 --directory .
```

Acesse em `http://localhost:3000`

---

## Branches

| Branch | Descrição |
|---|---|
| `main` | Produção (GitHub Pages) |
| `dev` | Desenvolvimento — alterações entram aqui antes de ir para main |

---

## Deploy

O site é hospedado via **GitHub Pages** com domínio customizado configurado no arquivo `CNAME`.

Para publicar: abrir PR de `dev` → `main` e fazer merge.

---

## Contato

✉ helphstudio@gmail.com · 📱 (21) 97134-9275 · [LinkedIn](https://www.linkedin.com/in/pereirapedrohs/)
