# views.py

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# --- IMPORTS CORRIGIDOS ---
# Importa os modelos
from .models import Colaborador, Equipamento, Emprestimos
# Importa TODOS os formulários que vamos usar
from .forms import LoginForm, RegistrationForm, ColaboradorForm, EquipamentoForm, EmprestimoForm

# frameworks
# Django Messages Framework
from django.contrib import messages

# --- VIEW DE LOGIN (USANDO FORM) ---
def login_view(request):
    if request.user.is_authenticated:
        return redirect('app_dashboard')
    
    error_message = None

    if request.method == 'POST':
        # 1. Crie uma instância do formulário
        form = LoginForm(request.POST) # Usa o LoginForm
        
        # 2. Verifique se é válido
        if form.is_valid():
            cd = form.cleaned_data
            email = cd.get('email')
            password = cd.get('password')

            try:
                user_obj = User.objects.get(email=email)
                username = user_obj.username
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    auth_login(request, user)
                    return redirect('app_dashboard')
                else:
                    error_message = "Senha incorreta. Tente novamente."

            except User.DoesNotExist:
                error_message = "Nenhum usuário encontrado com este email."
            except Exception as e:
                error_message = f"Ocorreu um erro: {e}"
    else:
        # 3. Se for GET, crie um formulário vazio
        form = LoginForm()

    context = {'form': form, 'error': error_message}
    return render(request, "login.html", context)


# --- VIEW DE CRIAÇÃO DE CONTA (USANDO FORM) ---
def login_create(request):
    if request.user.is_authenticated:
        return redirect('app_dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST) # Usa o RegistrationForm
        
        if form.is_valid():
            cd = form.cleaned_data
            email = cd.get('email')
            password = cd.get('password')

            try:
                user = User.objects.create_user(username=email, email=email, password=password)
                
                user_auth = authenticate(request, username=email, password=password)
                if user_auth is not None:
                    auth_login(request, user_auth)
                    return redirect('app_dashboard')
                else:
                    form.add_error(None, "Erro ao autenticar após a criação.")

            except Exception as e:
                form.add_error(None, f"Ocorreu um erro inesperado: {e}")
    else:
        form = RegistrationForm()

    # O 'form' carrega todos os erros de validação
    context = {'form': form}
    return render(request, 'login_create.html', context)


@login_required
def app_dashboard(request):
    return render(request, 'app_ui_dashboard.html')

# --- CRUD DE COLABORADORES ---

@login_required
def app_users(request):
    """
    READ (List): Mostra todos os colaboradores.
    """
    colaboradores = Colaborador.objects.all().order_by('nome')
    
    object_data = []
    for col in colaboradores:
        object_data.append({
            'pk': col.pk,
            'fields': [col.nome, col.email, col.funcao]
        })

    context = {
        'page_title': 'Colaboradores',
        'headers': ['Nome', 'Email', 'Função'],
        'object_data': object_data,
        'add_url_name': 'app_users_create',
        'edit_url_name': 'app_users_edit',   
        'delete_url_name': 'app_users_delete',
    }
    return render(request, 'app_ui_users.html', context)

@login_required
def app_users_create(request):
    if request.method == 'POST':
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            colaborador_salvo = form.save()
            messages.success(request, f'Colaborador "{colaborador_salvo.nome}" cadastrado com sucesso!')
        else:
            messages.error(request, 'Falha no cadastro. Verifique os erros abaixo.')
    else:
        form = ColaboradorForm()
    
    context = {
        'form': form,
        'page_title': 'Cadastrar Novo Colaborador',
    }
    return render(request, 'app_ui_form_base.html', context)

@login_required
def app_users_edit(request, pk):
    """
    UPDATE: Edita um colaborador existente.
    """
    colaborador = get_object_or_404(Colaborador, pk=pk)

    if request.method == 'POST':
        form = ColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            form.save()
            return redirect('app_users')
    else:
        form = ColaboradorForm(instance=colaborador)

    context = {
        'form': form,
        'page_title': f'Editar Colaborador: {colaborador.nome}'
    }
    return render(request, 'app_ui_form_base.html', context)

@login_required
def app_users_delete(request, pk):
    """
    DELETE: Exclui um colaborador.
    """
    colaborador = get_object_or_404(Colaborador, pk=pk)

    if request.method == 'POST':
        colaborador.delete()
        return redirect('app_users')

    context = {
        'item': colaborador,
    }
    return render(request, 'app_ui_delete_confirm_base.html', context)


# --- CRUD DE EQUIPAMENTOS ---

@login_required
def app_items(request):
    """
    READ (List): Mostra todos os equipamentos.
    """
    equipamentos = Equipamento.objects.all().order_by('nome')
    
    object_data = []
    for item in equipamentos:
        object_data.append({
            'pk': item.pk,
            'fields': [item.nome, item.marca, item.quantidade]
        })

    context = {
        'page_title': 'Equipamentos',
        'headers': ['Nome', 'Marca', 'Quantidade'],
        'object_data': object_data,
        'add_url_name': 'app_items_create',
        'edit_url_name': 'app_items_edit',   
        'delete_url_name': 'app_items_delete',
    }
    return render(request, 'app_ui_items.html', context)

@login_required
def app_items_create(request):
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            item_salvo = form.save()
            messages.success(request, f'Equipamento "{item_salvo.nome}" cadastrado com sucesso!')
        else:
            messages.error(request, 'Falha no cadastro. Verifique os erros abaixo.')
    else:
        form = EquipamentoForm()

    context = {
        'form': form,
        'page_title': 'Cadastrar Novo Equipamento',
    }
    return render(request, 'app_ui_form_base.html', context)

@login_required
def app_items_edit(request, pk):
    """
    UPDATE: Edita um equipamento existente.
    """
    item = get_object_or_404(Equipamento, pk=pk)

    if request.method == 'POST':
        form = EquipamentoForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('app_items')
    else:
        form = EquipamentoForm(instance=item)

    context = {
        'form': form,
        'page_title': f'Editar Equipamento: {item.nome}',
    }
    return render(request, 'app_ui_form_base.html', context)

@login_required
def app_items_delete(request, pk):
    """
    DELETE: Exclui um equipamento.
    """
    item = get_object_or_404(Equipamento, pk=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('app_items')

    context = {
        'item': item,
    }
    return render(request, 'app_ui_delete_confirm_base.html', context)


# --- CRUD DE EMPRÉSTIMOS ---

@login_required
def app_requests(request):
    """
    READ (List): Mostra todos os empréstimos.
    """
    emprestimos = Emprestimos.objects.all().order_by('-data_emprestimo')
    
    object_data = []
    for emp in emprestimos:
        object_data.append({
            'pk': emp.pk,
            'fields': [
                emp.nome.nome, 
                emp.equipamento.nome, 
                emp.quantidade,
                emp.data_emprestimo.strftime('%d/%m/%Y %H:%M'),
                emp.data_prazo.strftime('%d/%m/%Y %H:%M'),
                emp.estoque_disponivel
            ]
        })

    context = {
        'page_title': 'Empréstimos',
        'headers': ['Colaborador', 'Equipamento', 'Quantidade', 'Data Empréstimo', 'Prazo Devolução', 'Estoque Disponível'],
        'object_data': object_data,
        'add_url_name': 'app_requests_create',
        'edit_url_name': 'app_requests_edit',   
        'delete_url_name': 'app_requests_delete',
    }
    return render(request, 'app_ui_requests.html', context)

@login_required
def app_requests_create(request):
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo_salvo = form.save()
            messages.success(request, f'Empréstimo para "{emprestimo_salvo.nome.nome}" cadastrado com sucesso!')
            return redirect('app_requests')
        else:
            messages.error(request, 'Falha no cadastro. Verifique os erros abaixo.')
    else:
        form = EmprestimoForm()
    
    context = {
        'form': form,
        'page_title': 'Cadastrar Novo Empréstimo',
    }
    return render(request, 'app_ui_form_base.html', context)

@login_required
def app_requests_edit(request, pk):
    """
    UPDATE: Edita um empréstimo existente.
    """
    emprestimo = get_object_or_404(Emprestimos, pk=pk)

    if request.method == 'POST':
        form = EmprestimoForm(request.POST, instance=emprestimo)
        if form.is_valid():
            form.save()
            messages.success(request, f'Empréstimo atualizado com sucesso!')
            return redirect('app_requests')
        else:
            messages.error(request, 'Falha ao atualizar. Verifique os erros abaixo.')
    else:
        form = EmprestimoForm(instance=emprestimo)

    context = {
        'form': form,
        'page_title': f'Editar Empréstimo',
    }
    return render(request, 'app_ui_form_base.html', context)

@login_required
def app_requests_delete(request, pk):
    """
    DELETE: Exclui um empréstimo.
    """
    emprestimo = get_object_or_404(Emprestimos, pk=pk)

    if request.method == 'POST':
        emprestimo.delete()
        messages.success(request, 'Empréstimo excluído com sucesso!')
        return redirect('app_requests')

    context = {
        'item': emprestimo,
    }
    return render(request, 'app_ui_delete_confirm_base.html', context)


# --- OUTRAS VIEWS DO APP ---

@login_required
def app_history(request):
    return render(request, 'app_ui_history.html')

@login_required
def app_reports(request):
    return render(request, 'app_ui_reports.html')

@login_required
def app_configs(request):
    return render(request, 'app_ui_configs.html')