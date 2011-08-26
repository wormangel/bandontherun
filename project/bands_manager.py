from models import Band

def create_band(band_name, shortcut_name, bio, url, user):
    band = Band.objects.create(name=band_name, shortcut_name=shortcut_name, bio=bio, url=url)
    band.members.add(user)
    band.save()
    return band
    
def get_band(name):
    band = Band.objects.filter(name=name)
