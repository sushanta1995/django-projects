from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Course, Enrollment
from .forms import CourseForm, EnrollmentForm, ProfilePhotoForm
from django.contrib.auth.views import LogoutView
from django.urls import reverse
from django.http import HttpResponseRedirect

def home_view(request):
    courses = Course.objects.all()
    return render(request, 'core/home.html', {'courses': courses})

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

@login_required
def available_courses(request):
    if request.user.user_type != 'student':
        return redirect('login')
    courses = Course.objects.all()
    paginator = Paginator(courses, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/course_list.html', {'page_obj': page_obj})

@login_required
def enroll_course(request):
    if request.user.user_type != 'student':
        return redirect('login')

    course_id = request.GET.get('course_id')
    course = Course.objects.get(id=course_id)

    # Prevent enrolling in full course
    if course.remaining_seats <= 0:
        return redirect('available_courses')

    if request.method == 'POST':
        form = EnrollmentForm(request.POST, student=request.user)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.student = request.user
            enrollment.save()
            return redirect('available_courses')
    else:
        form = EnrollmentForm(student=request.user, initial={'course': course_id})

    return render(request, 'core/enroll.html', {'form': form})

@login_required
def admin_enrollments_view(request):
    if request.user.user_type != 'admin':
        return redirect('login')
    enrollments = Enrollment.objects.select_related('student', 'course')
    q = request.GET.get('q')
    if q:
        enrollments = enrollments.filter(
            Q(student__username__icontains=q) |
            Q(course__name__icontains=q)
        )
    paginator = Paginator(enrollments, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/enrollments_admin.html', {'page_obj': page_obj})
