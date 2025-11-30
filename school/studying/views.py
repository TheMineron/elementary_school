from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.services import get_user_profile, get_parent_child
from .models import *
from .forms import GradeForm, HomeworkForm
from .services import user_type_required


@login_required
def dashboard(request):
    redirect_routes = {
        'student': 'student_grades',
        'parent': 'parent_children',
        'teacher': 'teacher_classes',
    }
    route = redirect_routes.get(request.user.user_type, 'dashboard')
    return redirect(route)


@login_required
@user_type_required('student')
def student_grades(request):
    student = get_user_profile(request.user)
    grades = Grade.objects.filter(student=student).order_by('-date')

    return render(request, 'school/student_grades.html', {
        'grades': grades,
        'student': student
    })


@login_required
@user_type_required('student')
def student_homework(request):
    student = get_user_profile(request.user)
    school_class = student.school_class.first()
    homework = Homework.objects.filter(school_class=school_class).order_by('-due_date')

    return render(request, 'school/student_homework.html', {
        'homework': homework,
        'student': student
    })


@login_required
@user_type_required('student')
def student_schedule(request):
    student = get_user_profile(request.user)
    school_class = student.school_class.first()
    schedule = Schedule.objects.filter(school_class=school_class).order_by('day_of_week', 'time')

    return render(request, 'school/student_schedule.html', {
        'schedule': schedule,
        'student': student
    })


@login_required
@user_type_required('parent')
def parent_children(request):
    parent = get_user_profile(request.user)
    children = parent.children.all()

    return render(request, 'school/parent_children.html', {
        'children': children,
        'parent': parent
    })


@login_required
@user_type_required('parent')
def parent_child_grades(request, child_id):
    parent = get_user_profile(request.user)
    child = get_parent_child(parent, child_id)
    grades = Grade.objects.filter(student=child).order_by('-date')

    return render(request, 'school/parent_child_grades.html', {
        'child': child,
        'grades': grades
    })


@login_required
@user_type_required('parent')
def parent_child_homework(request, child_id):
    parent = get_user_profile(request.user)
    child = get_parent_child(parent, child_id)
    school_class = child.school_class.first()
    homework = Homework.objects.filter(school_class=school_class).order_by('-due_date')

    return render(request, 'school/parent_child_homework.html', {
        'child': child,
        'homework': homework
    })


@login_required
@user_type_required('teacher')
def teacher_classes(request):
    teacher = get_user_profile(request.user)
    classes_taught = Class.objects.filter(class_teacher=teacher)

    return render(request, 'school/teacher_classes.html', {
        'classes_taught': classes_taught,
        'teacher': teacher
    })


@login_required
@user_type_required('teacher')
def teacher_class_grades(request, class_id):
    teacher = get_user_profile(request.user)
    school_class = get_object_or_404(Class, id=class_id, class_teacher=teacher)
    students = school_class.students.all()
    grades = Grade.objects.filter(student__in=students).order_by('-date')

    return render(request, 'school/teacher_class_grades.html', {
        'school_class': school_class,
        'students': students,
        'grades': grades
    })


@login_required
@user_type_required('teacher')
def add_grade(request):
    teacher = get_user_profile(request.user)

    if request.method == 'POST':
        form = GradeForm(teacher, request.POST)
        if form.is_valid():
            grade = form.save()
            messages.success(request, f'Оценка {grade.value} успешно выставлена для {grade.student}')
            return redirect('teacher_classes')
    else:
        form = GradeForm(teacher)

    return render(request, 'school/add_grade.html', {'form': form})


@login_required
@user_type_required('teacher')
def add_homework(request, class_id):
    teacher = get_user_profile(request.user)
    school_class = get_object_or_404(Class, id=class_id)

    if request.method == 'POST':
        form = HomeworkForm(teacher, request.POST)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.school_class = school_class
            homework.save()
            messages.success(request, f'Домашнее задание по {homework.subject} добавлено')
            return redirect('teacher_classes')
    else:
        form = HomeworkForm(teacher)

    return render(request, 'school/add_homework.html', {
        'form': form,
        'school_class': school_class
    })


@login_required
@user_type_required('teacher')
def teacher_schedule(request):
    teacher = get_user_profile(request.user)
    subjects = Subject.objects.filter(teachers=teacher)
    schedule = Schedule.objects.filter(subject__in=subjects).order_by('day_of_week', 'time')

    return render(request, 'school/teacher_schedule.html', {
        'schedule': schedule,
        'teacher': teacher
    })


def get_students_by_class(request):
    class_id = request.GET.get('class_id')
    if class_id:
        students = Student.objects.filter(school_class__id=class_id)
        students_data = [
            {
                'id': student.id,
                'name': f"{student.user.last_name} {student.user.first_name}"
            }
            for student in students
        ]
        return JsonResponse({'students': students_data})
    return JsonResponse({'students': []})
