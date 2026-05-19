from django.shortcuts import render ,redirect
from .models import Attendance, Student
from .forms import StudentForm
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from .forms import GradeForm
from datetime import date as datetime_date

def student_list(request):
 query = request.GET.get('search')
 if query:
        all_students = Student.objects.filter(first_name__icontains=query) | Student.objects.filter(last_name__icontains=query)
 else:
        all_students = Student.objects.all()
 return render(request, 'students/student_list.html', {'students': all_students})

# NEW: The view to add a student
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save() # This saves the data to the database!
            return redirect('student_list') # Go back to the list page
    else:
        form = StudentForm()
    
    return render(request, 'students/add_student.html', {'form': form})

# EDIT STUDENT
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/add_student.html', {'form': form, 'edit': True})

# DELETE STUDENT
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        return redirect('student_list')
    return render(request, 'students/delete_confirm.html', {'student': student})

def student_profile(request, student_id):
   # Change .get() to get_object_or_404
    student = get_object_or_404(Student, id=student_id)
    
    # Analysis 1: Calculate Average Grade
    average_grade = student.grades.aggregate(Avg('score'))['score__avg'] or 0
    
    # Analysis 2: Calculate Attendance Rate
    total_days = student.attendance_records.count()
    days_present = student.attendance_records.filter(status='Present').count()
    
    attendance_rate = (days_present / total_days * 100) if total_days > 0 else 0
    
    context = {
        'student': student,
        'average_grade': round(average_grade, 2),
        'attendance_rate': round(attendance_rate, 1),
    }
    return render(request, 'students/student_profile.html', context)

def add_grade(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == "POST":
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.student = student  # Link the grade to the specific student
            grade.save()
            return redirect('student_profile', student_id=student.id)
    else:
        # Pre-fill the student field in the form
        form = GradeForm(initial={'student': student})
    
    return render(request, 'students/add_grade.html', {'form': form, 'student': student})
def daily_attendance(request):
    # Get the date from the URL parameter, or default to today's date
    selected_date = request.GET.get('date', str(datetime_date.today()))
    all_students = Student.objects.all()
    
    if request.method == "POST":
        # Loop through all students to save their attendance status
        for student in all_students:
            status = request.POST.get(f'status_{student.id}')
            if status:
                # Update the record if it exists, otherwise create a new one
                Attendance.objects.update_or_create(
                    student=student,
                    date=selected_date,
                    defaults={'status': status}
                )
        return redirect('daily_attendance')

    return render(request, 'students/daily_attendance.html', {
        'students': all_students,
        'selected_date': selected_date
    })