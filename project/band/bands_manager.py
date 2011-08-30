from models import Band

def create_band(name, bio, url, user):
    try:
        band = Band.objects.create(name=name, bio=bio, url=url)
        band.members.add(user)
        band.save()
        return band
    except Exception as exc:
       raise Exception("Error creating band. Reason: " + exc.message)
    
def update_band(band_id, name, bio, url):
    band = get_band(band_id)
    band.name = name
    band.bio = bio
    band.url = url
    band.save()
    return band

def exists(band_id):
    return Band.objects.filter(id=band_id).exists()

def add_band_member(band_id, user):
    band = get_band(band_id)
    if band is None:
        raise Exception("There is no band with this shortcut name.")

    if band.members.filter(username=user.username).exists():
        raise Exception(user.username + " is already rocking in this band!")

    band.members.add(user)
    band.save()
    return band
    
def remove_band_member(band_id, username):
    band = get_band(band_id)
    if band is None:
        raise Exception("There is no band with this shortcut name.")

    if not band.members.filter(username=username).exists():
        raise Exception(username + " is not a member of this band.")

    # band.members.remove(user)
    band.members.remove(username)
    band.save()
    return band
    
def get_band(band_id):
    band = Band.objects.filter(id=band_id)
    if len(band) == 0:
        return None
    elif len(band) != 1:
        raise Exception("Unexpected! Call security!")
    else:
        return band[0]
