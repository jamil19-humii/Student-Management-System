from django.shortcuts import render ,redirect
from .models import Student
from .forms import StudentForm
from django.shortcuts import get_object_or_404

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