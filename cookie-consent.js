/**
 * Helph Studio — Banner de Consentimento LGPD
 * Salva preferência em localStorage (chave: helph_cookie_consent)
 * Valores: "accepted" | "essential"
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'helph_cookie_consent';

  // Se já respondeu, não exibe o banner
  if (localStorage.getItem(STORAGE_KEY)) return;

  /* ── Estilos ─────────────────────────────────────────────────── */
  var css = `
    #helph-cookie-banner {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      z-index: 99999;
      background: #0f0f1a;
      border-top: 1px solid rgba(124, 58, 237, 0.35);
      padding: 14px 20px;
      display: flex;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
      font-family: 'Inter', 'DM Sans', Arial, sans-serif;
      font-size: 13px;
      color: #c8c8d8;
      box-shadow: 0 -4px 24px rgba(0,0,0,0.45);
      animation: helphSlideUp 0.35s ease;
    }
    @keyframes helphSlideUp {
      from { transform: translateY(100%); opacity: 0; }
      to   { transform: translateY(0);    opacity: 1; }
    }
    #helph-cookie-banner p {
      margin: 0;
      flex: 1;
      min-width: 200px;
      line-height: 1.5;
    }
    #helph-cookie-banner a {
      color: #a78bfa;
      text-decoration: underline;
      white-space: nowrap;
    }
    #helph-cookie-banner .helph-cookie-actions {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      align-items: center;
    }
    #helph-cookie-banner button {
      cursor: pointer;
      border: none;
      border-radius: 6px;
      padding: 8px 18px;
      font-size: 13px;
      font-weight: 600;
      font-family: inherit;
      white-space: nowrap;
      transition: opacity 0.2s;
    }
    #helph-cookie-banner button:hover { opacity: 0.85; }
    #helph-cookie-btn-accept {
      background: #7c3aed;
      color: #fff;
    }
    #helph-cookie-btn-essential {
      background: transparent;
      color: #c8c8d8;
      border: 1px solid rgba(200,200,216,0.3) !important;
    }
  `;

  var style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  /* ── HTML ────────────────────────────────────────────────────── */
  var banner = document.createElement('div');
  banner.id = 'helph-cookie-banner';
  banner.setAttribute('role', 'region');
  banner.setAttribute('aria-label', 'Aviso de cookies');
  banner.innerHTML = `
    <p>
      Usamos recursos externos (como fontes do Google) que podem registrar seu IP.
      Ao continuar navegando, você concorda com nossa
      <a href="/privacidade.html" target="_blank" rel="noopener">Política de Privacidade</a>.
    </p>
    <div class="helph-cookie-actions">
      <button id="helph-cookie-btn-essential">Apenas essenciais</button>
      <button id="helph-cookie-btn-accept">Aceitar tudo</button>
    </div>
  `;
  document.body.appendChild(banner);

  /* ── Ações ───────────────────────────────────────────────────── */
  function dismiss(value) {
    localStorage.setItem(STORAGE_KEY, value);
    banner.style.animation = 'none';
    banner.style.transition = 'opacity 0.3s, transform 0.3s';
    banner.style.opacity = '0';
    banner.style.transform = 'translateY(20px)';
    setTimeout(function () { banner.remove(); }, 320);
  }

  document.getElementById('helph-cookie-btn-accept').addEventListener('click', function () {
    dismiss('accepted');
  });

  document.getElementById('helph-cookie-btn-essential').addEventListener('click', function () {
    dismiss('essential');
  });
})();
