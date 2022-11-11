function PostCliente(){

    const token = sessionStorage.getItem('token');
    console.log(token);
    
    let nombre = document.getElementById("nombre");
    let email  = document.getElementById("email");

    let payload = {
        "nombre": nombre.value,
        "email" : email.value,
    }

    /*console.log("nombre: " + nombre.value);
    console.log("email: "  + email.value);
    console.log(payload);*/
    
    var request = new XMLHttpRequest(); 
    request.open('POST', "http://0.0.0.0:8000/clientes/",true);
    request.setRequestHeader("accept", "application/json");
    request.setRequestHeader("Authorization", "Bearer " + btoa(token));
    request.setRequestHeader("Content-Type", "application/json");

    request.onload = () => {
        
        const response  = request.responseText;
        const json      = JSON.parse(response); 
        
        const status    = request.status;

        if (request.status === 401 || request.status === 403) {
            alert(json.detail);
        }

        else if (request.status == 202){

            console.log("Response: " + response);
            console.log("JSON: " + json);
            console.log("Status: " + status);

            Swal.fire({
                title: json.message,
                text: "Regresar a la lista de clientes ",
                type: "success"
            }).then(function() {
                window.location = "/templates/get_clientes.html";
            });
            
        }
    };
    request.send(JSON.stringify(payload));
};