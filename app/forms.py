

from django import forms
from django.db import models
from django.forms import fields, widgets
from django.forms.models import ModelForm
from django.utils.regex_helper import Choice

from .models import DepartamentoModel,FuncionarioModel

class FuncionarioCadastroForm(forms.ModelForm):

    class Meta:

        fields = ['departamento','nome','sobrenome','usuario','senha','horario','superusuario']
        model = FuncionarioModel

    
    options_horarios = (
        ('manha','Manha'),
        ('tarde','Tarde'),
        ('dia todo','Dia todo')
    )

    horario = forms.CharField(label="Horario",widget=forms.Select(choices=options_horarios))

class FuncionarioEdicaoForm(forms.ModelForm):

    
    """
        Verificamos que ao editar uma chave primaria, no caso é a senha do usuario, não é editado a senha
        mas é criado um novo usuario, por isso não colocamos a opcao de edição senha no formulario          
    """
    class Meta:

        fields = ['departamento','nome','sobrenome','usuario','superusuario','horario']
        model = FuncionarioModel  

     
    options_horarios = (
        ('manha','Manha'),
        ('tarde','Tarde'),
        ('dia todo','Dia todo')
    )

    horario = forms.CharField(label="Horario",widget=forms.Select(choices=options_horarios))

class LoginForm(forms.Form):

    usuario = forms.CharField(label='Usuário', max_length=100)
    senha = forms.CharField(label='Senha', max_length=12, widget=forms.PasswordInput())
  


class CadastrarDepartamentoForm(forms.ModelForm):

    class Meta:

        fields = ['sigla','nome']
        model = DepartamentoModel


