from models import Band, BandFile

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
        raise Exception("There is no band with this id.")

    if band.members.filter(username=user.username).exists():
        raise Exception(user.username + " is already rocking in this band!")

    band.members.add(user)
    band.save()
    return band
    
def remove_band_member(band_id, username):
    band = get_band(band_id)
    if band is None:
        raise Exception("There is no band with this id.")

    if not band.members.filter(username=username).exists():
        raise Exception(username + " is not a member of this band.")

    band.members.remove(user)
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
        
def add_files(band_id, name, upload_file):
    filename = upload_file.name
    size = upload_file.size
    band_file = BandFile.objects.create(name=name, filename=filename, size=size, uploader='', band=get_band(band_id))
    try:
        destination = open('project/upload_files/%s' % band_file.id, 'wb+')
        for chunk in upload_file.chunks():
            destination.write(chunk)
        destination.close()
    except Exception as exc:
       raise Exception("Error adding a file. Reason: " + exc.message)
    band_file.save()
    
