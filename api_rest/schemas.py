from ninja import Schema
from datetime import datetime, date
from typing import Literal

class UserRegisterSchema(Schema):
    username: str
    email: str
    password: str
    idade: int
    first_name: str

class UserSchema(Schema):
    id: int
    username: str
    email:str
    first_name: str

class LoginSchema(Schema):
    email: str
    password:str

class TokenSChema(Schema):
    access:str
    refresh:str

class LoginResponseSchema(Schema):
    tokens: TokenSChema
    user:UserSchema

class TokenRefreshInputSchema(Schema):
    refresh: str

class TokenObtainPairOutputSchema(Schema):
    access: str
    refresh: str

class ErrorSchema(Schema):
    message: str

class TarefaSchema(Schema):
    id: int
    titulo: str
    descricao: str |None
    concluida: bool
    data_criacao: datetime
    prioridade: str | None
    data_vencimento: date | None

class TarefaCreateSchema(Schema):
    titulo: str
    descricao: str|None=None
    data_vencimento: date
    prioridade: Literal["A","M","B"]

class TarefaUpdateSchema(Schema):
    titulo:str| None= None
    descricao: str| None=None
    concluida: bool| None=None
    data_vencimento: date | None = None