from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    idade = models.IntegerField(null=True,blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name']
    def __str__(self):
        return self.email

class Tarefa(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='tarefas')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    concluida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_vencimento = models.DateField(null=True, blank=True)

    @property
    def prioridade_display(self):
        return self.get_prioridade_display()

    def __str__(self):
        return self.titulo
    
    class Prioridade(models.TextChoices):
        ALTA = 'A', 'Alta'
        MEDIA = 'M','Média'
        BAIXA = 'B', 'Baixa'
    prioridade = models.CharField(max_length=1,choices=Prioridade.choices, default=Prioridade.MEDIA)
