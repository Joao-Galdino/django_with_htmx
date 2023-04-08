from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user_model
from django.views.generic.list import ListView

from films.forms import RegisterForm
from films.models import Film

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'
    
class Login(LoginView):
    template_name = 'registration/login.html'

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)


class FilmList(ListView):
    template_name = "films.html"
    model = Film
    context_object_name = "films"

    def get_queryset(self):
        return Film.objects.filter(user=self.request.user)


def check_username(request):
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse('<div id="username-error" class="error">Username already exists</div') 
    else:
        return HttpResponse('<div id="username-error" class="success">Username is available</div')
    
def add_film(request):
    name = request.POST.get('filmname') #Name of atrribute name in form

    film = Film.objects.create(name=name)

    # add film to user`s list
    request.user.films.add(film)

    #return tamplate with new film
    films = request.user.films.all()
    return render(request, 'partials/film-list.html', {'films': films})