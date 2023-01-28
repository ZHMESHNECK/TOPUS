from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from django.db.models import Q
from .models import *
from .utils import *
from .forms import *


class TankHome(DataMixin, ListView):
    model = Tank
    template_name = 'tanks/index.html'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return context | c_def

    #search / sort
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Tank.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query), is_published=True)
        return Tank.objects.filter(is_published=True).select_related('cat')


# def index(request):  # имя функ. - любое, request - обязательно
#     posts = Tank.objects.all().order_by('title')
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0
#     }
#     # путь к шаблону
#     return render(request, 'tanks/index.html', context=context)



def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1><h2>проверьте url ссылку</h2>')


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'tanks/addpage.html'
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return context | c_def

# def addpage(request):
#     if request.method == 'POST':
#         # с заполенными данными
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()  # пустая форма
#     return render(request, 'tanks/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'tanks/new_contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return context | c_def

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class ShowPost(DataMixin, DetailView):
    model = Tank
    template_name = 'tanks/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return context | c_def

    # def show_post(request, post_slug):
    #     post = get_object_or_404(Tank, slug=post_slug)
    #     comment = Comment.objects.filter(post=post)

    #     context = {
    #         'post': post,
    #         'menu': menu,
    #         'title': post.title,
    #         'cat_selected': post.cat_id
    #     }
    #     if request.method == 'POST':
    #         form = CommentForm(request.POST)
    #         if form.is_valid():
    #             comm = form.save(commit=False)
    #             comm.user = request.user.get_username()
    #             comm.post = post
    #             comm.save()
    #     else:
    #         form = CommentForm()
    #     return request | post | context | form | comment


class AddReview(View):
    """Отзывы""" 

    def post(self, request, pk):
        form = CommentForm(request.POST)
        post = Tank.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.tank = post
            form.profile = request.user.profile
            form.save()
        return redirect(post.get_absolute_url())


class TankCategory(DataMixin, ListView):
    model = Tank
    template_name = 'tanks/index.html'
    allow_empty = False

    def get_queryset(self):
        return Tank.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(
            title='Категория - ' + str(c.name), cat_selected=c.pk)
        return context | c_def

# def show_category(request, cat_slug):
#     posts = Tank.objects.filter(cat__slug=cat_slug)

#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Категории',
#         'cat_selected': cat_slug
#     }
#     print(context['cat_selected'])
#     return render(request, 'tanks/index.html', context=context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'tanks/new_register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return context | c_def

    def form_valid(self, form):
        user = form.save()
        profile = Profile()
        profile.user = user
        profile.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'tanks/new_login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return context | c_def

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


# @login_required
# def profile(request):
#     menu = [
#         {'title': "Добавить статью", 'url_name': 'add_page'},
#         {'title': "Обратная связь", 'url_name': 'contact'},
#         {'title': 'Админ', 'url_name': 'admin'},

#     ]
#     if request.method == 'POST':
#         user_form = UserUpdateForm(request.POST, instance=request.user)
#         profile_form = ProfileUpdateForm(
#             request.POST, request.FILES, instance=request.user.profile)

#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, 'Your profile is updated successfully')
#             return redirect('profile')
#     else:
#         user_form = UserUpdateForm(instance=request.user)
#         profile_form = ProfileUpdateForm(instance=request.user.profile)

#     return render(request, 'tanks/profile.html', {'user_form': user_form, 'profile_form': profile_form, 'menu': menu})


class ProfileUser(DataMixin, DetailView):
    model = Profile
    template_name = 'tanks/new_profile.html'
    login_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated == True:
            # Try to dispatch to the right method; if a method doesn't exist,
            # defer to the error handler. Also defer to the error handler if the
            # request method isn't on the approved list.
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            return handler(request, *args, **kwargs)
        else:
            return redirect('login')

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileUser, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context

    def post(self, request, *args, **kwargs):
        users = Profile.objects.get(id=request.user.profile.id)
        if request.method == 'POST':
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = ProfileUpdateForm(
                request.POST, request.FILES, instance=request.user.profile)
            sa = request.POST.get('status')
            if sa:
                users.satus = True
                users.save()
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
            return redirect(f'/profile/{request.user.profile.id}/')
        else:
            user_form = UserUpdateForm(instance=users)
            profile_form = ProfileUpdateForm(instance=users.profile)
