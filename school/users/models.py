from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
	USER_TYPES = (
		('teacher', 'Учитель'),
		('parent', 'Родитель'),
		('student', 'Ученик'),
	)
	user_type = models.CharField(max_length=10, choices=USER_TYPES)
	phone = models.CharField(max_length=15, blank=True)

	def __str__(self):
		return f"{self.username} ({self.get_user_type_display()})"


class Student(models.Model):
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	birth_date = models.DateField(null=True, blank=True)
	address = models.TextField(blank=True)

	def __str__(self):
		return self.user.get_full_name()


class Parent(models.Model):
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	children = models.ManyToManyField('Student', related_name='parents')

	def __str__(self):
		return self.user.get_full_name()


class Teacher(models.Model):
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.get_full_name()
