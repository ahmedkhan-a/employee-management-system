from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Employee 
from .forms import EmployeeForm

# Create your views here.


@login_required
def dashboard(request):
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



@login_required
def employee_list(request):
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



@login_required
def employee_detail(request, id):
    employee = Employee.objects.get(id=id)
    return render(request, 'employee_details.html', {'employee': employee})


@login_required
def employee_update(request, id):
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


@login_required
def employee_delete(request, id):
    employee = Employee.objects.get(id=id)

    if request.method == 'POST':
        employee.delete()
        messages.success(request, "Employee deleted successfully.")
        return redirect('employee_list')

    return render(request, 'employee_details.html', {'employee': employee})


@login_required
def employee_form(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Employee added successfully.")
            return redirect("employee_list")

    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form})