from django import forms
from .models import Employee,RegisteredUser 


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = [
            'employee_id',
            'employee_name',
            'email',
            'phone',
            'department',
            'designation',
            'salary',
            'joining_date',
        ]

        widgets = {
            'joining_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }


def clean_employee_id(self):
    employee_id = self.cleaned_data['employee_id']

    if not employee_id.strip():
        raise forms.ValidationError("Employee ID cannot be empty.")
    return employee_id

def clean_employee_name(self):
    employee_name = self.cleaned_data['employee_name']

    if not employee_name.strip():
        raise forms.ValidationError("Employee name cannot be empty.")

    return employee_name

def clean_salary(self):
    salary = self.cleaned_data['salary']

    if salary < 0:
        raise forms.ValidationError("Salary cannot be negative.")

    return salary

def clean_phone(self):
    phone = self.cleaned_data['phone']

    if not phone.isdigit():
        raise forms.ValidationError("Phone number must contain only numbers.")

    if len(phone) != 10:
        raise forms.ValidationError("Phone number must be 10 digits.")

    return phone

def clean_joining_date(self):
    joining_date = self.cleaned_data['joining_date']

    from datetime import date

    if joining_date > date.today():
        raise forms.ValidationError("Joining date cannot be in the future.")

    return joining_date





class RegistrationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password"}
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password"}
        )
    )

    class Meta:
        model = RegisteredUser
        fields = [
            'name',
            'email',
            'mobile',
            'password',
            'confirm_password',
        ]

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']

        if not mobile.isdigit():
            raise forms.ValidationError(
                "Mobile number must contain only numbers."
            )

        if len(mobile) != 10:
            raise forms.ValidationError(
                "Mobile number must be 10 digits."
            )

        return mobile

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(
                    "Passwords do not match."
                )

        return cleaned_data