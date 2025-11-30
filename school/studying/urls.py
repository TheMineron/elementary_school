from django.urls import path
from . import views

urlpatterns = [
	path('', views.dashboard, name='dashboard'),

	path('student/grades/', views.student_grades, name='student_grades'),
	path('student/homework/', views.student_homework, name='student_homework'),
	path('student/schedule/', views.student_schedule, name='student_schedule'),

	path('parent/children/', views.parent_children, name='parent_children'),
	path('parent/child/<int:child_id>/grades/', views.parent_child_grades, name='parent_child_grades'),
	path('parent/child/<int:child_id>/homework/', views.parent_child_homework, name='parent_child_homework'),

	path('teacher/classes/', views.teacher_classes, name='teacher_classes'),
	path('teacher/class/<int:class_id>/grades/', views.teacher_class_grades, name='teacher_class_grades'),
	path('teacher/class/<int:class_id>/homework/add/', views.add_homework, name='add_homework'),
	path('teacher/add_grade/', views.add_grade, name='add_grade'),
	path('teacher/schedule/', views.teacher_schedule, name='teacher_schedule'),

	path('api/students/', views.get_students_by_class, name='get_students_by_class'),
]
