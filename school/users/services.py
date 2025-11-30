from django.shortcuts import get_object_or_404

from users.models import Student, Parent, Teacher


profile_models = {
	'student': Student,
	'parent': Parent,
	'teacher': Teacher,
}


def get_user_profile(user):
	model = profile_models.get(user.user_type)
	return get_object_or_404(model, user=user) if model else None


def get_parent_child(parent, child_id):
	return get_object_or_404(Student, id=child_id, parents=parent)
