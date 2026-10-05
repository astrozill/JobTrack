from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import JobApplication


class ApplicationAccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.users = [
            User.objects.create_user(username=username)
            for username in ['alice', 'bob', 'charlie']
        ]
        cls.applications = [
            JobApplication.objects.create(
                owner=user,
                company=f'{user.username.title()} Company',
                position='Developer',
                status=JobApplication.Status.WISHLIST,
            )
            for user in cls.users
        ]
        cls.list_url = reverse('applications:application_list')

    def test_logged_out_user_is_redirected_from_application_list(self):
        response = self.client.get(self.list_url)

        self.assertRedirects(
            response, f'{reverse("login")}?next={self.list_url}',
        )

    def test_logged_in_users_can_open_application_list(self):
        for user in self.users:
            with self.subTest(user=user.username):
                self.client.force_login(user)
                response = self.client.get(self.list_url)

                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'applications/job_application_list.html')

    def test_users_only_see_their_own_applications(self):
        for user, owned_application in zip(self.users, self.applications):
            with self.subTest(user=user.username):
                self.client.force_login(user)
                response = self.client.get(self.list_url)

                # Check all results, including records on other pagination pages.
                self.assertQuerySetEqual(
                    response.context['paginator'].object_list, [owned_application],
                )
                self.assertContains(response, owned_application.company)
                for application in self.applications:
                    if application.owner_id != user.pk:
                        self.assertNotContains(response, application.company)

    def test_other_users_application_details_return_404(self):
        for user in self.users:
            self.client.force_login(user)
            for application in self.applications:
                with self.subTest(user=user.username, application=application.pk):
                    response = self.client.get(reverse(
                        'applications:application_detail', args=[application.pk],
                    ))

                    expected_status = 200 if application.owner_id == user.pk else 404
                    self.assertEqual(response.status_code, expected_status)

    def test_creating_application_sets_logged_in_user_as_owner(self):
        for user in self.users:
            with self.subTest(user=user.username):
                self.client.force_login(user)
                company = f'New company for {user.username}'
                response = self.client.post(reverse('applications:application_create'), {
                    'company': company,
                    'position': 'Engineer',
                    'status': JobApplication.Status.WISHLIST,
                })

                self.assertEqual(response.status_code, 302)
                application = JobApplication.objects.get(company=company)
                self.assertEqual(application.owner, user)
                self.assertRedirects(response, application.get_absolute_url())
