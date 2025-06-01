from django.urls import path
from . import views
from .views import CustomLogoutView

urlpatterns = [
    path('', views.home_view, name='home'),  # 👈 Add this
    path('courses/', views.available_courses, name='available_courses'),
    path('enroll/', views.enroll_course, name='enroll_course'),
    path('admin/enrollments/', views.admin_enrollments_view, name='admin_enrollments_view'),
    path('logout/', CustomLogoutView.as_view(next_page='home'), name='logout'),
]
