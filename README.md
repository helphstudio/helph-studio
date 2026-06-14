# Helph Studio Soluções Digitais — Site Institucional

Site da **Helph Studio Soluções Digitais**, empresa de criação de sites e soluções digitais para negócios locais, profissionais liberais, freelancers e empreendedores.

🌐 **Produção:** [helphstudio.com.br](https://www.helphstudio.com.br)  
📦 **Versão atual:** `2.0.1` — ver [CHANGELOG.md](./CHANGELOG.md)

---

## Sobre o projeto

Landing page estática (HTML + CSS + JS puro) focada em conversão. O visitante conhece o serviço, vê o portfólio, tira dúvidas e solicita orçamento diretamente pelo WhatsApp.

**Stack:** HTML5 · CSS3 · JavaScript vanilla · Cloudflare Workers (deploy automático via GitHub)

---

## Estrutura

```
/
├── index.html                          # Página principal
├── helph-booking.html                  # Landing page: Helph Booking (agendamento)
├── cardapio-digital.html               # Landing page: Cardápio Digital
├── privacidade.html                    # Política de privacidade (LGPD)
├── cookie-consent.js                   # Banner de consentimento LGPD
│
├── demo-pacote-presenca.html           # Demo: Salão de Beleza (Studio Bella)
├── demo-pacote-profissional.html       # Demo: Restaurante (Cantina Bella Vista)
├── demo-pacote-completo.html           # Demo: Clínica Estética (Espaço Serenità) + blog
├── demo-barbearia.html                 # Demo: Barbearia (Kings Barber)
├── demo-padaria.html                   # Demo: Padaria (Padaria Grão)
├── demo-petshop.html                   # Demo: Pet Shop (PetAmor)
├── demo-veterinaria.html               # Demo: Veterinária (Vet Vida)
├── demo-advogado.html                  # Demo: Advocacia (Dr. Rodrigo Mendes)
│
├── blog/                               # Posts de blog (demo Pacote Completo)
│   ├── peeling-quimico.html
│   ├── radiofrequencia.html
│   └── skincare-verao.html
│
├── assets/
│   └── img/
│       ├── site/
│       │   ├── pedro.png                       # Foto do fundador
│       │   ├── parperfeito-preview.jpg         # Preview: Par Perfeito
│       │   └── fcservicos-preview.jpg          # Preview: FC Serviços
│       └── marca/
│           ├── logos/
│           │   ├── helph-logo-horizontal.svg/.jpg
│           │   └── helph-logo-whatsapp.svg/.jpg
│           └── whatsapp/
│               └── helph-capa-whatsapp.svg/.jpg
│
├── scripts/                            # Scripts utilitários (não sobem para produção)
│   ├── gerar_cartao_visita.py
│   ├── gerar_cartao_visita_claro.py
│   └── gerar_pecas_publicitarias.py
│
├── package.json                        # Versão semântica + scripts de dev/deploy
├── wrangler.toml                       # Configuração Cloudflare Workers
├── .wranglerignore                     # Exclusões do deploy
├── .gitignore
├── CHANGELOG.md                        # Histórico de versões
└── README.md                           # Este arquivo
```

---

## Seções da página principal (`index.html`)

| Ordem | Seção | ID | Descrição |
|-------|-------|----|-----------|
| 1 | Hero | — | Headline, subtítulo, CTAs e stats animados |
| 2 | Por que investir | `#por-que` | 6 cards com benefícios de ter presença digital |
| 3 | Portfólio — Clientes | `#portfolio` | Clientes reais com screenshots full-page |
| 4 | Portfólio — Demos | `#demos` | Carrossel 3D de exemplos por nicho |
| 5 | Como funciona | `#como-funciona` | Processo em 4 etapas |
| 6 | Preços | `#precos` | 3 pacotes de criação de sites |
| 7 | Apps | `#apps` | Helph Booking + App sob medida |
| 8 | Manutenção | `#manutencao` | Hospedagem, SSL, suporte e planos mensais |
| 9 | FAQ | `#faq` | Perguntas frequentes |
| 10 | Quem faz | — | Perfil do fundador |

---

## Portfólio de clientes reais

| Cliente | Nicho | Status | URL |
|---------|-------|--------|-----|
| Par Perfeito | Eventos & Assessoria | ✅ Ao vivo | [parperfeitoassessoria.com.br](https://parperfeitoassessoria.com.br) |
| FC Serviços | Ar Condicionado | ✅ Ao vivo | [fcservicos.helphstudio.com.br](https://fcservicos.helphstudio.com.br) |

> Para adicionar um novo cliente: duplicar um `.portfolio-card` existente na seção `#portfolio` do `index.html` e adicionar o screenshot em `assets/img/site/`.

---

## Demos por nicho (carrossel)

| Nicho | Arquivo | Estilo |
|-------|---------|--------|
| Salão de Beleza | `demo-pacote-presenca.html` | Rosa/elegante |
| Barbearia | `demo-barbearia.html` | Dark/masculino |
| Padaria | `demo-padaria.html` | Aconchegante/terra |
| Pet Shop | `demo-petshop.html` | Colorido/amigável |
| Veterinária | `demo-veterinaria.html` | Azul/confiança |
| Advocacia | `demo-advogado.html` | Formal/sóbrio |
| Restaurante | `demo-pacote-profissional.html` | Quente/gourmet |
| Estética | `demo-pacote-completo.html` | Premium/spa |

---

## Desenvolvimento local

```bash
# Python (sem dependências)
python -m http.server 3001 --directory .

# Ou via npm script (requer Node.js)
npm run dev
```

Acesse em `http://localhost:3001`

---

## Branches e deploy

| Branch | Função |
|--------|--------|
| `dev` | Desenvolvimento — todas as alterações entram aqui primeiro |
| `main` | Produção — push automático dispara deploy no Cloudflare Workers |

### Fluxo de trabalho

```
dev  →  PR  →  merge em main  →  Cloudflare Workers (auto-deploy ~1 min)
```

O deploy é automático via integração GitHub do Cloudflare Workers. Não é necessário rodar `wrangler deploy` manualmente.

### Como subir uma nova versão

```bash
# 1. Trabalhar na dev
git checkout dev
git add .
git commit -m "feat: descrição da mudança"
git push origin dev

# 2. Abrir PR no GitHub: dev → main
gh pr create --base main --head dev --title "descrição"

# 3. Após merge, o Cloudflare faz deploy automático
```

### URLs

| Ambiente | URL |
|----------|-----|
| Produção | https://www.helphstudio.com.br |
| Workers (interno) | https://helph-studio.helphstudio.workers.dev |
| Cloudflare Dashboard | https://dash.cloudflare.com → Workers & Pages → helph-studio |

---

## Versionamento

O projeto usa [Semantic Versioning](https://semver.org/):

- **MAJOR** — redesign completo ou mudança de produto
- **MINOR** — nova seção, novo demo, novo cliente, nova feature
- **PATCH** — correção de texto, ajuste visual, bugfix

Para lançar uma nova versão:
1. Atualizar `"version"` em `package.json`
2. Adicionar entrada em `CHANGELOG.md`
3. Commitar: `git commit -m "chore: bump version to X.Y.Z"`

---

## Contato

✉ helphstudio@gmail.com · 📱 (21) 97134-9275 · [LinkedIn](https://www.linkedin.com/in/pereirapedrohs/) · [Instagram](https://www.instagram.com/helphstudio/)
