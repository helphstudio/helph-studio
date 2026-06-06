# Changelog — Helph Studio

Todas as mudanças relevantes do projeto são documentadas aqui.  
Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).  
Versionamento seguindo [Semantic Versioning](https://semver.org/).

---

## [2.0.0] — 2026-06-05

### Adicionado
- **Seção de manutenção e suporte técnico** (`#manutencao`) com 3 planos mensais: Essencial, Profissional e Premium
- **Carrossel 3D coverflow** no portfólio de demos — 8 nichos com perspectiva 3D, auto-avanço a cada 4s, setas de navegação e swipe touch
- **Portfólio de clientes** atualizado: FC Serviços Ar Condicionado adicionado (card com badge "Em desenvolvimento")
- **Card fantasma** "Novo projeto chegando em breve" no portfólio
- **Aviso de personalização** na seção de demos (chip: "🎨 Estes são exemplos de referência...")
- **Demos de novos nichos**: barbearia, padaria, pet shop, veterinária, advocacia
- **Página de privacidade** (`privacidade.html`) e sistema de consentimento LGPD (`cookie-consent.js`)
- **`.gitignore`** excluindo `.wrangler/` e `node_modules/`
- **`package.json`** com versão semântica e scripts de dev/deploy
- **`CHANGELOG.md`** (este arquivo)

### Alterado
- **Ordem das seções** reorganizada em funil de conversão AIDA:  
  Hero → Por que → Portfólio → Como funciona → Preços → Apps → Manutenção → FAQ → Quem faz
- **Seção de portfólio** — badge "Demo ao vivo" removido dos cards do carrossel
- **Botões de nicho** — agora funcionam como atalhos de navegação no carrossel
- **`wrangler.toml`** — excludes corrigidos para não subir `.git/` e `.wrangler/` como assets públicos
- **`wranglerignore`** — atualizado com exclusões de scripts e arquivos internos

### Corrigido
- Arquivos `.git/objects/` e `.wrangler/tmp/` eram enviados como assets estáticos para o Cloudflare

---

## [1.3.0] — 2026-06-04

### Adicionado
- 16 peças publicitárias para redes sociais (feeds e stories)
- Capa WhatsApp com Helph Booking e Apps Web

### Corrigido
- Sobreposição no feed-02
- Screenshot real no feed-07
- Botão e preço corrigidos em story-02

---

## [1.2.0] — 2026-06-03

### Adicionado
- Landing page Helph Booking (`helph-booking.html`)
- Landing page Cardápio Digital (`cardapio-digital.html`)
- Demo Pacote Completo com blog multi-página (`demo-pacote-completo.html`)
- Posts de blog de demonstração (`blog/`)

---

## [1.1.0] — anterior

### Adicionado
- Seção de Apps (Helph Booking + App sob medida)
- FAQ expandível com 9 perguntas
- Seção "Quem faz" com perfil do fundador
- Portfolio com cliente real: Par Perfeito Assessoria de Eventos
- Demo Pacote Presença (Studio Bella — Salão de Beleza)
- Demo Pacote Profissional (Cantina Bella Vista — Restaurante)

---

## [1.0.0] — lançamento inicial

### Adicionado
- Site institucional completo: Hero, Por que investir, Como funciona, Planos, Portfólio, FAQ
- 3 planos de criação de sites: Presença (R$599,90), Profissional (R$999,90), Completo (R$1.499,90)
- Design dark theme com paleta roxa (#7c5cfc) e tipografia Inter
- Responsivo mobile-first
- Deploy na Cloudflare Workers com domínio `helphstudio.com.br`
- Schema.org LocalBusiness para SEO
- Integração WhatsApp com mensagens pré-preenchidas por contexto
