from django.contrib.auth.models import User

def create_user(first_name, last_name, username, password, email, phone):
    exists = get_user(username)
    if exists:
        raise Exception("Username already in use.")

    try:
        user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email)
        user.set_password(password)
        user.save()

        profile = user.profile
        profile.phone = phone
        profile.save()
        return user
    except Exception as exc:
       raise Exception("Error creating user. Reason: " + exc.message)

def update_user(user, first_name, last_name, new_password, email, phone):
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    if new_password is not None:
        user.set_password(new_password)
    user.save()

    profile = user.profile
    profile.phone = phone
    profile.save()
    return user
    
def exists(username):
    return User.objects.filter(username=username).exists()

def get_user(username):
    user = User.objects.filter(username=username)
    if len(user) == 0:
        return None
    elif len(user) != 1:
        raise Exception("Unexpected! Call security!")
    else:
        return user[0]

def invitation_exists(email, key):
    return UserInvitation.objects.filter(email=email, key=key).exists()
    
def get_invitation(email):
    return UserInvitation.objects.filter(email)

def create_invitation(email, key, band):
    invitation = UserInvitation.objects.create(email=email, key=key, band=band)
    return invitation

def invite_user(band, inviter, email):
    if email is not None:
        UserInvitationTask.delay(band, inviter, email)
