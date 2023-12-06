function desconectarse(){
    sessionStorage.setItem('isLogged', 'no')
    location.href ="./index.html"
}

document.getElementById('formularioLogin').addEventListener('submit', function (event)
{
    event.preventDefault();
    
    let user;
    let pass;
    user = document.getElementById('usuario').value
    pass = document.getElementById('password').value

    if (user == 'admin' && pass == '123456')
    {
        sessionStorage.setItem('user', user)
        sessionStorage.setItem('isLogged', 'si')
        location.href ="./index.html"
    }
    else
    {
        sessionStorage.setItem('isLogged', 'no')
        alert("Usuario no existe")
    }
    
})
