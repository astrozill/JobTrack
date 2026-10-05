from django.contrib import admin

from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'company', 'position', 'status',
        'applied_date', 'updated_at'
    )
    list_display_links = ('company', 'position')
    list_filter = ('status', 'applied_date')
    search_fields = ('company', 'position')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)
