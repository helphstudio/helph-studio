const dialog = document.querySelector('#reserva');
document.querySelectorAll('[data-reserva]').forEach(button => button.addEventListener('click', () => dialog.showModal()));
document.querySelectorAll('.close, #voltar').forEach(button => button.addEventListener('click', () => dialog.close()));
dialog.addEventListener('click', event => { if (event.target === dialog) { const r = dialog.getBoundingClientRect(); if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close(); } });

const header = document.querySelector('header');
let scrollQueued = false;
function updateHeader() {
  // Hysteresis keeps the header stable near the transition point.
  const compact = header.classList.contains('is-scrolled');
  header.classList.toggle('is-scrolled', compact ? window.scrollY > 32 : window.scrollY > 72);
  scrollQueued = false;
}
window.addEventListener('scroll', () => {
  if (!scrollQueued) { scrollQueued = true; requestAnimationFrame(updateHeader); }
}, { passive: true });
updateHeader();

const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
if ('IntersectionObserver' in window && !motionPreference.matches) {
  const targets = document.querySelectorAll('.hero-content > *, .hero-foot, .highlights > *, .intro > div > *, .intro figure, .section-head > div > *, .section-head > p, .cards article, .destination > *, .cta > *, footer > *, .disclosure');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -24px 0px' });
  targets.forEach((element, index) => {
    element.classList.add('reveal');
    element.style.setProperty('--reveal-delay', `${(index % 3) * 75}ms`);
    observer.observe(element);
  });
  motionPreference.addEventListener('change', event => {
    if (event.matches) { observer.disconnect(); targets.forEach(element => element.classList.add('is-visible')); }
  });
  document.addEventListener('focusin', event => {
    const target = event.target.closest('.reveal');
    if (target) target.classList.add('is-visible');
  });
}
