from django.contrib import admin
from .models import Student, Grade, Attendance

admin.site.register(Student)
admin.site.register(Grade)
admin.site.register(Attendance)
