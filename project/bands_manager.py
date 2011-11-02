from datetime import date as date
from models import Band
from project.errors import SongAlreadyOnSetlistError
from project.models import Song, Setlist, Contact, Unavailability, Gig, Rehearsal, AllocatedSong
import users_manager

FILES_PATH = "project/upload_files/"

def create_band(name, bio, url, user):
    try:
        band = Band.objects.create(name=name, bio=bio, url=url)

        band.members.add(user)
        Setlist.objects.create(band = band)
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
            raise Exception(username.username + " is not a member of this band.")
        
        if len(band.members.all()) <= 1:
            raise Exception(username.username + " is the unique representant of this band. Please delete the band to get out.")

        band.members.remove(user)
        band.save()
        return band
    except Exception as exc:
        raise Exception("Error removing member: %s" % exc.message)

def add_setlist_song(band_id, artist, title):
    try:
        band = get_band(band_id)

        song = Song.objects.filter(band = band, artist = artist, title = title)
        if len(song) == 0:
            song = Song.objects.create(band = band, artist = artist, title = title)
        else:
            song = song[0]

        if band.setlist.contains(song):
            raise SongAlreadyOnSetlistError(song, "This song is already on the setlist!")

        aSong = AllocatedSong(setlist=band.setlist, song=song)
        aSong.save()

        return band
    except SongAlreadyOnSetlistError:
        raise
    except Exception as exc:
        raise Exception("Error adding song: %s" % exc.message)

def remove_setlist_song(band_id, song_id):
    try:
        band = get_band(band_id)
        song = get_song(song_id)

        if not band.setlist.contains(song):
            raise Exception("This song is not on the setlist!")

        aSong = AllocatedSong.objects.get(song=song, setlist=band.setlist)
        aSong.delete()
        return band
    except Exception as exc:
        raise Exception("Error removing song: %s" % exc.message)

def get_band(band_id):
    try:
        band = Band.objects.get(id=band_id)
        return band
    except Band.DoesNotExist:
        raise Exception("There is no band associated with id %s." % band_id)

def get_song(song_id):
    try:
        song = Song.objects.get(id=song_id)
        return song
    except Song.DoesNotExist:
        raise Exception("There is no song associated with id %s." % song_id)

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

        if band.contains_contact(contact):
            raise Exception("This contact is already on the band list!")

        band.contacts.add(contact)
        band.save()
        return band
    except Exception as exc:
        raise Exception("Error adding contact: %s" % exc.message)

def add_unavailability_entry(band_id, date_start, date_end, time_start, time_end, all_day, user):
    try:
        band = get_band(band_id)
        entry = Unavailability.objects.create(date_start=date_start, date_end=date_end, time_start=time_start, time_end=time_end, all_day=all_day, band=band, added_by=user)
        entry.save()
    except Exception as exc:
        raise Exception("Error adding unavailability: %s" % exc.message)
    
def remove_unavailability(band_id, entry_id, user):
    try:
        entry = Unavailability.objects.filter(id=entry_id)
        entry.delete()
    except Exception as exc:
        raise Exception("Error removing unavailability: %s" % exc.message)

### Gigs ###

def get_gig(gig_id):
    try:
        gig = Gig.objects.get(id=gig_id)
        return gig
    except Gig.DoesNotExist:
        raise Exception("There is no gig associated with id %s." % gig_id)

def add_gig_entry(band_id, date_start, date_end, time_start, time_end, place, costs, ticket, user):
    try:
        band = get_band(band_id)
        entry = Gig.objects.create(date_start=date_start, date_end=date_end, time_start=time_start, time_end=time_end, place=place, costs=costs, ticket=ticket, band=band, added_by=user)
        entry.setlist = Setlist.objects.create()
        entry.save()
    except Exception as exc:
        raise Exception("Error adding gig: %s" % exc.message)

def update_gig_entry(entry_id, date_start, time_start, time_end, place, costs, ticket):
    try:
        gig = get_gig(entry_id)
        gig.date_start = date_start
        gig.time_start = time_start
        gig.time_end = time_end
        gig.place = place
        gig.costs = costs
        gig.ticket = ticket
        gig.save()
        return gig
    except Exception as exc:
        raise Exception("Error updating gig: %s" % exc.message)
    
def remove_gig(band_id, entry_id, user):
    try:
        entry = Gig.objects.filter(id=entry_id)
        entry.delete()
    except Exception as exc:
        raise Exception("Error removing gig: %s" % exc.message)

def add_gig_song(gig_id, song_id, pos):
    try:
        gig = get_gig(gig_id)
        song = get_song(song_id)

        if gig.setlist.contains(song):
            raise Exception("This song is already on the setlist!")

        newSong = AllocatedSong(setlist=gig.setlist, song=song, position = pos)
        newSong.save()
        
        # advances each song in the setlist after my new position by 1 position
        if (gig.setlist.count > 0):
            for aSong in AllocatedSong.objects.filter(setlist=gig.setlist, position__gte=pos).exclude(song=song):
                aSong.position += 1
                aSong.save()
                
        return gig
    except Exception as exc:
        raise Exception("Error adding song to gig's setlist: %s" % exc.message)

def remove_gig_song(gig_id, song_id):
    try:
        gig = get_gig(gig_id)
        song = get_song(song_id)

        if not gig.setlist.contains(song):
            raise Exception("This song is not on the gig setlist!")

        aSong = AllocatedSong.objects.get(song=song, setlist=gig.setlist)
        pos = aSong.position # my old position
        
        aSong.delete()

        # rewinds each song in the setlist before my position by 1 position
        for aSong in AllocatedSong.objects.filter(setlist=gig.setlist, position__gte=pos).exclude(song=song):
            aSong.position -= 1
            aSong.save()

        return gig
    except Exception as exc:
        raise Exception("Error removing song to gig's setlist: %s" % exc.message)

def sort_gig_setlist(gig_id, song_id, pos):
    try:
        remove_gig_song(gig_id, song_id)
        add_gig_song(gig_id, song_id, pos)

    except Exception as exc:
        raise Exception("Error adding song to gig's setlist: %s" % exc.message)

### Rehearsals ###

def get_rehearsal(rehearsal_id):
    try:
        rehearsal = Rehearsal.objects.get(id=rehearsal_id)
        return rehearsal
    except Rehearsal.DoesNotExist:
        raise Exception("There is no rehearsal associated with id %s." % gig_id)

def add_rehearsal_entry(band_id, date_start, time_start, time_end, place, costs, user):
    try:
        band = get_band(band_id)
        entry = Rehearsal.objects.create(date_start=date_start, time_start=time_start, time_end=time_end, place=place, costs=costs, band=band, added_by=user)
        entry.setlist = Setlist.objects.create()
        entry.save()
    except Exception as exc:
        raise Exception("Error adding rehearsal: %s" % exc.message)

def update_rehearsal_entry(entry_id, date_start, time_start, time_end, place, costs):
    try:
        rehearsal = get_rehearsal(entry_id)
        rehearsal.date_start = date_start
        rehearsal.time_start = time_start
        rehearsal.time_end = time_end
        rehearsal.place = place
        rehearsal.costs = costs
        rehearsal.save()
        return rehearsal
    except Exception as exc:
        raise Exception("Error updating rehearsal: %s" % exc.message)

def remove_rehearsal(band_id, entry_id, user):
    try:
        entry = Rehearsal.objects.filter(id=entry_id)
        entry.delete()
    except Exception as exc:
        raise Exception("Error removing rehearsal: %s" % exc.message)

def add_rehearsal_song(rehearsal_id, song_id, pos):
    try:
        rehearsal = get_rehearsal(rehearsal_id)
        song = get_song(song_id)

        if rehearsal.setlist.contains(song):
            raise Exception("This song is already on the setlist!")

        aSong = AllocatedSong(setlist=rehearsal.setlist, song=song, position=pos)
        aSong.save()

        # advances each song in the setlist after my new position by 1 position
        if (rehearsal.setlist.count > 0):
            for aSong in AllocatedSong.objects.filter(setlist=rehearsal.setlist, position__gte=pos).exclude(song=song):
                aSong.position += 1
                aSong.save()

        return rehearsal
    except Exception as exc:
        raise Exception("Error adding song to rehearsal's setlist: %s" % exc.message)

def remove_rehearsal_song(rehearsal_id, song_id):
    try:
        rehearsal = get_rehearsal(rehearsal_id)
        song = get_song(song_id)

        if not rehearsal.setlist.contains(song):
            raise Exception("This song is not on the rehearsal setlist!")

        aSong = AllocatedSong.objects.get(song=song, setlist=rehearsal.setlist)
        pos = aSong.position # my old position
        
        aSong.delete()

        # rewinds each song in the setlist before my position by 1 position
        for aSong in AllocatedSong.objects.filter(setlist=rehearsal.setlist, position__gte=pos).exclude(song=song):
            aSong.position -= 1
            aSong.save()

        return rehearsal
    except Exception as exc:
        raise Exception("Error removing song to rehearsal's setlist: %s" % exc.message)

def sort_rehearsal_setlist(rehearsal_id, song_id, pos):
    try:
        remove_rehearsal_song(rehearsal_id, song_id)
        add_rehearsal_song(rehearsal_id, song_id, pos)

    except Exception as exc:
        raise Exception("Error sorting rehearsal's setlist: %s" % exc.message)
        
def has_unavailabilities(band_id, date_start, date_end):
    band = get_band(band_id)
    return len(Unavailability.objects.filter(date_start__lte=date_start, date_end__gte=date_end, band=band)) > 0
