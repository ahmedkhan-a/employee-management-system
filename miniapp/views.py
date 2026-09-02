from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password

from .models import Employee, RegisteredUser, LoginHistory
from .forms import EmployeeForm, RegistrationForm

# Create your views here.



def dashboard(request):


    if "user_id" not in request.session:
        return redirect("login")


    total_employees = Employee.objects.count()

    departments = Employee.objects.values('department').distinct().count()

    department_data = {}

    for employee in Employee.objects.all():
        department = employee.department

        if department in department_data:
            department_data[department] += 1
        else:
            department_data[department] = 1

    return render(
        request,       
        'dashboard.html',
        {
            'total_employees': total_employees,
            'departments': departments,
            'department_data': department_data,
        }
    )   




def employee_list(request):
    if "user_id" not in request.session:
        return redirect("login")
    search = request.GET.get('search')

    if search:
        employees = Employee.objects.filter(
            employee_name__icontains=search
        ) | Employee.objects.filter(
            employee_id__icontains=search
        )
    else:
        employees = Employee.objects.all()

    return render(request, 'employee_list.html', {'employees': employees})



def employee_detail(request, id):

    if "user_id" not in request.session:
        return redirect("login")

    employee = Employee.objects.get(id=id)
    return render(request, 'employee_details.html', {'employee': employee})


def employee_update(request, id):
    if "user_id" not in request.session:
        return redirect("login")    
    employee = Employee.objects.get(id=id)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)

        if form.is_valid():
            form.save()
            messages.success(request, "Employee updated successfully.")
            return redirect('employee_list')

    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employee_form.html', {'form': form})



def employee_delete(request, id):


    if "user_id" not in request.session:
        return redirect("login")

    employee = Employee.objects.get(id=id)

    if request.method == 'POST':
        employee.delete()
        messages.success(request, "Employee deleted successfully.")
        return redirect('employee_list')

    return render(request, 'employee_details.html', {'employee': employee})



def employee_form(request):

    if "user_id" not in request.session:
        return redirect("login")
    if request.method == "POST":
        form = EmployeeForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Employee added successfully.")
            return redirect("employee_list")

    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form})






def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # Hash the password before saving
            user.password = make_password(
                form.cleaned_data["password"]
            )

            user.save()

            messages.success(
                request,
                "Registration successful. Please login."
            )

            return redirect("login")

    else:
        form = RegistrationForm()

    return render(
        request,
        "registration/register.html",
        {"form": form}
    )





def user_login(request):
    if request.method == "POST":

        name = request.POST.get("name")
        password = request.POST.get("password")

        try:
            user = RegisteredUser.objects.get(name=name)

            if check_password(password, user.password):

                request.session["user_id"] = user.id
                request.session["user_name"] = user.name


                LoginHistory.objects.create(
                    name=name,
                    status="Success"
                )

                messages.success(
                    request,
                    "Login successful."
                )

                return redirect("dashboard")

            else:

                LoginHistory.objects.create(
                    name=name,
                    status="Failed"
                )

                messages.error(
                    request,
                    "Incorrect password. Please enter correct details."
                )

        except RegisteredUser.DoesNotExist:

            LoginHistory.objects.create(
                name=name,
                status="Failed"
            )

            messages.error(
                request,
                "Incorrect password. Please enter correct details."
            )

    return render(
        request,
        "registration/login.html"
    )


def user_logout(request):
    request.session.flush()
    return redirect("login")