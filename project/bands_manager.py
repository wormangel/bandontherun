from datetime import date as date
from models import Band
from project.models import Song, Setlist, Contact, Unavailability
import users_manager

FILES_PATH = "project/upload_files/"

def create_band(name, bio, url, user):
    try:
        band = Band.objects.create(name=name, bio=bio, url=url)

        band.members.add(user)
        band.setlist = Setlist.objects.create()
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

def add_setlist_song(band_id, artist, title):
    try:
        band = get_band(band_id)

        song = Song.objects.filter(artist = artist, title = title)
        if len(song) == 0:
            song = Song.objects.create(artist = artist, title = title)
        else:
            song = song[0]

        print band.setlist
        if band.setlist.contains(song):
            raise Exception("This song is already on the setlist!")

        band.setlist.songs.add(song)
        band.save()
        return band
    except Exception as exc:
        raise Exception("Error adding song: %s" % exc.message)

def remove_setlist_song(band_id, song_id):
    try:
        band = get_band(band_id)
        song = Song.objects.get(id=song_id)

        if not band.setlist.contains(song):
            raise Exception("This song is not on the setlist!")

        band.setlist.songs.remove(song)
        band.save()
        return band
    except Exception as exc:
        raise Exception("Error removing song: %s" % exc.message)

def get_band(band_id):
    try:
        band = Band.objects.get(id=band_id)
        return band
    except Band.DoesNotExist:
        raise Exception("There is no band associated with id %s." % band_id)
        
def remove_contact(band_id, contact_id):
    try:
        band = get_band(band_id)
        contact = Contact.objects.get(id=contact_id)

        if not band.contains_contact(contact):
            raise Exception("This contact is not exists!")

        band.contacts.remove(contact)
        band.save()
        return band
    except Exception as exc:
        raise Exception("Error removing contact: %s" % exc.message)


def add_contact(band_id, name, phone, service, cost, added, added_by):
    try:
        band = get_band(band_id)

        contact = Contact.objects.filter(name = name, phone = phone)
        if len(contact) == 0:
            contact = Contact.objects.create(name=name, phone=phone, service=service, cost=cost, added=added, added_by=added_by)
        else:
            contact = contact[0]

        print band.contacts
        if band.contains_contact(contact):
            raise Exception("This contact is already on the band list!")

        band.contacts.add(contact)
        band.save()
        return band
    except Exception as exc:
        raise Exception("Error adding contact: %s" % exc.message)

def add_unavailability_entry(band_id, date, start, end, user):
    band = get_band(band_id)
    entry = Unavailability.objects.create(date=date, start=start, end=end, band=band, user=user)
    entry.save()

