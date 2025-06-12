from ninja import NinjaAPI
from api_rest.routers.tarefas import router as api_rest_router
from ninja_jwt.authentication import JWTAuth
from api_rest.routers import users,auth,tarefas

api = NinjaAPI(
    title= "To-do List API",
    version= "1.0.0",
    description="Uma API para gerenciar tarefas e usuarios",
    auth=JWTAuth(),
)
api.add_router("/auth", auth.router,tags=["Login e Logout"])
api.add_router("/users", users.router,tags=["Cadastro"])
api.add_router("/tarefas", tarefas.router,tags=["Tarefas do Usuario"])