let miHeader=`

<nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-too">
    <div class="container">

        <div class="iconoConsultorio">
            <img src="./img/icono.png" class="img-fluid" alt="">
        </div>
        
        <div class="logoytitulo">
            <a href="#" class="navbar-brand"><span class="text-primary"></span>Gabinete
                Psicopedagógico</a>
            <h5>San Pablo</h5>
        </div>


        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarS"
            aria-controls="navbarS" aria-expanded="false" aria-label="Toggle navigation">

            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarS">
            <ul class="navbar-nav ms-auto mb-2 mb-lg-0">`


if (sessionStorage.getItem('isLogged') == "no" || sessionStorage.getItem('isLogged') == null)
{
    miHeader = miHeader + 
    `<li class="nav-item">
    <a href="./login.html" class="nav-link">Iniciar Sesión</a>
    </li>`
}
else
{
    miHeader = miHeader + 
    `<li class="nav-item">
    <a href="Javascript:desconectarse()" class="nav-link">Desconectarse</a>
    </li>`
}

miHeader = miHeader + `
                <li class="nav-item">
                    <a href="./index.html" class="nav-link">Quienes somos</a>
                </li>
                <li class="nav-item">
                    <a href="./index.html#Servicios" class="nav-link">Servicios</a>
                </li>
                <li class="nav-item">
                    <a href="./index.html#PruebasRealizadas" class="nav-link">Pruebas Realizadas en el
                        Centro</a>
                </li>
                <!--<li class="nav-item">
                    <a href="#" class="nav-link">Integracion</a>
                </li> -->
                <li class="nav-item">
                    <a href="./profesionales.html" class="nav-link">Profesionales</a>
                </li>
                <li class="nav-item">
                    <a href="./contacto.html" class="nav-link">Contacto</a>
                </li>`

if (sessionStorage.getItem('isLogged') == "si")
{
    miHeader = miHeader + 
    `<div class="panelLoginUser">
       <p>MODO ADMIN</p>
    </div>`
}

miHeader = miHeader + `

            </ul>
        </div>
    </div>

</nav>

`

document.querySelector("header").innerHTML=miHeader;

