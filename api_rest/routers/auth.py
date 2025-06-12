from ninja import Router
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from ninja.errors import HttpError
from ..schemas import LoginSchema,TokenSChema,TokenRefreshInputSchema,UserSchema,ErrorSchema
from ..models import Usuario
from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404
from django.http import Http404

router = Router(tags=["Autenticação"])

@router.post(
    "/login",
    response={200:TokenSChema,401:dict},
    summary="Login do Usuario",
    auth=None,
)
def login(request,data:LoginSchema):
    user = authenticate(email= data.email,password=data.password)
    if not user:
        return HttpError(401,"Usuario ou senha invalida")
    refresh = RefreshToken.for_user(user)
    return{
        "acess":str(refresh.access_token),
        "refresh":str(refresh),
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
            "acess":str(access_token),
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

@router.get(
    "/usuario/  {user_id}",
    response={200:UserSchema,404:ErrorSchema},
    summary="Buscar usuario pelo Id",
    auth=JWTAuth(),
)
   
def buscar_usuario(request,user_id:int):
    try:
        user = get_object_or_404(Usuario,id=user_id)
        return user
    except Http404:
        return 404,{"message":f"Nenhum usuario com o ID: {user_id}, foi encontrado"}