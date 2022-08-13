from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.http.response import HttpResponseRedirect

from core.models.keys import Key

from ..mixins.views import TitleMixin


class KeyView(LoginRequiredMixin, TitleMixin, TemplateView):
    title = "All Keys"
    template_name = "frontend/key_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data_url"] = reverse_lazy("frontend:key_list_data")
        return context


class KeyEditView(LoginRequiredMixin, TitleMixin, UpdateView):
    model = Key
    template_name = "frontend/key_edit.html"
    title = "Edit Key"
    fields = ["application", "key", "comment"] 
    success_url = reverse_lazy("frontend:keys")


class KeyCreateView(LoginRequiredMixin, TitleMixin, CreateView):
    model = Key
    template_name = "frontend/key_edit.html"
    title = "Create Key"
    fields = ["application", "key", "comment"]
    success_url = reverse_lazy("frontend:keys")

    def form_valid(self, form):
        key = form.save(commit=False)
        key.created_at = timezone.now()
        key.created_by = self.request.user
        key.save()
        return super().form_valid(form)


class KeyUseView(LoginRequiredMixin, TitleMixin, DeleteView):
    model = Key
    template_name = "frontend/key_use.html"
    title = "Use Key"

    def form_valid(self, form):
        success_url = reverse_lazy("frontend:keys", self.object.id)
        self.object.used_at = timezone.now()
        self.object.used_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(success_url)