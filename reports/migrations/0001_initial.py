# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LeadSummaryReports'
        db.create_table(u'reports_leadsummaryreports', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('total_leads', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=10)),
            ('win', self.gf('django.db.models.fields.FloatField')(default=0, max_length=10)),
            ('implemented', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=10)),
            ('in_queue', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=10)),
            ('in_progress', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=10)),
            ('tat_implemented', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=10)),
            ('tat_first_contacted', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=10)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'reports', ['LeadSummaryReports'])


    def backwards(self, orm):
        # Deleting model 'LeadSummaryReports'
        db.delete_table(u'reports_leadsummaryreports')


    models = {
        u'reports.leadsummaryreports': {
            'Meta': {'object_name': 'LeadSummaryReports'},
            'code_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implemented': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'in_progress': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'in_queue': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'tat_first_contacted': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'tat_implemented': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'total_leads': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'win': ('django.db.models.fields.FloatField', [], {'default': '0', 'max_length': '10'})
        }
    }

    complete_apps = ['reports']