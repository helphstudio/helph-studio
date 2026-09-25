const dialog = document.querySelector('#reserva');
document.querySelectorAll('[data-reserva]').forEach(button => button.addEventListener('click', () => dialog.showModal()));
document.querySelectorAll('.close, #voltar').forEach(button => button.addEventListener('click', () => dialog.close()));
dialog.addEventListener('click', event => { if (event.target === dialog) { const r = dialog.getBoundingClientRect(); if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close(); } });
