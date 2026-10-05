from django.conf import settings
from django.db import migrations, models


def assign_existing_applications(apps, schema_editor):
    JobApplication = apps.get_model('applications', 'JobApplication')
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
    database = schema_editor.connection.alias
    applications = JobApplication.objects.using(database).filter(owner__isnull=True)
    if not applications.exists():
        return

    admin = User.objects.using(database).filter(username='admin', is_superuser=True).first()
    if admin is None:
        raise RuntimeError('The admin superuser must exist to assign existing applications.')
    applications.update(owner_id=admin.pk)


class Migration(migrations.Migration):
    dependencies = [
        ('applications', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='owner',
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
                related_name='job_applications',
                editable=False,
                null=True,
            ),
        ),
        migrations.RunPython(assign_existing_applications, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='jobapplication',
            name='owner',
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
                related_name='job_applications',
                editable=False,
            ),
        ),
    ]
