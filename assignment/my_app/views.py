from django.shortcuts import render, get_object_or_404
# from .models import Registration
# from .models import User, Role, API

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .permissions import IsAdmin
# from .serializers import UserCreateSerializer

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CustomUser, profile, API
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status

    
def user_view(request):
    if request.method == 'POST':    
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(username=username)
            if user.password == password:
                refresh = RefreshToken.for_user(user)
                tokens = {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                token1,_ = profile.objects.get_or_create(user_id=user.pk)
                token1.token = tokens['access']
                token1.save()
                request.session['auth_token'] = tokens['access']
                if user.role == 'Admin':
                    return render(request, 'my_app/admin.html')
                elif user.role == 'User':
                    return render(request, 'my_app/user.html')
                elif user.role == 'Viewer':
                    return render(request, 'my_app/viewer.html')
                return HttpResponse("Success")
            else:
                return HttpResponse("Invalid Password")
        except CustomUser.DoesNotExist:
            return HttpResponse("Invalid Username")
    else:
        return render(request, 'my_app/login.html')     

# def login_view(request):
#     if request.method == 'POST':
#         # Handle login form submission here (authenticate the user, set session/cookie, etc.)
#         # Example:
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             return render(request, 'login.html', {'error': 'Invalid credentials'})

#     return render(request, 'login.html')   

def add_api(request):
    if 'auth_token' in request.session:
        token = AccessToken(request.session.get('auth_token'))
        obj = CustomUser.objects.get(id=token['user_id'])
        if obj.role == 'Admin' or obj.role == 'User':
            if request.method == 'POST':
                # Get the form data from the POST request
                url = request.POST['url']
                # Add more fields as required based on your API model

                # Create the API object and save it to the database
                if API.objects.filter(api_name=url).exists():
                    return HttpResponse("API already exists")
                else:
                    api = API.objects.create(api_name=url)

                # Optionally, you can add more fields to the API object before saving

                # Redirect to the API list page after API creation
                return redirect('adding_user')  # Replace 'api_list' with the URL name for the API list page

            return render(request, 'my_app/add_api.html')
        else:
            return HttpResponse("You are not authorized to add user")
    else:
        return HttpResponse("You are not logged in")


def update_api(request):
    if 'auth_token' in request.session:
        token = AccessToken(request.session.get('auth_token'))
        obj = CustomUser.objects.get(id=token['user_id'])
        if obj.role == 'Admin' or obj.role == 'User':
            if request.method == 'POST':
                
                    # api_id = form.cleaned_data['id']  # Get the API ID from the form data
                    

                    # Update the existing API object with the form data
                    name = request.POST['curr_url']
                    update_api = request.POST['up_api']

                    api = get_object_or_404(API, api_name=name)
                    api.api_name = update_api
                    # Update more fields as needed based on your API model

                    api.save()

                    return redirect('adding_user')  # Redirect to the view_api page after API update
            else:
                apis = API.objects.all()
                return render(request, 'my_app/update_api.html', {'apis': apis})
        else:
            return HttpResponse("You are not authorized to add user")
    else:
        return HttpResponse("You are not logged in")

def view_api(request):
    # apis = API.objects.all()
    # return render(request, 'my_app/view_api.html', {'apis': apis})

    user  = CustomUser.objects.prefetch_related('apis')
    return render(request, 'my_app/view_api.html', {'user': user})

    

def add_user(request):
    if 'auth_token' in request.session:
        token = AccessToken(request.session.get('auth_token'))
        obj = CustomUser.objects.get(id=token['user_id'])
        if obj.role == 'Admin':
            if request.method == 'POST':
                # Get the form data from the POST request
                username = request.POST['username']
                password = request.POST['password']
                role = request.POST['role']
                selected_apis = request.POST.getlist('API')


                # Check if the user already exists
                if CustomUser.objects.filter(username=username).exists():
                    return render(request, 'my_app/add_user.html', {'error': 'Username already exists'})

                # Create a new user with the provided data
                user = CustomUser.objects.create(username=username, password=password, role=role)
                user.apis.set(API.objects.filter(api_name__in=selected_apis))
                user.save()



                # Optionally set other user attributes here, e.g., first_name, last_name

                # Redirect to the user list page after user creation
                return redirect('adding_user')  # Replace 'user_list' with the URL name for the user list page
            else:
                apis = API.objects.all()
                return render(request, 'my_app/add_user.html', {'apis': apis})
        else:
            return HttpResponse("You are not authorized to add user")
    else:
        return HttpResponse("You are not logged in")

def update_user(request):
    if 'auth_token' in request.session:
        token = AccessToken(request.session.get('auth_token'))
        obj = CustomUser.objects.get(id=token['user_id'])
        if obj.role == 'Admin':
            if request.method == 'POST':  
                try:
                    # Retrieve the user object from the database using the provided user_id

                    
                    # Update user data based on the form fields
                    username = request.POST['username']
                    role = request.POST['role']
                    selected_apis = request.POST.getlist('API')
                    
                    # Add more fields as needed
                    user = get_object_or_404(CustomUser, username=username)
                    if role != '':
                        user.role = role
                    user.apis.set(API.objects.filter(api_name__in=selected_apis))

                    # Save the updated user data to the database
                    user.save()

                    # Redirect to the user detail view after successful update
                    return redirect('adding_user')  # Replace 'user_detail' with the URL name of the user detail view
                except CustomUser.DoesNotExist:
                    # Handle the case when the user is not found
                    return render(request, 'user_not_found.html')

            # Render the update user form
            else:
                apis = API.objects.all()
                return render(request, 'my_app/update_user.html', {'apis': apis})
        else:
            return HttpResponse("You are not authorized to add user")
    else:
        return HttpResponse("You are not logged in")

def remove_user(request):
    if 'auth_token' in request.session:
        token = AccessToken(request.session.get('auth_token'))
        obj = CustomUser.objects.get(id=token['user_id'])
        if obj.role == 'Admin':
            if request.method == 'POST':
                # Get the form data from the POST request
                username = request.POST['username']

                try:
                    # Try to get the user by the provided username
                    user = CustomUser.objects.get(username=username)

                    # Check if the user is a superuser or not
                    # if user.is_superuser:
                    #     return render(request, 'my_app/remove_user.html', {'error': 'Cannot remove a superuser'})
                    
                    # Delete the user
                    user.delete()

                    # Redirect to the user list page after user removal
                    return redirect('adding_user')  # Replace 'user_list' with the URL name for the user list page
                except CustomUser.DoesNotExist:
                    # If the user with the provided username doesn't exist
                    return render(request, 'my_app/remove_user.html', {'error': 'User not found'})

            return render(request, 'my_app/remove_user.html')
        else:
            return HttpResponse("You are not authorized to add user")
    else:
        return HttpResponse("You are not logged in")

def remove_api(request):
    if 'auth_token' in request.session:
        token = AccessToken(request.session.get('auth_token'))
        obj = CustomUser.objects.get(id=token['user_id'])
        if obj.role == 'Admin':
            if request.method == 'POST':
                # Get the form data from the POST request
                api_name = request.POST['api']

                try:
                    # Try to get the user by the provided username
                    user = API.objects.get(api_name=api_name)

                    # Check if the user is a superuser or not
                    # if user.is_superuser:
                    #     return render(request, 'my_app/remove_user.html', {'error': 'Cannot remove a superuser'})
                    
                    # Delete the user
                    user.delete()

                    # Redirect to the user list page after user removal
                    return redirect('adding_user')  # Replace 'user_list' with the URL name for the user list page
                except API.DoesNotExist:
                    # If the user with the provided username doesn't exist
                    return render(request, 'my_app/remove_api.html', {'error': 'API not found'})
            apis = API.objects.all()
            return render(request, 'my_app/remove_api.html', {'apis': apis})
        else:
            return HttpResponse("You are not authorized to add user")
    else:
        return HttpResponse("You are not logged in")


# Create your views here.
# def register_user(request):
#     if request.method == 'POST':
#         data = request.POST

#         name = data['name']
#         username = data['username']
#         password =data['password']

#         Registration.objects.create(name=name, username = username, password = password)
#     return render(request, 'my_app/registration.html')




