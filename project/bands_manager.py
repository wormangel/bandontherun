from models import Band, BandFile

from datetime import datetime

import os


FILES_PATH = "project/upload_files/"

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

    band.members.remove(username)
    band.save()
    return band
    
def get_band(band_id):
    return Band.objects.get(id=band_id)
        
def add_file(band_id, name, username, upload_file):
    filename = upload_file.name
    size = upload_file.size
    band_file = BandFile(name=name, filename=filename, size=size, uploader=username, band=get_band(band_id), created=datetime.now())
    band_file.save()
    try:
        destination = open('%s%s' % (FILES_PATH, band_file.id), 'wb+')
        for chunk in upload_file.chunks():
            destination.write(chunk)
        destination.close()
    except Exception as exc:
       band_file.delete()
       raise Exception("Error adding a file. Reason: " + exc.message)
    
def delete_file(bandfile_id):
    bandfile = BandFile.objects.get(id=bandfile_id)
    if bandfile is None:
        raise Exception("There is no bandfile with this id.")
    os.remove('%s%s' % (FILES_PATH, bandfile_id))
    bandfile.delete()
    
