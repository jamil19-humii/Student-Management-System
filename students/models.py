from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
# --- New Fields Below ---
    age = models.IntegerField(default=18) 
    major = models.CharField(max_length=100, default="General Studies")
    enrollment_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Grade(models.Model):
     student=models.ForeignKey(Student, on_delete=models.CASCADE , related_name='grades')
     subject=models.CharField(max_length=100)
     score=models.FloatField()
     def __str__(self):
        return f"{self.student.first_name} - {self.subject}"
     

class Attendance(models.Model):  
    # This defines a Django model called "Attendance".
    # Each instance will represent one student's attendance record for a specific date.

    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]
    # STATUS_CHOICES is a list of tuples used to restrict the "status" field.
    # The first value in each tuple is stored in the database,
    # the second value is the human-readable label shown in forms/admin.

    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='attendance_records')
    # ForeignKey creates a relationship to another model (Student).
    # Each attendance record belongs to one student.
    # on_delete=models.CASCADE means if a student is deleted, all their attendance records are deleted too.
    # related_name='attendance_records' lets you access attendance from a student object like: student.attendance_records.all()

    date = models.DateField()
    # A DateField stores the date of the attendance record (year-month-day).
    # Example: 2026-05-05

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    # A CharField stores text. Here it’s limited to 10 characters.
    # The "choices" argument restricts values to either "Present" or "Absent".

    def __str__(self):
        return f"{self.student.first_name} - {self.date} ({self.status})"
    # __str__ defines how this object is displayed as a string (e.g., in the admin panel).
    # It shows: Student’s first name, the date, and their status.
    # Example output: "Jamila - 2026-05-05 (Present)"
