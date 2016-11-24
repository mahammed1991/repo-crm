# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TagLeadDetail.Spend_cfc'
        db.add_column(u'leads_tagleaddetail', 'Spend_cfc',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.reason_for_conversion_not_reporting'
        db.add_column(u'leads_tagleaddetail', 'reason_for_conversion_not_reporting',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.unethical_win'
        db.add_column(u'leads_tagleaddetail', 'unethical_win',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.other_cms'
        db.add_column(u'leads_tagleaddetail', 'other_cms',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.gcss_exception_approved_by'
        db.add_column(u'leads_tagleaddetail', 'gcss_exception_approved_by',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.action_taken'
        db.add_column(u'leads_tagleaddetail', 'action_taken',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.on_call_win'
        db.add_column(u'leads_tagleaddetail', 'on_call_win',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.dynamic_value'
        db.add_column(u'leads_tagleaddetail', 'dynamic_value',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=80, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.regalix_webmaster'
        db.add_column(u'leads_tagleaddetail', 'regalix_webmaster',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=150, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.anything_else_we_should_know'
        db.add_column(u'leads_tagleaddetail', 'anything_else_we_should_know',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.not_interested_cases_rca'
        db.add_column(u'leads_tagleaddetail', 'not_interested_cases_rca',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=80, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.lead_bundle'
        db.add_column(u'leads_tagleaddetail', 'lead_bundle',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.alternate_contact_role'
        db.add_column(u'leads_tagleaddetail', 'alternate_contact_role',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.contact_alternate'
        db.add_column(u'leads_tagleaddetail', 'contact_alternate',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.please_specify_if_others'
        db.add_column(u'leads_tagleaddetail', 'please_specify_if_others',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.reporting_status_1'
        db.add_column(u'leads_tagleaddetail', 'reporting_status_1',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.reporting_status_2'
        db.add_column(u'leads_tagleaddetail', 'reporting_status_2',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.reporting_status_3'
        db.add_column(u'leads_tagleaddetail', 'reporting_status_3',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.reporting_status_4'
        db.add_column(u'leads_tagleaddetail', 'reporting_status_4',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.reporting_status_5'
        db.add_column(u'leads_tagleaddetail', 'reporting_status_5',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.analytics_account_id_1'
        db.add_column(u'leads_tagleaddetail', 'analytics_account_id_1',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.analytics_account_id_2'
        db.add_column(u'leads_tagleaddetail', 'analytics_account_id_2',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.analytics_account_id_3'
        db.add_column(u'leads_tagleaddetail', 'analytics_account_id_3',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.analytics_account_id_4'
        db.add_column(u'leads_tagleaddetail', 'analytics_account_id_4',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.analytics_account_id_5'
        db.add_column(u'leads_tagleaddetail', 'analytics_account_id_5',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TagLeadDetail.transaction_behaviour_1'
        db.add_column(u'leads_tagleaddetail', 'transaction_behaviour_1',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.transaction_behaviour_2'
        db.add_column(u'leads_tagleaddetail', 'transaction_behaviour_2',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.transaction_behaviour_3'
        db.add_column(u'leads_tagleaddetail', 'transaction_behaviour_3',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.transaction_behaviour_4'
        db.add_column(u'leads_tagleaddetail', 'transaction_behaviour_4',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.transaction_behaviour_5'
        db.add_column(u'leads_tagleaddetail', 'transaction_behaviour_5',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.check_out_process_1'
        db.add_column(u'leads_tagleaddetail', 'check_out_process_1',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.check_out_process_2'
        db.add_column(u'leads_tagleaddetail', 'check_out_process_2',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.check_out_process_3'
        db.add_column(u'leads_tagleaddetail', 'check_out_process_3',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.check_out_process_4'
        db.add_column(u'leads_tagleaddetail', 'check_out_process_4',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.check_out_process_5'
        db.add_column(u'leads_tagleaddetail', 'check_out_process_5',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.cart_page_behaviour_1'
        db.add_column(u'leads_tagleaddetail', 'cart_page_behaviour_1',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.cart_page_behaviour_2'
        db.add_column(u'leads_tagleaddetail', 'cart_page_behaviour_2',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.cart_page_behaviour_3'
        db.add_column(u'leads_tagleaddetail', 'cart_page_behaviour_3',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.cart_page_behaviour_4'
        db.add_column(u'leads_tagleaddetail', 'cart_page_behaviour_4',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.cart_page_behaviour_5'
        db.add_column(u'leads_tagleaddetail', 'cart_page_behaviour_5',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.created_call_extension_1'
        db.add_column(u'leads_tagleaddetail', 'created_call_extension_1',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.created_call_extension_2'
        db.add_column(u'leads_tagleaddetail', 'created_call_extension_2',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.created_call_extension_3'
        db.add_column(u'leads_tagleaddetail', 'created_call_extension_3',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.created_call_extension_4'
        db.add_column(u'leads_tagleaddetail', 'created_call_extension_4',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.created_call_extension_5'
        db.add_column(u'leads_tagleaddetail', 'created_call_extension_5',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.analytics_code_is_setup_1'
        db.add_column(u'leads_tagleaddetail', 'analytics_code_is_setup_1',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.analytics_code_is_setup_2'
        db.add_column(u'leads_tagleaddetail', 'analytics_code_is_setup_2',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.analytics_code_is_setup_3'
        db.add_column(u'leads_tagleaddetail', 'analytics_code_is_setup_3',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.analytics_code_is_setup_4'
        db.add_column(u'leads_tagleaddetail', 'analytics_code_is_setup_4',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.analytics_code_is_setup_5'
        db.add_column(u'leads_tagleaddetail', 'analytics_code_is_setup_5',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.product_behaviour_1'
        db.add_column(u'leads_tagleaddetail', 'product_behaviour_1',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.product_behaviour_2'
        db.add_column(u'leads_tagleaddetail', 'product_behaviour_2',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.product_behaviour_3'
        db.add_column(u'leads_tagleaddetail', 'product_behaviour_3',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.product_behaviour_4'
        db.add_column(u'leads_tagleaddetail', 'product_behaviour_4',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'TagLeadDetail.product_behaviour_5'
        db.add_column(u'leads_tagleaddetail', 'product_behaviour_5',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'TagLeadDetail.Spend_cfc'
        db.delete_column(u'leads_tagleaddetail', 'Spend_cfc')

        # Deleting field 'TagLeadDetail.reason_for_conversion_not_reporting'
        db.delete_column(u'leads_tagleaddetail', 'reason_for_conversion_not_reporting')

        # Deleting field 'TagLeadDetail.unethical_win'
        db.delete_column(u'leads_tagleaddetail', 'unethical_win')

        # Deleting field 'TagLeadDetail.other_cms'
        db.delete_column(u'leads_tagleaddetail', 'other_cms')

        # Deleting field 'TagLeadDetail.gcss_exception_approved_by'
        db.delete_column(u'leads_tagleaddetail', 'gcss_exception_approved_by')

        # Deleting field 'TagLeadDetail.action_taken'
        db.delete_column(u'leads_tagleaddetail', 'action_taken')

        # Deleting field 'TagLeadDetail.on_call_win'
        db.delete_column(u'leads_tagleaddetail', 'on_call_win')

        # Deleting field 'TagLeadDetail.dynamic_value'
        db.delete_column(u'leads_tagleaddetail', 'dynamic_value')

        # Deleting field 'TagLeadDetail.regalix_webmaster'
        db.delete_column(u'leads_tagleaddetail', 'regalix_webmaster')

        # Deleting field 'TagLeadDetail.anything_else_we_should_know'
        db.delete_column(u'leads_tagleaddetail', 'anything_else_we_should_know')

        # Deleting field 'TagLeadDetail.not_interested_cases_rca'
        db.delete_column(u'leads_tagleaddetail', 'not_interested_cases_rca')

        # Deleting field 'TagLeadDetail.lead_bundle'
        db.delete_column(u'leads_tagleaddetail', 'lead_bundle')

        # Deleting field 'TagLeadDetail.alternate_contact_role'
        db.delete_column(u'leads_tagleaddetail', 'alternate_contact_role')

        # Deleting field 'TagLeadDetail.contact_alternate'
        db.delete_column(u'leads_tagleaddetail', 'contact_alternate')

        # Deleting field 'TagLeadDetail.please_specify_if_others'
        db.delete_column(u'leads_tagleaddetail', 'please_specify_if_others')

        # Deleting field 'TagLeadDetail.reporting_status_1'
        db.delete_column(u'leads_tagleaddetail', 'reporting_status_1')

        # Deleting field 'TagLeadDetail.reporting_status_2'
        db.delete_column(u'leads_tagleaddetail', 'reporting_status_2')

        # Deleting field 'TagLeadDetail.reporting_status_3'
        db.delete_column(u'leads_tagleaddetail', 'reporting_status_3')

        # Deleting field 'TagLeadDetail.reporting_status_4'
        db.delete_column(u'leads_tagleaddetail', 'reporting_status_4')

        # Deleting field 'TagLeadDetail.reporting_status_5'
        db.delete_column(u'leads_tagleaddetail', 'reporting_status_5')

        # Deleting field 'TagLeadDetail.analytics_account_id_1'
        db.delete_column(u'leads_tagleaddetail', 'analytics_account_id_1')

        # Deleting field 'TagLeadDetail.analytics_account_id_2'
        db.delete_column(u'leads_tagleaddetail', 'analytics_account_id_2')

        # Deleting field 'TagLeadDetail.analytics_account_id_3'
        db.delete_column(u'leads_tagleaddetail', 'analytics_account_id_3')

        # Deleting field 'TagLeadDetail.analytics_account_id_4'
        db.delete_column(u'leads_tagleaddetail', 'analytics_account_id_4')

        # Deleting field 'TagLeadDetail.analytics_account_id_5'
        db.delete_column(u'leads_tagleaddetail', 'analytics_account_id_5')

        # Deleting field 'TagLeadDetail.transaction_behaviour_1'
        db.delete_column(u'leads_tagleaddetail', 'transaction_behaviour_1')

        # Deleting field 'TagLeadDetail.transaction_behaviour_2'
        db.delete_column(u'leads_tagleaddetail', 'transaction_behaviour_2')

        # Deleting field 'TagLeadDetail.transaction_behaviour_3'
        db.delete_column(u'leads_tagleaddetail', 'transaction_behaviour_3')

        # Deleting field 'TagLeadDetail.transaction_behaviour_4'
        db.delete_column(u'leads_tagleaddetail', 'transaction_behaviour_4')

        # Deleting field 'TagLeadDetail.transaction_behaviour_5'
        db.delete_column(u'leads_tagleaddetail', 'transaction_behaviour_5')

        # Deleting field 'TagLeadDetail.check_out_process_1'
        db.delete_column(u'leads_tagleaddetail', 'check_out_process_1')

        # Deleting field 'TagLeadDetail.check_out_process_2'
        db.delete_column(u'leads_tagleaddetail', 'check_out_process_2')

        # Deleting field 'TagLeadDetail.check_out_process_3'
        db.delete_column(u'leads_tagleaddetail', 'check_out_process_3')

        # Deleting field 'TagLeadDetail.check_out_process_4'
        db.delete_column(u'leads_tagleaddetail', 'check_out_process_4')

        # Deleting field 'TagLeadDetail.check_out_process_5'
        db.delete_column(u'leads_tagleaddetail', 'check_out_process_5')

        # Deleting field 'TagLeadDetail.cart_page_behaviour_1'
        db.delete_column(u'leads_tagleaddetail', 'cart_page_behaviour_1')

        # Deleting field 'TagLeadDetail.cart_page_behaviour_2'
        db.delete_column(u'leads_tagleaddetail', 'cart_page_behaviour_2')

        # Deleting field 'TagLeadDetail.cart_page_behaviour_3'
        db.delete_column(u'leads_tagleaddetail', 'cart_page_behaviour_3')

        # Deleting field 'TagLeadDetail.cart_page_behaviour_4'
        db.delete_column(u'leads_tagleaddetail', 'cart_page_behaviour_4')

        # Deleting field 'TagLeadDetail.cart_page_behaviour_5'
        db.delete_column(u'leads_tagleaddetail', 'cart_page_behaviour_5')

        # Deleting field 'TagLeadDetail.created_call_extension_1'
        db.delete_column(u'leads_tagleaddetail', 'created_call_extension_1')

        # Deleting field 'TagLeadDetail.created_call_extension_2'
        db.delete_column(u'leads_tagleaddetail', 'created_call_extension_2')

        # Deleting field 'TagLeadDetail.created_call_extension_3'
        db.delete_column(u'leads_tagleaddetail', 'created_call_extension_3')

        # Deleting field 'TagLeadDetail.created_call_extension_4'
        db.delete_column(u'leads_tagleaddetail', 'created_call_extension_4')

        # Deleting field 'TagLeadDetail.created_call_extension_5'
        db.delete_column(u'leads_tagleaddetail', 'created_call_extension_5')

        # Deleting field 'TagLeadDetail.analytics_code_is_setup_1'
        db.delete_column(u'leads_tagleaddetail', 'analytics_code_is_setup_1')

        # Deleting field 'TagLeadDetail.analytics_code_is_setup_2'
        db.delete_column(u'leads_tagleaddetail', 'analytics_code_is_setup_2')

        # Deleting field 'TagLeadDetail.analytics_code_is_setup_3'
        db.delete_column(u'leads_tagleaddetail', 'analytics_code_is_setup_3')

        # Deleting field 'TagLeadDetail.analytics_code_is_setup_4'
        db.delete_column(u'leads_tagleaddetail', 'analytics_code_is_setup_4')

        # Deleting field 'TagLeadDetail.analytics_code_is_setup_5'
        db.delete_column(u'leads_tagleaddetail', 'analytics_code_is_setup_5')

        # Deleting field 'TagLeadDetail.product_behaviour_1'
        db.delete_column(u'leads_tagleaddetail', 'product_behaviour_1')

        # Deleting field 'TagLeadDetail.product_behaviour_2'
        db.delete_column(u'leads_tagleaddetail', 'product_behaviour_2')

        # Deleting field 'TagLeadDetail.product_behaviour_3'
        db.delete_column(u'leads_tagleaddetail', 'product_behaviour_3')

        # Deleting field 'TagLeadDetail.product_behaviour_4'
        db.delete_column(u'leads_tagleaddetail', 'product_behaviour_4')

        # Deleting field 'TagLeadDetail.product_behaviour_5'
        db.delete_column(u'leads_tagleaddetail', 'product_behaviour_5')


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
        u'leads.agencydetails': {
            'Meta': {'object_name': 'AgencyDetails', 'db_table': "'agency_details'"},
            'agency_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'appointment_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 11, 24, 0, 0)'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'google_rep': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leads.Language']", 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leads.Location']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leads.Timezone']"})
        },
        u'leads.argosprocesstimetracker': {
            'Meta': {'object_name': 'ArgosProcessTimeTracker'},
            'assignee': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'assignee'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'assigner': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'assigner'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'attributes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leads.Leads']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'paused_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'products_count': ('django.db.models.fields.IntegerField', [], {}),
            'resumed_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Start'", 'max_length': '10'}),
            'time_spent': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'leads.blacklistedcid': {
            'Meta': {'object_name': 'BlackListedCID'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 11, 24, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'modified_by_user'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 11, 24, 0, 0)', 'auto_now': 'True', 'blank': 'True'})
        },
        u'leads.buildsbolteligibility': {
            'Meta': {'object_name': 'BuildsBoltEligibility', 'db_table': "'builds_bolt_eligibility'"},
            'bolt_eligible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_assessed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'leads.chatmessage': {
            'Meta': {'object_name': 'ChatMessage', 'db_table': "'chat_message'"},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leads.Leads']"}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'leads.codetype': {
            'Meta': {'ordering': "['name']", 'object_name': 'CodeType', 'db_table': "'code_types'"},
            'avg_setup_time': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'leads.contactperson': {
            'Meta': {'object_name': 'ContactPerson', 'db_table': "'contact_person'"},
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leads.AgencyDetails']"}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'contact_person': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'person_id': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'leads.language': {
            'Meta': {'object_name': 'Language', 'db_table': "'languages'"},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'language_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'leads.leadform': {
            'Meta': {'object_name': 'LeadForm', 'db_table': "'lead_forms'"},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'leads.leadformaccesscontrol': {
            'Meta': {'object_name': 'LeadFormAccessControl', 'db_table': "'lead_form_controls'"},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'google_rep': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead_form': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leads.LeadForm']", 'unique': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'programs': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['leads.Team']", 'null': 'True', 'blank': 'True'}),
            'target_location': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['leads.Location']", 'null': 'True', 'blank': 'True'})
        },
        u'leads.leadhistory': {
            'Meta': {'object_name': 'LeadHistory'},
            'action_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_owner': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_guid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_link': ('django.db.models.fields.CharField', [], {'max_length': '600', 'null': 'True', 'blank': 'True'}),
            'lead_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modifications': ('django.db.models.fields.TextField', [], {}),
            'modified_by': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'original_image_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'previous_owner': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'leads.leads': {
            'Meta': {'object_name': 'Leads'},
            'additional_description': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'additional_support_beyond_case': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'appointment_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'appointment_date_in_ist': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'appointment_date_in_pst': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'area_tobe_improved': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'authcase_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'business_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'call_recordings': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'campaign_id_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'campaign_id_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'campaign_id_3': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'campaign_id_4': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'campaign_id_5': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
            'created_by': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 11, 24, 0, 0)'}),
            'customer_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'date_of_installation': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'dials': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ecommerce': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'email_logs': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'email_optional': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'emails_received': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'emails_sent': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'eto_ldap': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'feed_optimisation_status': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'feed_optimisation_sub_status': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'first_contacted_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'first_name_optional': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'gcss': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'google_comment': ('django.db.models.fields.TextField', [], {}),
            'google_rep_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'google_rep_location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'google_rep_manager_email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'google_rep_manager_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'google_rep_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internale_cid_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'internale_cid_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'internale_cid_3': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'internale_cid_4': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'internale_cid_5': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'last_name_optional': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'last_updated_by': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'lead_owner_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'lead_owner_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'lead_status': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'lead_sub_status': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'no_of_calls_inbound': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'no_of_calls_outbound': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'number_of_products': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'override_existing_bid_modifiers_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'override_existing_bid_modifiers_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'override_existing_bid_modifiers_3': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'override_existing_bid_modifiers_4': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'override_existing_bid_modifiers_5': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone_optional': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'primary_contact_role': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'regalix_comment': ('django.db.models.fields.TextField', [], {}),
            'rescheduled_appointment': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'rescheduled_appointment_in_ist': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'rescheduled_appointment_in_pst': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'rlsa_bid_adjustment_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rlsa_bid_adjustment_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rlsa_bid_adjustment_3': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rlsa_bid_adjustment_4': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rlsa_bid_adjustment_5': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sf_lead_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'shopping_feed_link': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'tat': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'time_zone': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'type_1': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'type_2': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'type_3': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'type_4': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'type_5': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 11, 24, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'url_1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_2': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_3': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_4': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_5': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_list_id_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user_list_id_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user_list_id_3': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user_list_id_4': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user_list_id_5': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'webmaster_email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'webmaster_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'webmaster_phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
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
        u'leads.picassoleadgrouptype': {
            'Meta': {'object_name': 'PicassoLeadGroupType'},
            'group_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'leads.picassoleads': {
            'Meta': {'object_name': 'PicassoLeads'},
            'additional_notes': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'approximate_tat': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'case_categoriser': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'case_categorizer_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'case_notes_for_designer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'case_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'code_1': ('django.db.models.fields.TextField', [], {}),
            'comment_1': ('django.db.models.fields.TextField', [], {}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 11, 24, 0, 0)'}),
            'crop_email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'customer_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'date_of_installation': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'design_completion_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'designer': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'designer_email': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'desktop_score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'email_p': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'estimated_tat': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'gcases_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'gdrive_link': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'google_comment': ('django.db.models.fields.TextField', [], {}),
            'google_rep_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'google_rep_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'googler_cases_alias': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'googler_corporate_email': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_cid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'invision_link': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'invision_password': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'is_build_eligible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language_selector': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'lead_owner_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'lead_owner_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'lead_status': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'link_to_mocks_drive_internal': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'market_selector': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'my_advitiser_email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'my_cases_alias': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'no_of_mocks_delivered': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'picasso_lead_age_days': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'picasso_lead_source': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'picasso_lead_stage': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'picasso_market_served': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'picasso_objective': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'picasso_program_categorization': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'picasso_reference_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'picasso_type': ('django.db.models.fields.CharField', [], {'default': "'PICASSO'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pod_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ref_uuid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'regalix_comment': ('django.db.models.fields.TextField', [], {}),
            'sf_lead_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'speed_score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'standardised_template_link': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tat': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'treatment_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'type_1': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 11, 24, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'url_1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'url_3': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user_experience_score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'leads.regalixteams': {
            'Meta': {'ordering': "['team_name']", 'object_name': 'RegalixTeams', 'db_table': "'regalix_teams'"},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'ldap': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'ldap'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'location': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['leads.Location']", 'symmetrical': 'False'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'process_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'program': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['leads.Team']", 'null': 'True', 'blank': 'True'}),
            'team_lead': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'team_lead'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'team_manager': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'team_manager'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'team_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'leads.sfdcusers': {
            'Meta': {'object_name': 'SfdcUsers', 'db_table': "'sfdc_users'"},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'process_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'shift_end': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'shift_start': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'leads.tagleaddetail': {
            'Meta': {'object_name': 'TagLeadDetail'},
            'Spend_cfc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'action_taken': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'adwords_cid_submitted': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'agency_bundle_number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'agency_email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'agency_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'agency_phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'agency_poc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'agency_service_case_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'alternate_contact_role': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'analytics_account_id_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'analytics_account_id_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'analytics_account_id_3': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'analytics_account_id_4': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'analytics_account_id_5': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'analytics_code_is_setup_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'analytics_code_is_setup_2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'analytics_code_is_setup_3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'analytics_code_is_setup_4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'analytics_code_is_setup_5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'anything_else_we_should_know': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'appointment_sub_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'auth_email_sent': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'campaign_created_by_gsr': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'campaign_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'cart_page_behaviour_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cart_page_behaviour_2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cart_page_behaviour_3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cart_page_behaviour_4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cart_page_behaviour_5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'check_out_process_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'check_out_process_2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'check_out_process_3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'check_out_process_4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'check_out_process_5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'client_web_inventory': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'cms_platform': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'contact_alternate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_call_extension_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_call_extension_2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_call_extension_3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_call_extension_4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_call_extension_5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dead_lead_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dynamic_value': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'dynamic_variable_set': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'feed_upload_method': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'gcase_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'gcss_exception_approved_by': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'gcss_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'gcss_status_approved_by': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implemented_code_is': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'is_backup_taken': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'last_contacted_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'lead_bundle': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'lead_difficulty_level': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'lead_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leads.Leads']"}),
            'list_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'live_transfer': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mc_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mouse_control_approved_by': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mouse_control_taken': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'not_interested_cases_rca': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'number_of_dails': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'on_call_win': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'opt_in_percent': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'other_cms': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'payment_gateway': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pla_sub_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'please_specify_if_others': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'product_behaviour_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'product_behaviour_2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'product_behaviour_3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'product_behaviour_4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'product_behaviour_5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'products_uploaded': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'qc_by': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'qc_comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'qc_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'reason_for_conversion_not_reporting': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'recommended_bid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'recommended_budget': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'recommended_mobile_bid_modifier': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'regalix_sme': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'regalix_webmaster': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'reporting_status_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'reporting_status_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'reporting_status_3': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'reporting_status_4': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'reporting_status_5': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rlsa_auth_approval': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rlsa_tag_team_contacted': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'screenshare_scheduled': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'secured_checkout': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'service_segment': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'shopping_polices_verified': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'shopping_troubleshoot_issue_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sqo_sto_comments': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'tag_via_gtm': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'transaction_behaviour_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transaction_behaviour_2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transaction_behaviour_3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transaction_behaviour_4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transaction_behaviour_5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type_of_policy_violation': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'unethical_win': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'leads.team': {
            'Meta': {'ordering': "['team_name']", 'object_name': 'Team', 'db_table': "'teams'"},
            'belongs_to': ('django.db.models.fields.CharField', [], {'default': "'TAG'", 'max_length': '50'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'picasso_lead_group_type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['leads.PicassoLeadGroupType']", 'null': 'True', 'blank': 'True'}),
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
        u'leads.timezonemapping': {
            'Meta': {'ordering': "['standard_timezone']", 'unique_together': "(('standard_timezone', 'daylight_timezone'),)", 'object_name': 'TimezoneMapping', 'db_table': "'timezone_mapping'"},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'daylight_timezone': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ds_timezone'", 'unique': 'True', 'to': u"orm['leads.Timezone']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'standard_timezone': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'std_timezone'", 'unique': 'True', 'to': u"orm['leads.Timezone']"})
        },
        u'leads.treatmenttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'TreatmentType', 'db_table': "'treatment_type'"},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'leads.whitelistedauditcid': {
            'Meta': {'object_name': 'WhiteListedAuditCID'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 11, 24, 0, 0)'}),
            'external_customer_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 11, 24, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'opportunity_type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'leads.wppleads': {
            'Meta': {'object_name': 'WPPLeads'},
            'actual_deployment_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'actual_mock_review_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'actual_stage_review_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'actual_ui_ux_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'additional_notes': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'additional_notes_if_any': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'advertiser_email_3': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'advertiser_location': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'advertiser_role': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'advertiser_telephone_3': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'advertisers_e_mail_wpp': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'adwords_account_status': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'appointment_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'appointment_time_in_ist': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
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
            'conversion_goal': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 11, 24, 0, 0)'}),
            'customer_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'date_of_installation': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'dead_lead_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'delivery_pod': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'design_effort': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'design_owner': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'dev_owner': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'development_effort': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dials': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ecommerce': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'email_logs': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'email_mandatory': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'email_optional': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'emails_received': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'emails_sent': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'engagement_effort': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'first_contacted_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'first_name_3': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'first_name_optional': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'google_account_manager': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'google_comment': ('django.db.models.fields.TextField', [], {}),
            'google_rep_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'google_rep_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invision_links': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'is_ab_test': ('django.db.models.fields.CharField', [], {'default': "'YES'", 'max_length': '255', 'null': 'True'}),
            'is_active': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'is_build_eligible': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'is_nominated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'last_name_3': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'last_name_optional': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'lead_owner_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'lead_owner_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'lead_source': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'lead_source_c': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'lead_status': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'lead_sub_status': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'lead_via_live_transfer': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'mockup_password': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'mockup_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'no_of_calls_inbound': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'no_of_calls_outbound': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'no_of_pages': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone_optional': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'planned_deployment_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'planned_stage_review_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'qa_owner': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'ref_uuid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'regalix_comment': ('django.db.models.fields.TextField', [], {}),
            'reschedule_email_schedule_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'rescheduled_appointment': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'rescheduled_appointment_in_ist': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'role_2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'role_3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'role_others': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'role_others1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'role_others2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'screenshare_scheduled': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'sf_lead_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'stage_password': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'stage_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'tat': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'technology': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'testing_effort': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'time_zone': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'tracking_codes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'treatment_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'type_1': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'type_2': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'type_3': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'type_4': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'type_5': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 11, 24, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'url_1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_2': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_3': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_4': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_5': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'why_deferred': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['leads']