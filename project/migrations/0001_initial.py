# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Song'
        db.create_table('project_song', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('artist', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('project', ['Song'])

        # Adding model 'Setlist'
        db.create_table('project_setlist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('project', ['Setlist'])

        # Adding M2M table for field songs on 'Setlist'
        db.create_table('project_setlist_songs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('setlist', models.ForeignKey(orm['project.setlist'], null=False)),
            ('song', models.ForeignKey(orm['project.song'], null=False))
        ))
        db.create_unique('project_setlist_songs', ['setlist_id', 'song_id'])

        # Adding model 'UserProfile'
        db.create_table('project_userprofile', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
        ))
        db.send_create_signal('project', ['UserProfile'])

        # Adding model 'Contact'
        db.create_table('project_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('service', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('added', self.gf('django.db.models.fields.DateField')()),
            ('added_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('project', ['Contact'])

        # Adding model 'Band'
        db.create_table('project_band', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('bio', self.gf('django.db.models.fields.TextField')(max_length=1000, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('setlist', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['project.Setlist'], unique=True, null=True)),
        ))
        db.send_create_signal('project', ['Band'])

        # Adding M2M table for field members on 'Band'
        db.create_table('project_band_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('band', models.ForeignKey(orm['project.band'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('project_band_members', ['band_id', 'user_id'])

        # Adding M2M table for field contacts on 'Band'
        db.create_table('project_band_contacts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('band', models.ForeignKey(orm['project.band'], null=False)),
            ('contact', models.ForeignKey(orm['project.contact'], null=False))
        ))
        db.create_unique('project_band_contacts', ['band_id', 'contact_id'])

        # Adding model 'BandFile'
        db.create_table('project_bandfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('uploader', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('band', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project.Band'])),
            ('created', self.gf('django.db.models.fields.DateField')()),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('project', ['BandFile'])

        # Adding M2M table for field attachments on 'BandFile'
        db.create_table('project_bandfile_attachments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bandfile', models.ForeignKey(orm['project.bandfile'], null=False)),
            ('song', models.ForeignKey(orm['project.song'], null=False))
        ))
        db.create_unique('project_bandfile_attachments', ['bandfile_id', 'song_id'])

        # Adding model 'Unavailability'
        db.create_table('project_unavailability', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_start', self.gf('django.db.models.fields.DateField')()),
            ('time_start', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('time_end', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('band', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project.Band'])),
            ('added_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('all_day', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_end', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal('project', ['Unavailability'])

        # Adding model 'Rehearsal'
        db.create_table('project_rehearsal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_start', self.gf('django.db.models.fields.DateField')()),
            ('time_start', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('time_end', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('band', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project.Band'])),
            ('added_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('project', ['Rehearsal'])

        # Adding model 'Gig'
        db.create_table('project_gig', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_start', self.gf('django.db.models.fields.DateField')()),
            ('time_start', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('time_end', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('band', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project.Band'])),
            ('added_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('project', ['Gig'])

        # Adding model 'EventSetlist'
        db.create_table('project_eventsetlist', (
            ('setlist_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['project.Setlist'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('project', ['EventSetlist'])

        # Adding model 'UserInvitation'
        db.create_table('project_userinvitation', (
            ('key', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('band', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project.Band'], unique=True)),
        ))
        db.send_create_signal('project', ['UserInvitation'])


    def backwards(self, orm):
        
        # Deleting model 'Song'
        db.delete_table('project_song')

        # Deleting model 'Setlist'
        db.delete_table('project_setlist')

        # Removing M2M table for field songs on 'Setlist'
        db.delete_table('project_setlist_songs')

        # Deleting model 'UserProfile'
        db.delete_table('project_userprofile')

        # Deleting model 'Contact'
        db.delete_table('project_contact')

        # Deleting model 'Band'
        db.delete_table('project_band')

        # Removing M2M table for field members on 'Band'
        db.delete_table('project_band_members')

        # Removing M2M table for field contacts on 'Band'
        db.delete_table('project_band_contacts')

        # Deleting model 'BandFile'
        db.delete_table('project_bandfile')

        # Removing M2M table for field attachments on 'BandFile'
        db.delete_table('project_bandfile_attachments')

        # Deleting model 'Unavailability'
        db.delete_table('project_unavailability')

        # Deleting model 'Rehearsal'
        db.delete_table('project_rehearsal')

        # Deleting model 'Gig'
        db.delete_table('project_gig')

        # Deleting model 'EventSetlist'
        db.delete_table('project_eventsetlist')

        # Deleting model 'UserInvitation'
        db.delete_table('project_userinvitation')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'project.band': {
            'Meta': {'object_name': 'Band'},
            'bio': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['project.Contact']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'setlist': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['project.Setlist']", 'unique': 'True', 'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'project.bandfile': {
            'Meta': {'object_name': 'BandFile'},
            'attachments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['project.Song']", 'symmetrical': 'False'}),
            'band': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['project.Band']"}),
            'created': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'uploader': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'project.contact': {
            'Meta': {'object_name': 'Contact'},
            'added': ('django.db.models.fields.DateField', [], {}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'service': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'project.eventsetlist': {
            'Meta': {'object_name': 'EventSetlist', '_ormbases': ['project.Setlist']},
            'setlist_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['project.Setlist']", 'unique': 'True', 'primary_key': 'True'})
        },
        'project.gig': {
            'Meta': {'object_name': 'Gig'},
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'band': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['project.Band']"}),
            'date_start': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'time_end': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'time_start': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'project.rehearsal': {
            'Meta': {'object_name': 'Rehearsal'},
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'band': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['project.Band']"}),
            'date_start': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_end': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'time_start': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'project.setlist': {
            'Meta': {'object_name': 'Setlist'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'songs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['project.Song']", 'symmetrical': 'False'})
        },
        'project.song': {
            'Meta': {'object_name': 'Song'},
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'project.unavailability': {
            'Meta': {'object_name': 'Unavailability'},
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'all_day': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'band': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['project.Band']"}),
            'date_end': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_end': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'time_start': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'project.userinvitation': {
            'Meta': {'object_name': 'UserInvitation'},
            'band': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['project.Band']", 'unique': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'})
        },
        'project.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['project']
