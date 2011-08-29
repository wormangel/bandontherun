from django.contrib.auth.models import User

def create_user(first_name, last_name, username, password, email, phone):
    exists = get_user(username)
    if exists:
        raise Exception("Username already in use.")

    try:
        user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email)
        user.set_password(password)
        user.profile.phone = phone
        user.save()
        user.profile.save()
        return user
    except Exception as exc:
       raise Exception("Error creating user. Reason: " + exc.message)

def update_user(user, first_name, last_name, username, password, email, phone):
    user.first_name = first_name
    user.last_name = last_name
    user.username = username
    if len(password) > 5:
        user.set_password(password)
    user.profile.phone = phone
    user.save()
    return user

def get_user(username):
    return User.objects.filter(username=username)

def invite_user(email):
    if email is not None:
        pass
        # NewUserTask.delay(shortcut_name)
