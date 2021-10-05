
from app.calendario import Calendar
from django.shortcuts import redirect, render
from django.contrib import messages

from .models import FuncionarioModel,DepartamentoModel,HistoricoHorarioModel
from .forms import LoginForm, CadastrarDepartamentoForm, FuncionarioCadastroForm,FuncionarioEdicaoForm
from datetime import date, datetime

from django.utils.safestring import mark_safe


def index(request):

    
    if str(request.method) == 'POST':

        form = LoginForm(request.POST)

        
        if form.is_valid():

            usuario1 = form.cleaned_data['usuario']
            senha1 = form.cleaned_data['senha']
           
            usuario_logado = FuncionarioModel.objects.all().filter(senha=senha1).filter(usuario=usuario1)

            
            if(usuario_logado):

                usuario_logado = usuario_logado[0]
                request.session['dados_usuario'] = {
            
                    'nome':usuario_logado.nome,
                    'sobrenome':usuario_logado.sobrenome,
                    'usuario':usuario_logado.usuario,
                    'senha':usuario_logado.senha,
        
                }       
                usuario_logado = usuario_logado

                if usuario_logado.superusuario:

                    return redirect('administrativo_funcionarios/funcionario',permanent=True)
                
                else:

                    return redirect('area_usuario',permanent=False)
        
            messages.error(request,'Usuário não cadastrado')  
        
        else:

            messages.error(request,'Falha ao realizar login')
    
    else:
        
        # Caso não possua nenhum usuario administrador no sistema nas seguintes situações:
        # - caso onde o sistema não possui nenhum usuario
        # - caso onde todos os administradores foram excluidos.
        # Será criado um usuario administrador padrão e um departamento padrão, que poderão ser editados ou usados
        # para criar um novo usuario administrador e depois excluir o usuário padrão.
        funcionario_admin = FuncionarioModel.objects.all().filter(superusuario = True)
        if (not funcionario_admin):

            departamento_padrao = DepartamentoModel(sigla="...",nome="...")
            departamento_padrao.save()
            administrador_padrao = FuncionarioModel(departamento=departamento_padrao,nome="admin",sobrenome="admin",usuario="admin",senha="admin",superusuario=True,horario="dia todo")
            administrador_padrao.save()
    
        form = LoginForm()


    context = {

        'form': form
    }

    return render(request,'index.html',context)


##############################################################################

def area_usuario(request):

    if(not request.session.get('dados_usuario')):
        
        return redirect(index,permanent=False)

    funcionarios =FuncionarioModel.objects.all()[::] 
    funcionario = funcionarios.get(senha = request.session.get('dados_usuario')['senha'])  
    
    data_atual = date.today()
    
    # passa a data atual para a classe calendar
    cal = Calendar(data_atual.year,data_atual.month,funcionario)
    
    # Busca no historico uma data especifica
    horario_funcionario = HistoricoHorarioModel.objects.all().filter(funcionario = funcionario)
    horario = horario_funcionario.filter(data = datetime.now().strftime('%Y-%m-%d'))
    
   
   

    btn_saida_ativada = True

    # Verifica a existencia de um registro na data atual, Caso exista sinal de que jã foi realizado uma entrada
    if horario:
        
        # Variavel entrada é usada para alernar botão no tamplate entre entrada e saida
        entrada = False

        # a varivel btn_saida_ativada usado para desativar botao saida.
        if(horario[0].saida):

            btn_saida_ativada = False

    else:
        

        entrada = True

    html_cal = cal.formatmonth()
  
    context = {

        'data_atual': datetime.now().strftime('%d/%m/%Y'),
        'hora_atual': datetime.now().strftime('%H:%M:%S'),
        'calendario': mark_safe(html_cal), # o comando mark_safe permite que um html seja renderizado
        'entrada':entrada,
        'btn_saida_ativada':btn_saida_ativada,
       
    }
    return render(request,'area_usuario.html',context)

##############################################################################


def logout(request):

    
    try:
        del request.session['dados_usuario']
    except KeyError:
    
        pass

    return redirect(index)

##############################################################################

def administrativoFuncionarios(request,entidade='funcionario'):

    dados_adm = request.session.get('dados_usuario')
   
    if(not dados_adm):
        
        return redirect(index,permanent=False)

    if entidade == 'funcionario':

         
         dados_tabelas = FuncionarioModel.objects.all()[::]

    else:

        dados_tabelas = DepartamentoModel.objects.all()[::]
            

    context = {

        'dados_adm':dados_adm,
        'dados_tabelas':dados_tabelas,
        'informacao_atual':entidade

    }

   
    return render(request,'administrativoFuncionarios.html',context)


##############################################################################


def cadastroDepartamento(request):

    if(not request.session.get('dados_usuario')):
        
        return redirect(index,permanent=False)

    if str(request.method) == 'POST':

        form = CadastrarDepartamentoForm(request.POST)

        if form.is_valid():

            form.save()
            
            return redirect('/administrativo_funcionarios/departamento')

        else:

            messages.error(request,'Error')
    
    else:

        form = CadastrarDepartamentoForm()


    context = {

        'form': form
    }

    return render(request,'cadastroDepartamento.html',context)


##############################################################################


def cadastroFuncionario(request):

    # lembrar de cria uma verificação se existe algum departamento cadastrado, caso não exista transferir para
    # outra rota

    if(not request.session.get('dados_usuario')):
        
        return redirect(index,permanent=False)
    
    if str(request.method) == 'POST':

        form = FuncionarioCadastroForm(request.POST)

        if not FuncionarioModel.objects.all().filter(usuario = request.POST.get('usuario')):
            
            if form.is_valid():

                form.save()

                return redirect('/administrativo_funcionarios/funcionario',permanent=False)
            else:

                messages.error(request,'Erro nos dados fornecidos')
        else:

          
            form = FuncionarioCadastroForm()
            messages.error(request,'O nome de usuário fornecido já existe!')

    else:
        
        form = FuncionarioCadastroForm()
      

    context = {

        'form':form,
     
        
    }
    return render(request,'cadastroFuncionario.html',context)


##############################################################################


def editarFuncionario(request,login):

    if(not request.session.get('dados_usuario')):
        

        return redirect(index,permanent=False)
    
    if request.method == 'POST':

        form = FuncionarioEdicaoForm(request.POST)

        if form.is_valid():


            funcionario = FuncionarioModel.objects.get(senha=login)
            
            nome = form.cleaned_data['nome']
            sobrenome = form.cleaned_data['sobrenome']
            usuario = form.cleaned_data['usuario']
            funcionario.superusuario = form.cleaned_data['superusuario']
            funcionario.horario = form.cleaned_data['horario']
            funcionario.departamento = form.cleaned_data['departamento']
            funcionario.senha = form.cleaned_data['senha']

            
            funcionario.save()
            
            return redirect('/administrativo_funcionarios/funcionario',permanent=True)
        else:


            messages.error(request,'Dados com erro')
    else:
        
            try:
                dados_usuario = FuncionarioModel.objects.all().get(senha=login)

        
                departamento = dados_usuario.departamento
                nome = dados_usuario.nome
                sobrenome = dados_usuario.sobrenome
                usuario = dados_usuario.usuario       
                horario = dados_usuario.horario
                adm = dados_usuario.superusuario
                senha = dados_usuario.senha
                

                form = FuncionarioEdicaoForm({'departamento': departamento,'nome':nome,'sobrenome':sobrenome,'usuario':usuario,'senha': senha,'horario':horario,'superusuario':adm})
            
            except:

                return redirect('/administrativo_funcionarios/funcionario/',permanent=False)

    context = {

        'form':form,
        'senha':login
    }

    return render(request,'editarFuncionario.html',context)


##############################################################################



def removerFuncionario(request,login):

    
    if(not request.session.get('dados_usuario')):
        
        return redirect(index,permanent=False)
    
    funcionario = FuncionarioModel.objects.all().filter(senha = login)[::1]
    
    if funcionario:

        funcionario[0].delete()
        return redirect('/administrativo_funcionarios/funcionario',permanent=False)
    
    else:

        return redirect(index,permanent=False)



#################################################################################

def removerDepartamento(request,pk):

    if(not request.session.get('dados_usuario')):
        
        return redirect(index,permanent=False)
    
    departamento = DepartamentoModel.objects.all().filter(id= pk)[::1]
    if departamento:

        departamento[0].delete()
       
        
    return redirect('/administrativo_funcionarios/departamento',permanent=False)
 
 #################################################################################


def editarDepartamento(request,pk):
    
    if(not request.session.get('dados_usuario')):
        
        return redirect(index,permanent=False)

    if request.method == 'POST':

        form = CadastrarDepartamentoForm(request.POST)

        if form.is_valid():

            departamento = DepartamentoModel.objects.get(id=pk)
            
            departamento.sigla = form.cleaned_data['sigla']
            departamento.nome = form.cleaned_data['nome']
          
            departamento.save()
            return redirect('/administrativo_funcionarios/departamento',permanent=False)
        else:

            messages.error(request,'Dados com erro')
    else:
        
        try:

            dados_departamento = DepartamentoModel.objects.all().get(id=pk)

            sigla = dados_departamento.sigla
            nome = dados_departamento.nome
            form = CadastrarDepartamentoForm({'sigla': sigla,'nome':nome})

        except:

            return redirect('/administrativo_funcionarios/departamento/',permanent=False)

       

    context = {

        'form':form,
        'id':pk
    }

    return render(request,'editarDepartamento.html',context)


###################################################################################

def controle_entrada_saida(request,operacao):

    if(not request.session.get('dados_usuario')):
        
        return redirect(index,permanent=False)
   
    func = FuncionarioModel.objects.all().get(senha = request.session.get('dados_usuario')['senha'])    
    horario_funcionario = HistoricoHorarioModel.objects.all().filter(funcionario = func).filter(data = datetime.now().strftime('%Y-%m-%d'))


    if horario_funcionario:

        horario_funcionario[0].saida = datetime.now().strftime('%H:%M')
        horario_funcionario[0].status = 'presente'
        horario_funcionario[0].save()

    else:

        horario_funcionario = HistoricoHorarioModel( funcionario = func, data = datetime.now().strftime('%Y-%m-%d'),  entrada =  datetime.now().strftime('%H:%M'))
        horario_funcionario.save()

    
    return redirect('area_usuario',permanent=False)

    
    return redirect('area_usuario',permanent=False)


#############################################################################################################

def relatorios(request):

    if(not request.session.get('dados_usuario')):
        
        return redirect(index,permanent=False)
    
    if request.method == 'GET':
      
        historico = HistoricoHorarioModel.objects.all()[::]

    else :

        opcao = request.POST['opcao']
        campo_busca = request.POST['campo-busca']

        if opcao == 'full':

            historico = HistoricoHorarioModel.objects.all()[::]

        elif opcao == 'funcionario':

            funcionario = FuncionarioModel.objects.all().filter(nome=campo_busca)

            historico = []
            if(funcionario):

                for func in funcionario:

                    historico.extend(HistoricoHorarioModel.objects.all().filter(funcionario = func))
            
    

        elif opcao == 'entrada':

            if(campo_busca):

                historico = HistoricoHorarioModel.objects.all().filter(entrada=campo_busca)

            else:

                historico = []
        else:


            if campo_busca:

                historico = HistoricoHorarioModel.objects.all().filter(entrada=campo_busca)
            
            else:

                historico = []

            
    context = {

        'filtro': filter,
        'historico':historico
    }
    return render(request,"relatorio.html",context)