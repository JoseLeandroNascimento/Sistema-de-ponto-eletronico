from os import name
from django.urls import path
from .views import area_usuario, controle_entrada_saida, editarFuncionario, index,cadastroDepartamento,administrativoFuncionarios,cadastroFuncionario, logout, relatorios,removerFuncionario,removerDepartamento,editarDepartamento

urlpatterns = [ 

    path('',index, name='index'),
    path('cadastro_departamento',cadastroDepartamento,name='cadastro_departamento'),
    path('administrativo_funcionarios/<str:entidade>/',administrativoFuncionarios, name='administrativo_funcionarios'),
    path('logout',logout,name='logout'),
    path('cadastro_funcionario',cadastroFuncionario,name='cadastro_funcionarios'),
    path('editar_funcionario/<str:login>/',editarFuncionario,name='editar_funcionario'),
    path('remover_funcionario/<str:login>/',removerFuncionario,name='remover_funcionario'),
    path('editar_departamento/<str:pk>/',editarDepartamento,name='editar_departamento'),
    path('remover_departamento/<str:pk>/',removerDepartamento,name='remover_departamento'),
    path('area_usuario',area_usuario,name='area_usuario'),
    path('relatorio',relatorios,name='relatorio'),
    path('controle_entrada_saida/<str:operacao>/',controle_entrada_saida,name='controle_entrada_saida'),
    
]