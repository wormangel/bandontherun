from models import Band
from project.models import Song, Setlist
import users_manager


FILES_PATH = "project/upload_files/"

def create_band(name, bio, url, user):
    try:
        band = Band.objects.create(name=name, bio=bio, url=url, setlist=Setlist())
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

def add_band_member(band_id, username):
    try:
        band = get_band(band_id)
        user = users_manager.get_user(username)

        if band.is_member(user):
            raise Exception(username + " is already rocking in this band!")

        band.members.add(user)
        band.save()
        return band
    except Exception as exc:
        raise Exception("Error adding member: %s" % exc.message)
    
def remove_band_member(band_id, username):
    try:
        band = get_band(band_id)
        user = users_manager.get_user(username)
        
        if not band.is_member(user):
            raise Exception(username + " is not a member of this band.")

        band.members.remove(user)
        band.save()
        return band
    except Exception as exc:
        raise Exception("Error removing member: %s" % exc.message)

# TODO Vitor, falta isso embaixo :P esse e o remove_setlist_song (provavelmente eh so copiar o remove_member e sair mudando)

def add_setlist_song(band_id, artist, title):
    try:
        band = get_band(band_id)
        song = Song(artist=artist, title=title)

        if band.set_list.contains(song):
            raise Exception("This song is already on the setlist!")

        print band.setlist
        band.setlist.song_list.add(song)
        band.save()
        return band
    except Exception as exc:
        raise Exception("Error adding song: %s" % exc.message)

def get_band(band_id):
    try:
        band = Band.objects.get(id=band_id)
        return band
    except Band.DoesNotExist:
        raise Exception("There is no band associated with id %s." % band_id)