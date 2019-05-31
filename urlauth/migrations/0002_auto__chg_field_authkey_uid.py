# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'AuthKey.uid'
        db.alter_column('urlauth_authkey', 'uid', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'AuthKey.uid'
        raise RuntimeError("Cannot reverse this migration. 'AuthKey.uid' and its values cannot be restored.")


    models = {
        'urlauth.authkey': {
            'Meta': {'object_name': 'AuthKey'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {}),
            'expired': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'}),
            'onetime': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'uid': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['urlauth']
