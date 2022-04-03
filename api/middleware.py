from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.deprecation import MiddlewareMixin

from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import UserActivity


class UpdateLastActivityMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user'), 'The UpdateLastActivityMiddleware requires authentication middleware to be installed.'
        auth = JWTAuthentication()
        if auth.authenticate(request):
            header = auth.get_header(request)
            token = auth.get_raw_token(header)
            valid_token = auth.get_validated_token(token)
            user = auth.get_user(valid_token)
            user_obj = User.objects.get(username=user)
            try:
                obj = UserActivity.objects.get(user=user_obj.id)
                obj.last_activity = timezone.now()
                obj.save()
            except UserActivity.DoesNotExist:
                obj = UserActivity.objects.create(user=user_obj, last_activity=timezone.now())