from django.contrib.auth import logout
from django.shortcuts import render, redirect


def home_page(request):
    context = {
        "title": "Hello Gamer!",
        "content": "Welcome to home page"
    }
    return render(request, "homepage.html", context)






'''

# this one works with the upload pic being called as a function from student.view
# does not throw any validation error for non-image type

def register_page(request):
    # if request.method == 'POST':
        register_form = RegisterForm(request.POST or None)
        photo_upload_form = ImageUploadForm(request.POST, request.FILES)

        context = {
            "register_form": register_form,
            "photo_upload_form": photo_upload_form
        }
        if register_form.is_valid():
            # print(register_form.cleaned_data)
            username = register_form.cleaned_data.get("username")
            first_name = register_form.cleaned_data.get("first_name")
            last_name = register_form.cleaned_data.get("last_name")
            email = register_form.cleaned_data.get("email")
            password = register_form.cleaned_data.get("password")

            new_user = User.objects.create_user(
                username, email, password,
                first_name=first_name,
                last_name=last_name,
            )

            upload_pic(request, photo_upload_form, username=username)

        return render(request, "auth/register.html", context)


'''