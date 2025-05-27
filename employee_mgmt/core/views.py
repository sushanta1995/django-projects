from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, CustomUser
from .forms import EmployeeForm, CustomUserForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import csv

@login_required
def dashboard(request):
    if request.user.user_type == 'admin':
        employees = Employee.objects.all()
        return render(request, 'admin_dashboard.html', {'employees': employees})
    else:
        emp = get_object_or_404(Employee, user=request.user)
        return render(request, 'employee_dashboard.html', {'employee': emp})

@login_required
def add_employee(request):
    if request.user.user_type != 'admin':
        return redirect('dashboard')

    if request.method == 'POST':
        user_form = CustomUserForm(request.POST)
        emp_form = EmployeeForm(request.POST)
        if user_form.is_valid() and emp_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 'employee'
            user.save()
            employee = emp_form.save(commit=False)
            employee.user = user
            employee.save()
            return redirect('dashboard')
    else:
        user_form = CustomUserForm()
        emp_form = EmployeeForm()
    return render(request, 'employee_form.html', {'user_form': user_form, 'emp_form': emp_form})

@login_required
def update_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.user.user_type != 'admin' and request.user != employee.user:
        return redirect('dashboard')

    emp_form = EmployeeForm(request.POST or None, instance=employee)
    if emp_form.is_valid():
        emp_form.save()
        return redirect('dashboard')
    return render(request, 'employee_form.html', {'emp_form': emp_form})

@login_required
def delete_employee(request, pk):
    if request.user.user_type != 'admin':
        return redirect('dashboard')
    emp = get_object_or_404(Employee, pk=pk)
    emp.user.delete()
    return redirect('dashboard')

@login_required
def export_csv(request):
    if request.user.user_type != 'admin':
        return redirect('dashboard')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=employees.csv'
    writer = csv.writer(response)
    writer.writerow(['username', 'education', 'salary', 'date_joined', 'age', 'gender', 'details'])
    for emp in Employee.objects.all():
        writer.writerow([
            emp.user.username,
            emp.education_details,
            emp.salary,
            emp.date_joined,
            emp.age,
            emp.gender,
            emp.employee_details
        ])
    return response

@login_required
def import_csv(request):
    if request.user.user_type != 'admin':
        return redirect('dashboard')
    invalid_rows = []
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        decoded = file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded)
        next(reader)
        for i, row in enumerate(reader, start=2):
            try:
                username, education, salary, joined, age, gender, details = row
                if CustomUser.objects.filter(username=username).exists():
                    raise ValueError("Username exists")
                user = CustomUser.objects.create_user(username=username, password='pass1234', user_type='employee')
                Employee.objects.create(
                    user=user,
                    education_details=education,
                    salary=float(salary),
                    date_joined=joined,
                    age=int(age),
                    gender=gender,
                    employee_details=details
                )
            except Exception as e:
                invalid_rows.append((i, row, str(e)))
    return render(request, 'import_result.html', {'invalid_rows': invalid_rows})
