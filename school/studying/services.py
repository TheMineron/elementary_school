from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def user_type_required(*user_types):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.user_type not in user_types:
                messages.error(request, "У вас нет доступа к этой странице")
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
