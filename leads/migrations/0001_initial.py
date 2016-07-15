# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Leads'
        db.create_table(u'leads_leads', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('google_rep_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('google_rep_email', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ecommerce', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('lead_owner', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lead_status', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('customer_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('first_name_optional', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name_optional', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('phone_optional', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email_optional', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('date_of_installation', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('time_zone', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('regalix_comment', self.gf('django.db.models.fields.TextField')()),
            ('google_comment', self.gf('django.db.models.fields.TextField')()),
            ('code_1', self.gf('django.db.models.fields.TextField')()),
            ('url_1', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type_1', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('comment_1', self.gf('django.db.models.fields.TextField')()),
            ('code_2', self.gf('django.db.models.fields.TextField')()),
            ('url_2', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type_2', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('comment_2', self.gf('django.db.models.fields.TextField')()),
            ('code_3', self.gf('django.db.models.fields.TextField')()),
            ('url_3', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type_3', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('comment_3', self.gf('django.db.models.fields.TextField')()),
            ('code_4', self.gf('django.db.models.fields.TextField')()),
            ('url_4', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type_4', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('comment_4', self.gf('django.db.models.fields.TextField')()),
            ('code_5', self.gf('django.db.models.fields.TextField')()),
            ('url_5', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type_5', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('comment_5', self.gf('django.db.models.fields.TextField')()),
            ('no_of_calls_inbound', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('no_of_calls_outbound', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('emails_sent', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('emails_received', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('call_recordings', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('email_logs', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('team', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_active', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 7, 17, 0, 0))),
            ('updated_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 7, 17, 0, 0), auto_now=True, blank=True)),
            ('sf_lead_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'leads', ['Leads'])


    def backwards(self, orm):
        # Deleting model 'Leads'
        db.delete_table(u'leads_leads')


    models = {
        u'leads.leads': {
            'Meta': {'object_name': 'Leads'},
            'call_recordings': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'code_1': ('django.db.models.fields.TextField', [], {}),
            'code_2': ('django.db.models.fields.TextField', [], {}),
            'code_3': ('django.db.models.fields.TextField', [], {}),
            'code_4': ('django.db.models.fields.TextField', [], {}),
            'code_5': ('django.db.models.fields.TextField', [], {}),
            'comment_1': ('django.db.models.fields.TextField', [], {}),
            'comment_2': ('django.db.models.fields.TextField', [], {}),
            'comment_3': ('django.db.models.fields.TextField', [], {}),
            'comment_4': ('django.db.models.fields.TextField', [], {}),
            'comment_5': ('django.db.models.fields.TextField', [], {}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 17, 0, 0)'}),
            'customer_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'date_of_installation': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'ecommerce': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'email_logs': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'email_optional': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'emails_received': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'emails_sent': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'first_name_optional': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'google_comment': ('django.db.models.fields.TextField', [], {}),
            'google_rep_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'google_rep_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'last_name_optional': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'lead_owner': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'lead_status': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'no_of_calls_inbound': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'no_of_calls_outbound': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone_optional': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'regalix_comment': ('django.db.models.fields.TextField', [], {}),
            'sf_lead_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'team': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'time_zone': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'type_1': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'type_2': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'type_3': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'type_4': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'type_5': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 17, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'url_1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_2': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_3': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_4': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_5': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['leads']