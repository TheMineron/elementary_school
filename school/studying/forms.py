from django import forms
from .models import Grade, Homework, Subject, Class


class GradeForm(forms.ModelForm):
	school_class = forms.ModelChoiceField(
		queryset=Class.objects.none(),
		label="Класс",
		empty_label="Выберите класс"
	)

	class Meta:
		model = Grade
		fields = ['school_class', 'student', 'subject', 'value', 'date', 'comment']
		widgets = {
			'date': forms.DateInput(attrs={'type': 'date'}),
			'comment': forms.Textarea(attrs={'rows': 3}),
			'value': forms.NumberInput(attrs={'type': 'number', 'min': 1, 'max': 5}),
		}

	def __init__(self, teacher, *args, **kwargs):
		super().__init__(*args, **kwargs)

		from users.models import Student
		self.fields['school_class'].queryset = teacher.classes.all()
		self.fields['subject'].queryset = Subject.objects.filter(teachers=teacher)
		self.fields['student'].queryset = Student.objects.none()

		if 'school_class' in self.data:
			try:
				class_id = int(self.data.get('school_class'))
				self.fields['student'].queryset = Student.objects.filter(
					school_class__id=class_id
				).order_by('user__last_name', 'user__first_name')
			except (ValueError, TypeError):
				pass


class HomeworkForm(forms.ModelForm):
	class Meta:
		model = Homework
		fields = ['subject', 'due_date', 'assignment']
		widgets = {
			'due_date': forms.DateInput(attrs={'type': 'date'}),
			'assignment': forms.Textarea(attrs={'rows': 4}),
		}

	def __init__(self, teacher, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['subject'].queryset = Subject.objects.filter(teachers=teacher)
