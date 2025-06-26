from ninja import Router
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from ninja.errors import HttpError
from ..schemas import LoginSchema,TokenSChema,TokenRefreshInputSchema,UserSchema,ErrorSchema,LoginResponseSchema
from ..models import Usuario
from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404
from django.http import Http404

router = Router(tags=["Autenticação"])

@router.post(
    "/login",
    response={200:LoginResponseSchema,401: ErrorSchema},
    summary="Login do Usuario",
    auth=None,
)
def login(request,data:LoginSchema):
    user = authenticate(email= data.email,password=data.password)
    if not user:
        return 401,{"message":"E-mail ou senha invalidas"}
    user_data_para_json = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name
    }
    refresh = RefreshToken.for_user(user)
    return{
        "tokens":{
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        },
        "user": user_data_para_json,
    }

@router.post(
    "/refresh_token",
    response={200:TokenSChema,401:dict},
    summary="Renovar o token de acesso",
    auth=None
)
def renovar_token(request,payload:TokenRefreshInputSchema):
    try:
        refresh_token = RefreshToken(payload.refresh)
        access_token = refresh_token.access_token
        return{
            "access":str(access_token),
            "refresh":str(refresh_token)
        }
    except TokenError:
        raise HttpError(401,"Token invalido ou expirado")

@router.post(
    "/logout",
    response={200:dict},
    summary="Logout do usuario",
    auth=None
)
def logout(request,payload:TokenRefreshInputSchema):
    try:
        token = RefreshToken(payload.refresh)
        token.blacklist()
        return {"message":"Logout realizado com sucesso"}
    except TokenError:
        raise HttpError(401,"Token invalido")

@router.get("/usuario/  {user_id}", response={200:UserSchema,404:ErrorSchema},summary="Buscar usuario pelo Id",auth=JWTAuth(),)
def buscar_usuario(request,user_id:int):
    try:
        user = get_object_or_404(Usuario,id=user_id)
        return user
    except Http404:
        return 404,{"message":f"Nenhum usuario com o ID: {user_id}, foi encontrado"}

@router.get(
    "/me",
    response=UserSchema,
    auth=JWTAuth(),
    summary="Obter informações do usuário autenticado"
)
def get_current_user(request):
    user = request.auth
    if user and user.is_authenticated:
        return user
    return 401, {"message": "Usuário não autenticado"}
    
@router.delete("/{user_id}", response={204:None} ,auth=None,summary="Deletar usuario pelo id")

def deletar_user(request,user_id:int):
    user = get_object_or_404(Usuario, id= user_id)
    user.delete()
    return 204,None

