from django import forms

from .models import JobApplication


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = (
            'company', 'position', 'location', 'job_url',
            'status', 'applied_date', 'salary', 'notes',
        )
        widgets = {
            'applied_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'notes': forms.Textarea(attrs={'rows': 5}),
        }
        error_messages = {
            'company': {'required': 'Company cannot be blank or only whitespace.'},
            'position': {'required': 'Position cannot be blank or only whitespace.'},
        }
        help_texts = {
            'salary': 'Leave blank if unknown. If provided, salary must be greater than 0.',
            'applied_date': 'Required for every status except Wishlist; leave blank for Wishlist.',
        }

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary is not None and salary <= 0:
            raise forms.ValidationError(
                'Salary must be greater than 0.', code='non_positive',
            )
        return salary

    def clean(self):
        cleaned_data = super().clean()
        # Preserve field errors when the status or date input is invalid.
        if 'status' not in cleaned_data or 'applied_date' not in cleaned_data:
            return cleaned_data

        status = cleaned_data.get('status')
        applied_date = cleaned_data['applied_date']
        if status != JobApplication.Status.WISHLIST and applied_date is None:
            self.add_error('applied_date', forms.ValidationError(
                'Applied date is required for every status except Wishlist.', code='required',
            ))
        elif status == JobApplication.Status.WISHLIST and applied_date is not None:
            self.add_error('applied_date', forms.ValidationError(
                'Applied date must be empty when status is Wishlist.', code='unexpected_date',
            ))
        return cleaned_data
