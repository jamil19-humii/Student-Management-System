from django.db import models

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