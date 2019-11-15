from .forms import SignUpForm
from django.views import generic
from django.urls import reverse_lazy


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('dashboard')
    template_name = 'signup.html'
