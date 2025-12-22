from django.shortcuts import redirect
from functools import wraps

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            if request.user.profile.role == role:
                return view_func(request, *args, **kwargs)

            return redirect('no_permission')
        return _wrapped_view
    return decorator
