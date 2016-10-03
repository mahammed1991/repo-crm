# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UmmDailyTracker'
        db.create_table('umm_daily_tracker', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ldap', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, blank=True)),
            ('days_worked', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('days_out_of_office', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('uaa_target', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('uaa_achieved', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('pts_target', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('pts_won', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('region', self.gf('django.db.models.fields.CharField')(default=None, max_length=100)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'umm', ['UmmDailyTracker'])

        # Adding model 'QualityFeedbackForm'
        db.create_table('quality_feedback_form', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ldap', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('date_of_review', self.gf('django.db.models.fields.DateTimeField')()),
            ('feedback_notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('final_score', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
        ))
        db.send_create_signal(u'umm', ['QualityFeedbackForm'])

        # Adding model 'UmmCallData'
        db.create_table('umm_call_data', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ldap', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('umm_call_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('extn_out_call', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_call_time', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
        ))
        db.send_create_signal(u'umm', ['UmmCallData'])


    def backwards(self, orm):
        # Deleting model 'UmmDailyTracker'
        db.delete_table('umm_daily_tracker')

        # Deleting model 'QualityFeedbackForm'
        db.delete_table('quality_feedback_form')

        # Deleting model 'UmmCallData'
        db.delete_table('umm_call_data')


    models = {
        u'umm.qualityfeedbackform': {
            'Meta': {'object_name': 'QualityFeedbackForm', 'db_table': "'quality_feedback_form'"},
            'date_of_review': ('django.db.models.fields.DateTimeField', [], {}),
            'feedback_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'final_score': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ldap': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'umm.ummcalldata': {
            'Meta': {'ordering': "['umm_call_date']", 'object_name': 'UmmCallData', 'db_table': "'umm_call_data'"},
            'extn_out_call': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ldap': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'total_call_time': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'umm_call_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'umm.ummdailytracker': {
            'Meta': {'ordering': "['created_date']", 'object_name': 'UmmDailyTracker', 'db_table': "'umm_daily_tracker'"},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'days_out_of_office': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'days_worked': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ldap': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'blank': 'True'}),
            'pts_target': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'pts_won': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'region': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100'}),
            'uaa_achieved': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'uaa_target': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['umm']