from django.contrib.auth.models import User

def create_user(first_name, last_name, username, password, email, phone):

    if exists(username):
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
    try:
        user = User.objects.get(username=username)
        return user
    except User.DoesNotExist:
        raise Exception("There is no user called '%s'." % username)

def invitation_exists(key):
    return UserInvitation.objects.filter(key=key).exists()
    
def get_invitation(key):
    return UserInvitation.objects.filter(key)

def create_invitation(email, key, band):
    invitation = UserInvitation.objects.create(key=key, email=email, band=band)
    return invitation

def invite_user(email, inviter, band):
    if email is not None:
        UserInvitationTask.delay(band, inviter, email)
