from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.profile_photo and self.profile_photo.size > 2*1024*1024:
            raise ValueError("Image size should not exceed 2MB")
        if self.profile_photo and not self.profile_photo.name.endswith('.png'):
            raise ValueError("Only PNG images are allowed")
        super().save(*args, **kwargs)


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    max_students = models.IntegerField()
    credits = models.IntegerField()

    def __str__(self):
        return self.name

    def current_enrollment(self):
        return self.enrollment_set.count()

class Enrollment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')  # Prevent duplicate enrollment

    def __str__(self):
        return f"{self.student.username} - {self.course.code}"
