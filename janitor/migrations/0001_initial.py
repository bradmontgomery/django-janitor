# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FieldSanitizer'
        db.create_table('janitor_fieldsanitizer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('tags', self.gf('django.db.models.fields.TextField')(default='a, abbr, acronym, blockquote, cite, code, dd, del, dfn, dl, dt, em, h1, h2, h3, h4, h5, h6, hr, img, ins, kbd, li, ol, p, pre, q, samp, strong, ul', blank=True)),
            ('attributes', self.gf('django.db.models.fields.TextField')(default='alt, class, href, id, src, title', blank=True)),
            ('styles', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('strip', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('strip_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('janitor', ['FieldSanitizer'])

        # Adding unique constraint on 'FieldSanitizer', fields ['content_type', 'field_name']
        db.create_unique('janitor_fieldsanitizer', ['content_type_id', 'field_name'])


    def backwards(self, orm):
        # Removing unique constraint on 'FieldSanitizer', fields ['content_type', 'field_name']
        db.delete_unique('janitor_fieldsanitizer', ['content_type_id', 'field_name'])

        # Deleting model 'FieldSanitizer'
        db.delete_table('janitor_fieldsanitizer')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'janitor.fieldsanitizer': {
            'Meta': {'ordering': "['content_type', 'field_name']", 'unique_together': "(('content_type', 'field_name'),)", 'object_name': 'FieldSanitizer'},
            'attributes': ('django.db.models.fields.TextField', [], {'default': "'alt, class, href, id, src, title'", 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'strip': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'strip_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'styles': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('django.db.models.fields.TextField', [], {'default': "'a, abbr, acronym, blockquote, cite, code, dd, del, dfn, dl, dt, em, h1, h2, h3, h4, h5, h6, hr, img, ins, kbd, li, ol, p, pre, q, samp, strong, ul'", 'blank': 'True'})
        }
    }

    complete_apps = ['janitor']