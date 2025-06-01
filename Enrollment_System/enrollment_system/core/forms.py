from django import forms
from .models import Course, Enrollment, CustomUser

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['course']

    def clean(self):
        cleaned_data = super().clean()
        student = self.initial.get('student')
        course = cleaned_data.get('course')

        if Enrollment.objects.filter(student=student, course=course).exists():
            raise forms.ValidationError("Already enrolled in this course.")
        if course.enrollment_set.count() >= course.max_students:
            raise forms.ValidationError("Course has reached max capacity.")
        return cleaned_data

class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_photo']

    def clean_profile_photo(self):
        photo = self.cleaned_data.get('profile_photo')
        if photo:
            if not photo.name.endswith('.png'):
                raise forms.ValidationError("Only PNG files are allowed.")
            if photo.size > 2*1024*1024:
                raise forms.ValidationError("File size must be less than 2MB.")
        return photo
