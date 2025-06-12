from typing import List,Optional
from ninja import Router
from django.shortcuts import get_object_or_404
from ninja_jwt.authentication import JWTAuth
from ..models import Tarefa
from ..schemas import TarefaSchema,TarefaUpdateSchema,TarefaCreateSchema

router = Router()
@router.get(
    "",
    response=List[TarefaSchema],
    auth=JWTAuth(),
    summary="Listar as tarefas do usuario autenticado",
)
def listar_tarefas(request):
    tarefas = Tarefa.objects.filter(user = request.auth)
    return tarefas

@router.post(
    "",
    response={201:TarefaSchema},
    auth=JWTAuth(),
    summary="Criar uma nova Tarefa"
)
def criar_tarefa(request,payload:TarefaCreateSchema):
    tarefa = Tarefa.objects.create(user=request.auth,**payload.dict())
    return 201, tarefa

@router.get(
    "/id/{tarefa_id}",
    response=TarefaSchema,
    auth=JWTAuth(),
    summary="Buscar uma Tarefa"
)

def buscar_tarefa_pelo_id(request, tarefa_id:int):
    tarefa = get_object_or_404(Tarefa,id = tarefa_id,user=request.auth)
    return tarefa

@router.get(
    "/titulo/{tarefa_titulo}",
    auth=JWTAuth(),
    summary="Buscar tarefa pelo titulo",
    response=List[TarefaSchema],
)

def buscar_tarefa_pelo_titulo(request,tarefa_titulo:str):
    tarefa = Tarefa.objects.filter(titulo__icontains=tarefa_titulo, user=request.auth)
    return tarefa

@router.put(
    "{tarefa_id}",
    response=TarefaSchema,
    auth=JWTAuth(),
    summary="Atualizar uma Tarefa"
)
def atualizar_tarefa(request,tarefa_id:int,payload:TarefaUpdateSchema):
    tarefa = get_object_or_404(Tarefa,id=tarefa_id, user=request.auth)
    for attr,value in payload.dict(exclude_unset=True).items():
        setattr(tarefa,attr,value)
    tarefa.save()
    return tarefa

@router.delete(
    "{tarefa_id}",
    response={204:None},
    auth= JWTAuth(),
    summary="Deletar Tarefa"
)
def deletar_tarefa(request,tarefa_id:int):
    tarefa = get_object_or_404(Tarefa,id=tarefa_id,user=request.auth)
    tarefa.delete()
    return 204,None

@router.post(
    "{tarefa_id}",
    response=TarefaSchema,
    auth=JWTAuth(),
    summary="Marca uma tarefa como concluída",
)
def concluir_tarefa(request,tarefa_id:int):
    tarefa = get_object_or_404(Tarefa,id = tarefa_id,user = request.auth)
    tarefa.conluida = True
    tarefa.save()
    return tarefa

