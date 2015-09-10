from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, RedirectView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .forms import ClientForm, EntryForm, ProjectForm
from .models import Client, Entry, Project


class LoginRequiredMixin:
    """
    Mixin to apply login_required decorator to the dispatch method of multiple
    class based views.

    Mixin order matters and as all class based views implement a dispatch method
    this mixin must be given a higher precedence than the generic CBV class
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class ClientCreateView(LoginRequiredMixin, CreateView):
    """
    This view has a form for creating new clients. It also displays a list of
    clients. We could have used ListView for the latter part but then we
    wouldn't have the form handling of CreateView. It could be possible to mix
    in the functionality of CreateView and ListView classes with a combination
    of the mixin classes they comprise of but for the sake of simplicity we'll
    just pass the client queryset into the template context via
    get_context_data().
    """
    model = Client
    form_class = ClientForm
    template_name = 'clients.html'
    # Alternately to defining a get_success_url method returning
    # reverse('client-list'), reverse_lazy allows us to provide a url reversal
    # before the project's URLConf is loaded
    success_url = reverse_lazy('client-list')

    def get_context_data(self, **kwargs):
        context = super(ClientCreateView, self).get_context_data(**kwargs)
        context['client_list'] = Client.objects.all()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ClientCreateView, self).form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """
    CBV version of "client_detail" view function
    """
    model = Client
    form_class = ClientForm
    template_name = 'client_detail.html'
    success_url = reverse_lazy('client-list')

    def get_queryset(self):
        qs = super(ClientUpdateView, self).get_queryset()
        return qs.filter(author=self.request.user)


class EntryCreateView(LoginRequiredMixin, CreateView):
    """
    CBV version of "entries" view function
    """
    model = Entry
    form_class = EntryForm
    success_url = reverse_lazy('entry-list')
    template_name = 'entries.html'

    def get_context_data(self, **kwargs):
        context = super(EntryCreateView, self).get_context_data(**kwargs)
        # Limit the entries listed to just the ones the currently logged in user
        # has created
        context['entry_list'] = Entry.objects.filter(author=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(EntryCreateView, self).form_valid(form)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """
    CBV version of "projects" view function
    """
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('project-list')
    template_name = 'projects.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        context['project_list'] = Project.objects.all()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ProjectCreateView, self).form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    """
    CBV version of "project_detail" view function
    """
    model = Project
    form_class = ProjectForm
    template_name = 'project_detail.html'
    success_url = reverse_lazy('project-list')

    def get_queryset(self):
        qs = super(ProjectUpdateView, self).get_queryset()
        return qs.filter(author=self.request.user)


class ClientRedirectView(RedirectView):
    # Set redirect non-permanent. We may want to change it later
    permanent = False
    url = reverse_lazy('client-list')
