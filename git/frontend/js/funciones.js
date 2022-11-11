const data = sessionStorage.getItem('token')
 
function Authentication(){
    console.log(data);
    if(data == null){
        Swal.fire({
        title: "No has iniciado sesion",
        text: "dirigete a la pagina de inicio para iniciar sesion",
        type: "error"
    }).then(function() {
        window.location = "/templates/login.html";
    });
    }

    if(data != null){
        Swal.fire({
            title: "Bienvenido",
            text: "Has iniciado sesion correctamente",
            type: "success"
        });
    }
}

function logout(){
    sessionStorage.clear(data)
    window.location = "/templates/login.html";
}


