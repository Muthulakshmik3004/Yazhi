from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.mongodb import login_collection, otp_collection
from django.core.mail import send_mail
from django.conf import settings
import random
from backend.mongodb import attendance_collection
from datetime import datetime

# ---------------- LOGIN ----------------

@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = login_collection.find_one({
        "username": username,
        "password": password
    })

    if user:
        return Response({
            "success": True,
            "message": "Login Successful",
            "role": user.get("role")
        })

    return Response({
        "success": False,
        "message": "Invalid Username or Password"
    })


# ---------------- CHECK EMAIL ----------------
# ---------------- CHECK EMAIL ----------------

@api_view(["POST"])
def check_email(request):

    email = request.data.get("email")

    user = login_collection.find_one({"email": email})

    if not user:
        return Response({
            "success": False,
            "message": "Email not registered"
        })

    otp = str(random.randint(100000, 999999))

    otp_collection.delete_many({"email": email})

    otp_collection.insert_one({
        "email": email,
        "otp": otp
    })

    print("Saved OTP:", otp)

    try:

        message = f"""
Hello,

Your YAZHLI verification code is:

{otp}

This OTP is valid for 60 seconds.

Thank you,
YAZHLI Team
"""

        send_mail(
            "YAZHLI Password Reset OTP",
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )   

        print("Mail sent successfully")

        return Response({
            "success": True,
            "message": "OTP Sent Successfully"
        })

    except Exception as e:

        print("EMAIL ERROR:", e)

        return Response({
            "success": False,
            "message": str(e)
        })
        # ---------------- VERIFY OTP ----------------

@api_view(["POST"])
def verify_otp(request):

    email = request.data.get("email")
    otp = str(request.data.get("otp")).strip()

    print("Email:", email)
    print("OTP:", otp)

    otp_data = otp_collection.find_one({
        "email": email,
        "otp": otp
    })

    print("DB:", otp_data)

    if not otp_data:
        return Response({
            "success": False,
            "message": "Invalid OTP"
        })

    otp_collection.delete_many({"email": email})

    return Response({
        "success": True,
        "message": "OTP Verified Successfully"
    })
 # ---------------- RESET PASSWORD ----------------

@api_view(["POST"])
def reset_password(request):

    email = request.data.get("email")
    password = request.data.get("password")

    user = login_collection.find_one({
        "email": email
    })

    if not user:
        return Response({
            "success": False,
            "message": "User not found"
        })

    login_collection.update_one(
        {"email": email},
        {
            "$set": {
                "password": password
            }
        }
    )

    return Response({
        "success": True,
        "message": "Password Updated Successfully"
    })


@api_view(["POST"])
def punch_in(request):

    name = request.data.get("name")
    designation = request.data.get("designation")

    photo = request.FILES.get("photo")

    if not name or not designation or not photo:
        return Response({
            "success": False,
            "message": "All fields are required"
        })

    import os

    upload_folder = "media/punchin"

    os.makedirs(upload_folder, exist_ok=True)

    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{photo.name}"

    filepath = os.path.join(upload_folder, filename)

    with open(filepath, "wb+") as destination:
        for chunk in photo.chunks():
            destination.write(chunk)

    attendance_collection.insert_one({
        "name": name,
        "designation": designation,
        "photo": filepath,
        "punchIn": datetime.now(),
    })

    return Response({
        "success": True,
        "message": "Punch In Successful"
    })