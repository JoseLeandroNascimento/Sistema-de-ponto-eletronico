from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import DepartamentoModel, FuncionarioModel,HistoricoHorarioModel
# Register your models here.

class DepartamentoAdmin(admin.ModelAdmin):

    list_display = ('sigla', 'nome')

class FuncionarioAdmin(admin.ModelAdmin):

    list_display = ('departamento','nome','sobrenome','horario','usuario','senha','superusuario')

class HistoricoFuncionarioAdmin(admin.ModelAdmin):

    list_display = ('funcionario','data','entrada','saida','status')




admin.site.register(DepartamentoModel,DepartamentoAdmin)
admin.site.register(FuncionarioModel,FuncionarioAdmin)
admin.site.register(HistoricoHorarioModel,HistoricoFuncionarioAdmin)
# admin.site.register(HistoricoHorarioModel,HistoricoFuncionarioAdmin)






