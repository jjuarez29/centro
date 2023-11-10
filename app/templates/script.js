// JavaScript para hacer scroll a la ventana correspondiente al hacer clic en el menú
document.querySelectorAll('#menu-lateral a').forEach(link => {
  link.addEventListener('click', function(e) {
    e.preventDefault();
    let ventanaID = this.getAttribute('href');
    let ventana = document.querySelector(ventanaID);
    ventana.scrollIntoView({ behavior: 'smooth' });
  });
});
