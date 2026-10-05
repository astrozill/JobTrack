from django.conf import settings
from django.db import models
from django.urls import reverse


class JobApplication(models.Model):
    class Status(models.TextChoices):
        WISHLIST = 'wishlist', 'Wishlist'
        APPLIED = 'applied', 'Applied'
        INTERVIEW = 'interview', 'Interview'
        OFFER = 'offer', 'Offer'
        REJECTED = 'rejected', 'Rejected'
        WITHDRAWN = 'withdrawn', 'Withdrawn'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='job_applications',
        editable=False,
    )
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=150)
    location = models.CharField(max_length=100, blank=True)
    job_url = models.URLField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.WISHLIST,
    )
    applied_date = models.DateField(blank=True, null=True)
    salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    status__in=[
                        'wishlist', 'applied', 'interview',
                        'offer', 'rejected', 'withdrawn',
                    ]
                ),
                name='job_application_valid_status',
            ),
        ]

    def __str__(self):
        return f'{self.position} at {self.company}'

    def get_absolute_url(self):
        return reverse('applications:application_detail', kwargs={'pk': self.pk})
