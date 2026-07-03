from django.urls import path
from .views import login, check_email, verify_otp
from .views import login, check_email, verify_otp, reset_password
from .views import punch_in
urlpatterns = [
    path("login/", login, name="login"),
    path("check-email/", check_email, name="check_email"),
    path("verify-otp/", verify_otp, name="verify_otp"),
    path("reset-password/", reset_password, name="reset_password"),
    
    path("punchin/", punch_in),
]