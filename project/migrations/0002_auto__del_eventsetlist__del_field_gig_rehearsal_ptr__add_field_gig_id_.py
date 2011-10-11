# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'EventSetlist'
        db.delete_table('project_eventsetlist')

        # Deleting field 'Gig.rehearsal_ptr'
        db.delete_column('project_gig', 'rehearsal_ptr_id')

        # Adding field 'Gig.id'
        db.add_column('project_gig', 'id', self.gf('django.db.models.fields.AutoField')(default=0, primary_key=True), keep_default=False)

        # Adding field 'Gig.date_start'
        db.add_column('project_gig', 'date_start', self.gf('django.db.models.fields.DateField')(default=0), keep_default=False)

        # Adding field 'Gig.time_start'
        db.add_column('project_gig', 'time_start', self.gf('django.db.models.fields.CharField')(default=0, max_length=5), keep_default=False)

        # Adding field 'Gig.time_end'
        db.add_column('project_gig', 'time_end', self.gf('django.db.models.fields.CharField')(default=0, max_length=5), keep_default=False)

        # Adding field 'Gig.band'
        db.add_column('project_gig', 'band', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['project.Band']), keep_default=False)

        # Adding field 'Gig.added_by'
        db.add_column('project_gig', 'added_by', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['auth.User']), keep_default=False)

        # Adding field 'Gig.place'
        db.add_column('project_gig', 'place', self.gf('django.db.models.fields.CharField')(default=0, max_length=30), keep_default=False)

        # Adding field 'Gig.costs'
        db.add_column('project_gig', 'costs', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2, blank=True), keep_default=False)

        # Adding field 'Gig.setlist'
        db.add_column('project_gig', 'setlist', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['project.Setlist'], unique=True, null=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'EventSetlist'
        db.create_table('project_eventsetlist', (
            ('setlist_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['project.Setlist'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('project', ['EventSetlist'])

        # Adding field 'Gig.rehearsal_ptr'
        db.add_column('project_gig', 'rehearsal_ptr', self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['project.Rehearsal'], unique=True, primary_key=True), keep_default=False)

        # Deleting field 'Gig.id'
        db.delete_column('project_gig', 'id')

        # Deleting field 'Gig.date_start'
        db.delete_column('project_gig', 'date_start')

        # Deleting field 'Gig.time_start'
        db.delete_column('project_gig', 'time_start')

        # Deleting field 'Gig.time_end'
        db.delete_column('project_gig', 'time_end')

        # Deleting field 'Gig.band'
        db.delete_column('project_gig', 'band_id')

        # Deleting field 'Gig.added_by'
        db.delete_column('project_gig', 'added_by_id')

        # Deleting field 'Gig.place'
        db.delete_column('project_gig', 'place')

        # Deleting field 'Gig.costs'
        db.delete_column('project_gig', 'costs')

        # Deleting field 'Gig.setlist'
        db.delete_column('project_gig', 'setlist_id')


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
        'project.gig': {
            'Meta': {'object_name': 'Gig'},
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'band': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['project.Band']"}),
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['project.BandFile']"}),
            'costs': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'setlist': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['project.Setlist']", 'unique': 'True', 'null': 'True'}),
            'ticket': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'time_end': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'time_start': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'project.rehearsal': {
            'Meta': {'object_name': 'Rehearsal'},
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'band': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['project.Band']"}),
            'costs': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'setlist': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['project.Setlist']", 'unique': 'True', 'null': 'True'}),
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
