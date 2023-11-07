from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .forms import RegistrationForm, LoginForm, RequestForm, DesignCategoryForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from .models import Request, DesignCategory


# Create your views here.
def index(request):
    return render (request, 'index.html')

def home(request):
    return render(request, 'home.html')

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            fio = form.cleaned_data['fio']

            user = form.save()
            user.first_name = fio
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def login_v(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error_message('Неправильный логин или пароль.')
        else:
            form.add_error_message('Пожалуйста, исправьте ошибки в форме.')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

class ViewRequests(ListView):
   model = Request
   template_name = 'index.html'
   context_object_name = 'requests'

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)

       # Получите количество заявок в статусе "в процессе"
       in_process_count = Request.objects.filter(status='process').count()
       context['in_process_count'] = in_process_count

       # Получите последние 4 заявки в статусе "выполнено"
       done_requests = Request.objects.filter(status='made').order_by('-date')[:4]
       context['done_requests'] = done_requests

       return context

class RequestCreate(LoginRequiredMixin, CreateView):
    model = Request
    form_class = RequestForm
    template_name = 'auth_user/request_form.html'
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def user_requests(request):
        user = request.user
        status_filter = request.GET.get('status', 'all')

        if status_filter == 'new':
            requests = Request.objects.filter(user=user, status='new').order_by('-date')
        elif status_filter == 'in process':
            requests = Request.objects.filter(user=user, status='process').order_by('-date')
        elif status_filter == 'done':
            requests = Request.objects.filter(user=user, status='made').order_by('-date')
        else:
            requests = Request.objects.filter(user=user).order_by('-date')
        return render(request, 'auth_user/my_requests.html', {'requests': requests})



def delete_request(request, request_id):
    user = request.user
    request_to_delete = get_object_or_404(Request, id=request_id, user=user)
    if request.method == 'POST':
        if request_to_delete.status == 'new':
            request_to_delete.delete()
            return redirect('home')
        else:
            messages.error(request, "Невозможно удалить заявку с изменённым статусом.")
            return HttpResponseForbidden()

    return render(request, 'auth_user/delete_request.html', {'request_to_delete': request_to_delete})

def admin_requests(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        new_status = request.POST.get('new_status')
        comment = request.POST.get('comment')
        design_file = request.FILES.get('design_file')
        if request_id and new_status:
            request_obj = Request.objects.get(id=request_id)
            current_status = request_obj.status

            if current_status == 'made':
                if new_status in ('process', 'new'):
                        messages.error(request, 'Пепес дурак.')

            elif current_status == 'new':
                if new_status in ('process', 'made'):
                    if new_status == 'process':
                        if not comment:
                            messages.error(request, 'Для смены статуса на "В процессе" необходимо добавить комментарий.')
                        else:
                            request_obj.status = new_status
                            request_obj.comment = comment
                            request_obj.save()
                    elif new_status == 'made':
                        if not design_file:
                            messages.error(request,
                                           'Для смены статуса на "Выполнено" необходимо прикрепить файл дизайна.')
                        else:
                            request_obj.design_file = design_file
                            request_obj.status = new_status
                            request_obj.save()


            elif current_status == 'process':
                if new_status in ('made'):
                    if not design_file:
                        messages.error(request, 'Для смены статуса на "Выполнено" необходимо прикрепить файл дизайна.')
                    else:
                        request_obj.design_file = design_file
                        request_obj.status = new_status
                        request_obj.save()
                else:
                    messages.error(request, 'ффффффф Смена статуса с "в процессе" на другой статус невозможна.')

    requests = Request.objects.all().order_by('-date')
    return render(request, 'admin/admin_requests.html', {'requests': requests})

@login_required
def create_category(request):
    if request.method == 'POST':
        form = DesignCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return reverse_lazy('admin/category_list.html')
    else:
        form = DesignCategoryForm()
    return render(request, 'admin/create_category.html', {'form': form})

def category_list(request):
    categories = DesignCategory.objects.all()
    return render(request, 'admin/category_list.html', {'categories': categories})

def requests_by_category(request, category_id):
    category = DesignCategory.objects.get(id=category_id)
    requests = Request.objects.filter(category=category)
    return render(request, 'admin/requests_by_category.html', {'category': category, 'requests': requests})


def delete_category(request, category_id):
    category = get_object_or_404(DesignCategory, pk=category_id)

    if request.method == 'POST':
        requests = Request.objects.filter(category=category)
        for request in requests:
            request.delete()
        category.delete()
        return redirect('category_list')

    return render(request, 'home', {'category': category})

def request_detail(request, request_id):
    request_obj = get_object_or_404(Request, pk=request_id)
    return render(request, 'admin/request_detail.html', {'request': request_obj})
