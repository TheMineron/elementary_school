from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class StudentInline(admin.StackedInline):
	model = Student
	can_delete = False
	verbose_name_plural = 'Данные ученика'


class TeacherInline(admin.StackedInline):
	model = Teacher
	can_delete = False
	verbose_name_plural = 'Данные учителя'


class ParentInline(admin.StackedInline):
	model = Parent
	can_delete = False
	verbose_name_plural = 'Данные родителя'
	filter_horizontal = ('children',)


@admin.register(CustomUser)
class CustomUserAdminWithProfile(UserAdmin):
	list_display = ['username', 'email', 'user_type', 'phone', 'is_staff']
	list_filter = ['user_type', 'is_staff', 'is_superuser']

	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)

		if obj.user_type == 'student' and not hasattr(obj, 'student'):
			Student.objects.create(user=obj)
		elif obj.user_type == 'teacher' and not hasattr(obj, 'teacher'):
			Teacher.objects.create(user=obj)
		elif obj.user_type == 'parent' and not hasattr(obj, 'parent'):
			Parent.objects.create(user=obj)

	def get_inlines(self, request, obj=None):
		if obj and obj.user_type == 'student':
			return [StudentInline]
		elif obj and obj.user_type == 'teacher':
			return [TeacherInline]
		elif obj and obj.user_type == 'parent':
			return [ParentInline]
		return []

	def get_fieldsets(self, request, obj=None):
		fieldsets = super().get_fieldsets(request, obj)
		if obj:
			fieldsets = fieldsets + (
				('Дополнительная информация', {'fields': ('user_type', 'phone')}),
			)
		return fieldsets

	def get_add_fieldsets(self, request, obj=None):
		fieldsets = super().get_add_fieldsets(request, obj)
		fieldsets = list(fieldsets)
		fieldsets[1][1]['fields'] = fieldsets[1][1]['fields'] + ('user_type', 'phone')
		return fieldsets
