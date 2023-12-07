
myProf = {}

const URL = "http://127.0.0.1:5000/"
//Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
//const URL = "https://USUARIO.pythonanywhere.com/"

const btnRevert = document.getElementById("btnRevert");
btnRevert.onclick = btnRevertClick;

let params = new URLSearchParams(document.location.search);
let codigo = params.get("codigo");

console.log("Iniciando ScriptModificaciones: codigo: " + codigo);

//alert("Hola DOS!!, codigo: " + codigo);

//alert(descargarProfesional(codigo));

function descargarProfesional(codigoProf) {
    fetch(URL + 'profesionales/' + codigoProf)
    //Realiza una solicitud de red al servidor para obtener
    // los datos del profesional. Usa la URL definida anteriormente
    // y añade 'profesionales/' seguido del código del profesional.
    .then(response =>  {
        //Si es así, utilizamos response.json() para parsear la respuesta en formato JSON.
        if (response.ok) {
            return response.json() //Una vez que la respuesta llega del servidor,
            // se convierte de formato JSON a un objeto JavaScript.
        } else {
            //Si la respuesta es un error, lanzamos una excepción para ser "catcheada"
            // más adelante en el catch.
            throw new Error('Error al obtener los datos del profesional.')
        }
    })

    //En este bloque, se asignan los datos obtenidos
    // al resultado
    .then(data => {
        myProf =  {
            apellido: data.apellido,
            nombre: data.nombre,
            especialidad: data.especialidad,
            matricula: data.matricula,
            imagen_url: data.imagen_url
        };
        console.log("myProf:");
        console.log(myProf);
    })

    //Si ocurre un error durante la solicitud, se captura y se imprime en la consola.
    .catch(error => {
        alert('Código no encontrado.')
    })
}

function btnRevertClick(evt) {
    evt.preventDefault();
    console.log("Revertir")
    console.log(myProf)
}




// onload = "startFunction()"

// function startFunction() {
//     alert("Modificar: Start Function, codigo: " + codigo);
// }

//        alert("Hola Mundo");
//        console.log("Iniciada Modificaciones..");
