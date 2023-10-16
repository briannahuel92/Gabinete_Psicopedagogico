// Tipos de Asuntos:
textoAsuntos = {
  "1": 'Servicios',
  "2": 'Actividades',
  "3": 'Profesionales',
  "4": 'Postulaciones'
};

// Cargo todos los elementos html:
var nombre = document.getElementById('nombre');
var email = document.getElementById('email');
var asunto = document.getElementById('asunto');
var comentarios = document.getElementById('comentarios');
var enviar = document.getElementById('enviar');
var borrar = document.getElementById('borrar');
enviar.disabled = true;

// Defino todas las validaciones:
function invNombre() {
  return (nombre.value == '');
};

function invEmail() {
  return (email.value == '');
};

function invAsunto() {
  return (asunto.value == '');
}

function invComents() {
  return (comentarios.value == '');
};

// Defino todos los onChange:
function algunChange(event) {
//  console.log('Cambio en: ' + event.target.id + ' : ' + event.target.value);
  enviar.disabled = invNombre() || invEmail() || invAsunto() || invComents();
};

function enviarClick(event) {
  //console.log(event.target);
  var miStr = 'Preparando para Submitear:\n\n';
  miStr += 'Nombre: ' + nombre.value + '\n';
  miStr += 'Email: ' + email.value + '\n';
  miStr += 'Asunto: ' + asunto.value + ': ' + textoAsuntos[asunto.value] + '\n';
  miStr += 'Comentarios: ' + comentarios.value + '\n';
  alert(miStr);
};

// Activo todos los onChange:
nombre.addEventListener("input", algunChange);
email.addEventListener('input', algunChange);
asunto.addEventListener('input', algunChange);
comentarios.addEventListener('input', algunChange);
enviar.addEventListener("click", enviarClick);
