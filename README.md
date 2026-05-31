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
├── index.html                      # Página principal
├── agendamento-online.html         # Página de nicho: agendamento online
├── musicas.html                    # Página de curadoria musical
├── demo-pacote-presenca.html       # Demo: Pacote Presença (ex: Studio Bella)
├── demo-pacote-profissional.html   # Demo: Pacote Profissional
├── demo-pacote-completo.html       # Demo: Pacote Completo (com blog multi-página)
├── assets/
│   └── img/
│       ├── site/
│       │   ├── pedro.png                   # Foto do fundador
│       │   └── parperfeito-preview.jpg     # Screenshot do portfólio
│       └── marca/
│           ├── logos/
│           │   ├── helph-logo-horizontal.svg/.jpg
│           │   └── helph-logo-whatsapp.svg/.jpg
│           ├── whatsapp/
│           │   └── helph-capa-whatsapp.svg/.jpg
│           └── catalogo/
│               ├── catalogo-landing-page.svg/.jpg
│               ├── catalogo-manutencao.svg/.jpg
│               ├── catalogo-portfolio.svg/.jpg
│               ├── catalogo-profissional.svg/.jpg
│               └── catalogo-site-completo.svg/.jpg
└── CNAME                           # Domínio customizado (GitHub Pages)
```

---

## Páginas

| Arquivo | Descrição |
|---|---|
| `index.html` | Landing page principal com hero, planos, portfólio, FAQ e formulário |
| `agendamento-online.html` | Página de nicho focada em negócios com agendamento |
| `musicas.html` | Curadoria musical (página auxiliar) |
| `demo-pacote-presenca.html` | Demo do Pacote Presença — estilo salão de beleza (Studio Bella) |
| `demo-pacote-profissional.html` | Demo do Pacote Profissional |
| `demo-pacote-completo.html` | Demo do Pacote Completo com blog multi-página |

---

## Seções da página principal

| Seção | Descrição |
|---|---|
| Hero | Headline, subtítulo, CTAs e stats animados |
| Por que investir | 6 cards com benefícios de ter um site |
| Como funciona | Processo em 4 etapas |
| Planos | 3 cards de planos com preços |
| Portfólio | Cases com preview real + hover scroll |
| Orçamento | Proposta personalizada + promoção de lançamento |
| FAQ | Perguntas frequentes |
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
