# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CSATReport'
        db.create_table(u'reports_csatreport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('customer_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('cli', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True)),
            ('q1', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=10)),
            ('q2', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=10)),
            ('q3', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=10)),
            ('q4', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=10)),
            ('q5', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=10)),
            ('sf_lead_id', self.gf('django.db.models.fields.CharField')(default=None, max_length=50)),
            ('survey_date', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('channel', self.gf('django.db.models.fields.CharField')(default='PHONE', max_length=10)),
            ('process', self.gf('django.db.models.fields.CharField')(default='TAG', max_length=10)),
            ('category', self.gf('django.db.models.fields.CharField')(default='UNMAPPPED', max_length=10)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'reports', ['CSATReport'])


    def backwards(self, orm):
        # Deleting model 'CSATReport'
        db.delete_table(u'reports_csatreport')


    models = {
        u'leads.language': {
            'Meta': {'object_name': 'Language', 'db_table': "'languages'"},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'language_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'leads.location': {
            'Meta': {'ordering': "['location_name']", 'object_name': 'Location', 'db_table': "'locations'"},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'daylight_end': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'daylight_start': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ds_time_zone': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'daylight_timezone'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['leads.Timezone']"}),
            'flag_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'language': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['leads.Language']", 'symmetrical': 'False'}),
            'location_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'primary_language': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'primary_language'", 'to': u"orm['leads.Language']"}),
            'time_zone': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'standard_timezone'", 'symmetrical': 'False', 'to': u"orm['leads.Timezone']"})
        },
        u'leads.team': {
            'Meta': {'ordering': "['team_name']", 'object_name': 'Team', 'db_table': "'teams'"},
            'belongs_to': ('django.db.models.fields.CharField', [], {'default': "'TAG'", 'max_length': '10'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'team_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'leads.timezone': {
            'Meta': {'ordering': "['zone_name']", 'object_name': 'Timezone', 'db_table': "'timezone'"},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'time_value': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'zone_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        u'reports.calllogaccountmanager': {
            'Meta': {'object_name': 'CallLogAccountManager', 'db_table': "'call_log_account_manager'"},
            'alternate_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'call_status': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_time_stamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'meeting_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'seller_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'seller_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sheet_row_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'reports.csatreport': {
            'Meta': {'object_name': 'CSATReport'},
            'category': ('django.db.models.fields.CharField', [], {'default': "'UNMAPPPED'", 'max_length': '10'}),
            'channel': ('django.db.models.fields.CharField', [], {'default': "'PHONE'", 'max_length': '10'}),
            'cli': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'process': ('django.db.models.fields.CharField', [], {'default': "'TAG'", 'max_length': '10'}),
            'q1': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'q2': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'q3': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'q4': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'q5': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'sf_lead_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50'}),
            'survey_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
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
        },
        u'reports.quartertargetleads': {
            'Meta': {'ordering': "['target_leads']", 'unique_together': "(('program', 'location', 'quarter', 'year'),)", 'object_name': 'QuarterTargetLeads', 'db_table': "'quarter_target_leads'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leads.Location']"}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leads.Team']"}),
            'quarter': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'target_leads': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2015', 'max_length': '4'})
        },
        u'reports.region': {
            'Meta': {'ordering': "['name']", 'object_name': 'Region', 'db_table': "'regions'"},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['leads.Location']", 'symmetrical': 'False'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['reports']