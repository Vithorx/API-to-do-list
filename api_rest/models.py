from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    idade = models.IntegerField(null=True,blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name']
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_gruops', blank= True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permission', blank=True)

    def __str__(self):
        return self.email

class Prioridade(models.TextChoices):
        ALTA = 'A', 'Alta'
        MEDIA = 'M','Média'
        BAIXA = 'B', 'Baixa'

class Tarefa(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='tarefas')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True,null=True)
    concluida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_vencimento = models.DateField(null=True, blank=True)

    prioridade = models.CharField(max_length=1,choices=Prioridade.choices, default=Prioridade.MEDIA)

    @property
    def prioridade_display(self):
        return self.get_prioridade_display()

    def __str__(self):
        return self.titulo
    
    
