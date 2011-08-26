from django.contrib.auth.models import User

def create_user(first_name, last_name, username, password, email, phone):
    user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email)
    user.set_password(password)
    user.profile.phone = phone
    user.save()
    return user
    
def get_user(username):
    return User.objects.filter(username=username)
