# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'KickOffProgram.created_date'
        db.add_column(u'reports_kickoffprogram', 'created_date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2016, 2, 11, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'KickOffProgram.modified_date'
        db.add_column(u'reports_kickoffprogram', 'modified_date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, default=datetime.datetime(2016, 2, 11, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'KickOffProgram.created_date'
        db.delete_column(u'reports_kickoffprogram', 'created_date')

        # Deleting field 'KickOffProgram.modified_date'
        db.delete_column(u'reports_kickoffprogram', 'modified_date')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
        u'reports.csatfilterdetails': {
            'Meta': {'object_name': 'CSATFilterDetails'},
            'agent_language': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['leads.Language']", 'symmetrical': 'False'}),
            'channel': ('django.db.models.fields.CharField', [], {'default': "'PHONE'", 'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_category': ('django.db.models.fields.CharField', [], {'default': "'English'", 'max_length': '11'}),
            'lead_owners': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'process': ('django.db.models.fields.CharField', [], {'default': "'TAG'", 'max_length': '10'}),
            'survey_pin_number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'tagteam_location': ('django.db.models.fields.CharField', [], {'default': "'Bangalore'", 'max_length': '10'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'csat_user'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'reports.csatreport': {
            'Meta': {'object_name': 'CSATReport'},
            'category': ('django.db.models.fields.CharField', [], {'default': "'UNMAPPPED'", 'max_length': '10'}),
            'channel': ('django.db.models.fields.CharField', [], {'default': "'PHONE'", 'max_length': '10'}),
            'cli': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True'}),
            'code_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'lead_owner': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'lead_owner_email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'lead_owner_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'mapped_lead_created_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'process': ('django.db.models.fields.CharField', [], {'default': "'TAG'", 'max_length': '10'}),
            'program': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'q1': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'q2': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'q3': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'q4': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'q5': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'region': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'sf_lead_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50'}),
            'survey_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        u'reports.kickoffprogram': {
            'Meta': {'object_name': 'KickOffProgram'},
            'advertiser_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'attached_url_link_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'attached_url_link_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'attached_url_link_3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'attached_url_link_4': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'attached_url_link_5': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'codetypeslist': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'estimated_lead_volume': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'expectations': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'explain_workflow': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file_upload_name': ('jsonfield2.fields.JSONField', [], {'default': '{}', 'blank': 'True'}),
            'file_url_name': ('jsonfield2.fields.JSONField', [], {'default': '{}', 'blank': 'True'}),
            'google_poc': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'google_poc'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'google_poc_email': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'google_poc_email'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'google_poc_locations': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead_sub_mode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'lead_subbmission_other_val': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'program_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'program_overview_objective': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'programe_end_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'programe_start_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'real_time_support_chat': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'real_time_support_live_trans': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['reports.Region']", 'symmetrical': 'False'}),
            'succes_matrix': ('jsonfield2.fields.JSONField', [], {'default': '{}', 'blank': 'True'}),
            'tag_team_connect_detail': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'target_locations': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['leads.Location']", 'symmetrical': 'False'}),
            'upload_file_attachment_1': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'upload_file_attachment_2': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'upload_file_attachment_3': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'upload_file_attachment_4': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'upload_file_attachment_5': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'win_criteria': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'reports.leadsreport': {
            'Meta': {'object_name': 'LeadsReport'},
            'code_type': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 2, 11, 0, 0)'}),
            'customer_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'date_of_installation': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'google_rep_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'google_rep_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'lead_owner_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'lead_owner_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'lead_status': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'lead_sub_status': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'program': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sf_lead_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'tat': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 2, 11, 0, 0)', 'auto_now': 'True', 'blank': 'True'})
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
        u'reports.meetingminutes': {
            'Meta': {'object_name': 'MeetingMinutes'},
            'action_plan': ('jsonfield2.fields.JSONField', [], {'default': '{}', 'blank': 'True'}),
            'attach_file_name': ('jsonfield2.fields.JSONField', [], {'default': '{}', 'blank': 'True'}),
            'attached_link_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'attached_link_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'attached_link_3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'attached_link_4': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'attached_link_5': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'attachment_1': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'attachment_2': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'attachment_3': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'attachment_4': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'attachment_5': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'attendees': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'attendees'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'bcc': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'bcc'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'google_poc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'google_team': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_points': ('jsonfield2.fields.JSONField', [], {'default': '{}', 'blank': 'True'}),
            'link_file_name': ('jsonfield2.fields.JSONField', [], {'default': '{}', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'meeting_audience': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'meeting_status': ('django.db.models.fields.CharField', [], {'default': "'open'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'meeting_time_in_ist': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'next_meeting_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'other_subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'program': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'program_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'ref_uuid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'regalix_poc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'subject_timeline': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'tenantive_agenda': ('jsonfield2.fields.JSONField', [], {'default': '{}', 'blank': 'True'})
        },
        u'reports.quartertargetleads': {
            'Meta': {'ordering': "['target_leads']", 'unique_together': "(('program', 'location', 'quarter', 'year'),)", 'object_name': 'QuarterTargetLeads', 'db_table': "'quarter_target_leads'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leads.Location']"}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leads.Team']"}),
            'quarter': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'target_leads': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2016', 'max_length': '4'})
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