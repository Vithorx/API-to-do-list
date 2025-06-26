from ninja import Router
from ..models import Usuario
from django.contrib.auth import authenticate
from ninja.errors import HttpError
from api_rest.schemas import UserSchema, UserRegisterSchema,ErrorSchema
from ninja_jwt.authentication import JWTAuth
from typing import List

router = Router(tags=["Usuarios"])

@router.post(
    "/registro",
    response= {201:UserSchema,400: ErrorSchema},
    summary="Registrar um novo usuario",
    auth=None,
)
def registro(request,payload:UserRegisterSchema):
    if Usuario.objects.filter(username=payload.username).exists():
        return 400,{"message":"Este nome de usuario ja existe."}
    
    if Usuario.objects.filter(email=payload.email).exists():
        return 400,{"message": "Este email ja esta em uso"}
    
    try:
        user = Usuario.objects.create_user(
            username=payload.email,
            email=payload.email,
            password=payload.password,
            idade = payload.idade,
            first_name = payload.first_name
        )
        return 201,user
    except Exception as e:
        return 400,{"message":f"Erro ao criar um usuario:{(e)}"}



@router.get("/getAll", response=List[UserSchema], auth=None,summary="Exibir todos os usuarios cadastrados")

def getAllUsers(request):
    user = Usuario.objects.all()
    return user