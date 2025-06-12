from ninja import Schema
from datetime import datetime
from typing import Literal

class UserRegisterSchema(Schema):
    username: str
    email: str
    password: str
    idade: int

class UserSchema(Schema):
    id: int
    username: str
    email:str

class LoginSchema(Schema):
    email: str
    password:str

class TokenSChema(Schema):
    acess:str
    refresh:str

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
    conluida: bool
    data_criacao: datetime
    prioridade: str | None
    data_vencimento: datetime

class TarefaCreateSchema(Schema):
    titulo: str
    descricao: str|None=None
    data_vencimento: datetime
    prioridade: Literal["A","M","B"]

class TarefaUpdateSchema(Schema):
    titulo:str| None= None
    descricao: str| None=None
    conluida: bool| None=None