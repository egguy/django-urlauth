# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AuthKey'
        db.create_table('urlauth_authkey', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=40, primary_key=True)),
            ('uid', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('expired', self.gf('django.db.models.fields.DateTimeField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('onetime', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('urlauth', ['AuthKey'])


    def backwards(self, orm):
        
        # Deleting model 'AuthKey'
        db.delete_table('urlauth_authkey')


    models = {
        'urlauth.authkey': {
            'Meta': {'object_name': 'AuthKey'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {}),
            'expired': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'}),
            'onetime': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'uid': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['urlauth']
