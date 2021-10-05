from django import forms
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import NullBooleanField
from django.forms import widgets
from django.contrib.auth.models import User

class DepartamentoModel(models.Model):

    sigla = models.CharField('Sigla',max_length=5)
    nome = models.CharField('Nome', max_length=100)

    def __str__(self):

        return self.sigla


class FuncionarioModel(models.Model):


    departamento = models.ForeignKey(DepartamentoModel,on_delete= models.CASCADE)
    nome = models.CharField('Nome', max_length=100)
    sobrenome = models.CharField('Sobrenome',max_length=100)
    usuario = models.CharField('Usuário',max_length=100)
    senha = models.CharField('Senha', max_length=6, primary_key=True)
    superusuario = models.BooleanField('Super usuário',default=False)
    horario = models.CharField("Hora de trabalho",max_length=50)

    def __str__(self):

        return self.nome

class HistoricoHorarioModel(models.Model):

    funcionario = models.ForeignKey(FuncionarioModel, on_delete=models.CASCADE)
    data = models.DateField('Data')
    status = models.CharField('Status',default='limpo',max_length=30)
    entrada = models.TimeField('Entrada',null=True, blank=True)
    saida = models.TimeField('Saida',null=True,blank=True)

    def __str__(self):

        return "{} - {}".format(self.entrada,self.saida)
    





