from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import JobApplicationForm
from .models import JobApplication


class RegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class OwnedApplicationMixin:
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'applications/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        applications = JobApplication.objects.filter(owner=self.request.user)
        counts = {
            row['status']: row['total']
            for row in applications.values('status').annotate(total=Count('pk'))
        }
        context['total_applications'] = sum(counts.values())
        context['status_totals'] = [
            {'status': value, 'label': label, 'count': counts.get(value, 0)}
            for value, label in JobApplication.Status.choices
        ]
        context['recent_applications'] = applications.order_by('-updated_at', '-pk')[:5]
        return context


class JobApplicationListView(LoginRequiredMixin, OwnedApplicationMixin, ListView):
    model = JobApplication
    template_name = 'applications/job_application_list.html'
    context_object_name = 'applications'
    ordering = ('-updated_at')
    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset()
        self.search_query = self.request.GET.get('search', '').strip()
        self.selected_status = self.request.GET.get('status', '').strip()
        if self.selected_status not in JobApplication.Status.values:
            self.selected_status = ''

        if self.search_query:
            queryset = queryset.filter(
                Q(company__icontains=self.search_query)
                | Q(position__icontains=self.search_query)
            )
        if self.selected_status:
            queryset = queryset.filter(status=self.selected_status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.search_query
        context['selected_status'] = self.selected_status
        context['status_choices'] = JobApplication.Status.choices
        return context


class JobApplicationDetailView(LoginRequiredMixin, OwnedApplicationMixin, DetailView):
    model = JobApplication
    template_name = 'applications/job_application_detail.html'
    context_object_name = 'application'


class JobApplicationCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'applications/job_application_form.html'
    success_message = 'Application created successfully.'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class JobApplicationUpdateView(LoginRequiredMixin, OwnedApplicationMixin, SuccessMessageMixin, UpdateView):
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'applications/job_application_form.html'
    success_message = 'Application updated successfully.'


class JobApplicationDeleteView(LoginRequiredMixin, OwnedApplicationMixin, SuccessMessageMixin, DeleteView):
    model = JobApplication
    template_name = 'applications/job_application_confirm_delete.html'
    context_object_name = 'application'
    success_url = reverse_lazy('applications:application_list')
    success_message = 'Application deleted successfully.'
    http_method_names = ['get', 'post', 'head', 'options']
