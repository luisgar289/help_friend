from fastapi import Depends, FastAPI , HTTPException, status, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import pyrebase
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()


class Respuesta (BaseModel) :  
    message: str  
                
class UserIN(BaseModel):
    email       : str
    password    : str

class Cliente (BaseModel):  
    nombre: str  
    email: str  

class ClienteIN (BaseModel):  
    id_cliente: str
    nombre: str  
    email: str  
    

origins = [
    "http://0.0.0.0:8000/",
    "http://127.0.0.1:8000/",
    "*",   
            
    ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hola"}

firebaseConfig = {
  "apiKey": "AIzaSyBoM8UTB3QctzA873CuWBDWM_y7bGoo0bk",
  "authDomain": "fastapi-c5049.firebaseapp.com",
  "databaseURL": "https://fastapi-c5049-default-rtdb.firebaseio.com",
  "projectId": "fastapi-c5049",
  "storageBucket": "fastapi-c5049.appspot.com",
  "messagingSenderId": "552147332644",
  "appId": "1:552147332644:web:e04ce0f5335be5616832b1"
};

firebase = pyrebase.initialize_app(firebaseConfig)

securityBasic  = HTTPBasic()
securityBearer = HTTPBearer()

#Consigue el usuario autenticado en el token de autenticacion
@app.post(
    "/users/token",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Consigue un token para el usuario",
    description="Consigue un token para el usuario",
    tags=["auth"],
)

async def post_token(credentials: HTTPBasicCredentials = Depends(securityBasic)):
    try:
        email = credentials.username
        password = credentials.password
        auth = firebase.auth()
        user = auth.sign_in_with_email_and_password(email, password)
        
        response = {
            "token": user["idToken"]
        }
        return response
    except Exception as error:
        print(f"Error: {error}")
        return(f"Error: {error}")
        
#Consigue el usuario autenticado en el token de autenticacion
@app.get(
    "/users/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Consigue un usuario",
    description="Consigue un usuario",
    tags=["auth"]
)

async def get_user(credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    try:
        #token = credentials.credentials
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user["users"][0]["localId"]

        db=firebase.database()
        cliente = db.child("users").child(uid).get().val()

        response = {
            #"user": user,
            "cliente" : cliente
        }
        return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED           
        )
        

#Crea un usuario en la base de datos firebase
@app.post(  "/users/",  
    status_code=status.HTTP_202_ACCEPTED, 
    summary="Crea un usuario",
    description="Crea un usuario", 
    tags=["auth"]
)
async def create_user(usuario: UserIN ):
    try:
        auth = firebase.auth()
        db=firebase.database()
        user = auth.create_user_with_email_and_password(usuario.email, usuario.password)
        uid = user["localId"]
        db.child("users").child(uid).set({"email": usuario.email, "level": 1 })
        response = {"code": status.HTTP_201_CREATED, "message": "Usuario creado"}
        return response
    except Exception as error:
        print(f"Error: {error}")
        return(f"Error: {error}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )
        


#Obtiene una lista de clientes registrados
@app.get(
    "/clientes/", 
    status_code=status.HTTP_202_ACCEPTED,
    summary="Regresa una lista de usuarios",
    description="Regresa una lista de usuarios"
)
async def get_clientes(credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    try:
        db=firebase.database()
        clientes = db.child("clientes").get().val()
        response = {
            "clientes": clientes
        }
        return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No tienes permiso para ver estos datos",
            headers={"WWW-Authenticate": "Basic"},        
        )
    

#Obtiene un usuario por medio del id
@app.get(
    "/clientes/{id}", 
    status_code=status.HTTP_202_ACCEPTED,
    summary="Consigue un usuario",
    description="Consigue un usuario",
    tags=["auth"]
)
async def get_cliente_id(id_cliente: str, credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    try:       

        db=firebase.database()
        id=id_cliente
        print(id)
        cliente = db.child("clientes").child(id).get().val()

        response = {
            "cliente" : cliente
        }
        return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED           
        )

#Ingresa un nuevo usuario 
@app.post("/clientes/", 
    status_code=status.HTTP_202_ACCEPTED,
    summary="Inserta un usuario",
    description="Inserta un usuario",
    tags=["auth"]
)
async def post_clientes(cliente: Cliente, credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    try:
        db=firebase.database()
        db.child("clientes").push({"Nombre": cliente.nombre, "Email": cliente.email})
        response = {"code": status.HTTP_201_CREATED, "message": "Usuario creado"}
        return response
    except Exception as error:
        print(f"Error: {error}")
        return(f"Error: {error}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    
#Actualiza un usuario
@app.put(
    "/clientes/", 
    response_model=Respuesta,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Actualiza un usuario",
    description="Actualiza un usuario"
)
async def put_clientes(cliente:ClienteIN, credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    try:     
        db=firebase.database()
        db.child("clientes").child(cliente.id_cliente).update({"Nombre": cliente.nombre, "Email": cliente.email})
        response = {"message":"Cliente actualizado"}
        return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED           
        )
    
#Elimina un usuario
@app.delete(
    "/clientes/{id_cliente}", 
    response_model=Respuesta,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Elimina un usuario",
    description="Elimina un usuario",
    tags=["auth"]
)
async def delete_clientes(id_cliente: str, credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    try:       
        db=firebase.database()
        id=id_cliente
        print(id)
        db.child("clientes").child(id).remove()
        response = {"message":"Cliente eliminado"}
        return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED           
        )
    
