from models import Band

def create_band(band_name, shortcut_name, bio, url, user):
    band = Band.objects.create(name=band_name, shortcut_name=shortcut_name, bio=bio, url=url)
    band.members.add(user)
    band.save()
    return band
    
def update_band(band_name, shortcut_name, bio, url):
    band = Band.objects.create(name=band_name, shortcut_name=shortcut_name, bio=bio, url=url)
    band.members.add(user)
    band.save()
    return band
    
def add_band_member(shortcut_name, user):
    band = get_band(shortcut_name)
    band.members.add(user)
    band.save()
    return band
    
def remove_band_member(shortcut_name, user):
    band = get_band(shortcut_name)
    band.members.remove(user)
    band.save()
    return band
    
def get_band(name):
    band = Band.objects.filter(name=name)
