from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import Teacher, Student


class Class(models.Model):
	GRADE_CHOICES = (
		(1, '1 класс'),
		(2, '2 класс'),
		(3, '3 класс')
	)

	number = models.IntegerField(choices=GRADE_CHOICES)
	letter = models.CharField(max_length=1)
	class_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='classes')
	students = models.ManyToManyField(Student, related_name='school_class')

	class Meta:
		verbose_name_plural = "Classes"

	def __str__(self):
		return f"{self.number}{self.letter}"


class Subject(models.Model):
	name = models.CharField(max_length=150)
	teachers = models.ManyToManyField(Teacher, related_name='subjects')

	def __str__(self):
		return self.name


class Schedule(models.Model):
	DAYS_OF_WEEK = (
		(1, 'Понедельник'),
		(2, 'Вторник'),
		(3, 'Среда'),
		(4, 'Четверг'),
		(5, 'Пятница'),
		(6, 'Суббота'),
	)

	school_class = models.ForeignKey(Class, on_delete=models.CASCADE)
	day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
	time = models.TimeField()

	def __str__(self):
		return f"{self.school_class} - {self.get_day_of_week_display()}"


class Grade(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
	value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
	date = models.DateField()
	comment = models.TextField(blank=True)

	def __str__(self):
		return f"{self.student} - {self.value}"


class Homework(models.Model):
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
	school_class = models.ForeignKey(Class, on_delete=models.CASCADE)
	due_date = models.DateField()
	assignment = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.subject} - {self.school_class}"
