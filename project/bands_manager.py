from models import Band

def create_band(band_name, shortcut_name, bio, url, user):
    exists = get_band(shortcut_name)
    if exists:
        raise Exception("Band shortcut name already in use.")

    try:
        band = Band.objects.create(name=band_name, shortcut_name=shortcut_name, bio=bio, url=url)
        band.members.add(user)
        band.save()
        return band
    except Exception as exc:
       raise Exception("Error creating band. Reason: " + exc.message)
    
def update_band(band, band_name, bio, url):
    band.name = band_name
    band.bio = bio
    band.url = url
    band.save()
    return band
    
def add_band_member(shortcut_name, user):
    band = get_band(shortcut_name)
    if band is None:
        raise Exception("There is no band with this shortcut name.")

    if band.member_list.contains(user):
        raise Exception(user.username + " is already rocking in this band!")

    band.members.add(user)
    band.save()
    return band
    
def remove_band_member(shortcut_name, user):
    band = get_band(shortcut_name)
    if band is None:
        raise Exception("There is no band with this shortcut name.")

    if not band.member_list.contains(user):
        raise Exception(user.username + " is not a member of this band.")

    band.members.remove(user)
    band.save()
    return band
    
def get_band(shortcut_name):
    band = Band.objects.filter(shortcut_name=shortcut_name)
    if len(band) == 0:
        return None
    elif len(band) != 1:
        raise Exception("Unexpected! Call security!")
    else:
        return band[0]
