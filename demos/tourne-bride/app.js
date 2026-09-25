const dialog = document.querySelector('#reserva');
document.querySelectorAll('[data-reserva]').forEach(button => button.addEventListener('click', () => dialog.showModal()));
document.querySelectorAll('.close, #voltar').forEach(button => button.addEventListener('click', () => dialog.close()));
dialog.addEventListener('click', event => { if (event.target === dialog) { const r = dialog.getBoundingClientRect(); if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close(); } });

const header = document.querySelector('header');
const hero = document.querySelector('.hero');
let scrollQueued = false;
function updateHeader() {
  // Change only once the opening image has fully passed the top of the screen.
  header.classList.toggle('is-scrolled', hero.getBoundingClientRect().bottom <= 0);
  scrollQueued = false;
}
window.addEventListener('scroll', () => {
  if (!scrollQueued) { scrollQueued = true; requestAnimationFrame(updateHeader); }
}, { passive: true });
window.addEventListener('resize', updateHeader);
updateHeader();

const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
const slides = [...document.querySelectorAll('.hero-slide')];
const slideCount = document.querySelector('.slide-count');
const playButton = document.querySelector('.slide-play');
let slideIndex = 0;
let paused = motionPreference.matches;
let slideshowTimer;
function showSlide(index) {
  slideIndex = (index + slides.length) % slides.length;
  slides.forEach((slide, i) => {
    slide.classList.toggle('is-active', i === slideIndex);
    slide.setAttribute('aria-hidden', String(i !== slideIndex));
  });
  slideCount.textContent = `${slideIndex + 1} / ${slides.length}`;
}
function scheduleSlideshow() {
  clearInterval(slideshowTimer);
  playButton.textContent = paused ? 'Reproduzir' : 'Pausar';
  playButton.setAttribute('aria-label', paused ? 'Reproduzir troca automática de fotos' : 'Pausar troca automática de fotos');
  if (!paused && !document.hidden) slideshowTimer = setInterval(() => showSlide(slideIndex + 1), 6000);
}
document.querySelector('.slide-prev').addEventListener('click', () => { showSlide(slideIndex - 1); scheduleSlideshow(); });
document.querySelector('.slide-next').addEventListener('click', () => { showSlide(slideIndex + 1); scheduleSlideshow(); });
playButton.addEventListener('click', () => { paused = !paused; scheduleSlideshow(); });
document.addEventListener('visibilitychange', scheduleSlideshow);
motionPreference.addEventListener('change', event => { paused = event.matches; scheduleSlideshow(); });
scheduleSlideshow();
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
