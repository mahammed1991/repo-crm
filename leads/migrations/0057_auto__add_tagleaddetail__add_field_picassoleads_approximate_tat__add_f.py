# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TagLeadDetail'
        db.create_table(u'leads_tagleaddetail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lead_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['leads.Leads'])),
            ('qc_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('qc_by', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('qc_comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('auth_email_sent', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('live_transfer', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('cms_platform', self.gf('django.db.models.fields.CharField')(default='', max_length=80, null=True, blank=True)),
            ('appointment_sub_status', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('gcase_id', self.gf('django.db.models.fields.CharField')(default='', max_length=80, null=True, blank=True)),
            ('gcss_status', self.gf('django.db.models.fields.CharField')(default='', max_length=80, null=True, blank=True)),
            ('gcss_status_approved_by', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('mouse_control_taken', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('mouse_control_approved_by', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('list_type', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('regalix_sme', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('lead_difficulty_level', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('rlsa_tag_team_contacted', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('campaign_created_by_gsr', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('adwords_cid_submitted', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('implemented_code_is', self.gf('django.db.models.fields.CharField')(default='', max_length=80, null=True, blank=True)),
            ('number_of_dails', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pla_sub_status', self.gf('django.db.models.fields.CharField')(default='', max_length=80, null=True, blank=True)),
            ('dynamic_variable_set', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('last_contacted_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('dead_lead_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_backup_taken', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('tag_via_gtm', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('service_segment', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('rlsa_auth_approval', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('agency_poc', self.gf('django.db.models.fields.CharField')(default='', max_length=80, null=True, blank=True)),
            ('agency_name', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('agency_phone', self.gf('django.db.models.fields.CharField')(default='', max_length=80, null=True, blank=True)),
            ('agency_email', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('agency_bundle_number', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('agency_service_case_id', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('mc_id', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('opt_in_percent', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('client_web_inventory', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('recommended_budget', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('sqo_sto_comments', self.gf('django.db.models.fields.CharField')(default='', max_length=1000, null=True, blank=True)),
            ('secured_checkout', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('payment_gateway', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('recommended_mobile_bid_modifier', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('shopping_polices_verified', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('type_of_policy_violation', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('shopping_troubleshoot_issue_type', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('products_uploaded', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('campaign_id', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('feed_upload_method', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('recommended_bid', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'leads', ['TagLeadDetail'])

        # Adding field 'PicassoLeads.approximate_tat'
        db.add_column(u'leads_picassoleads', 'approximate_tat',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.email'
        db.add_column(u'leads_picassoleads', 'email',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.case_categoriser'
        db.add_column(u'leads_picassoleads', 'case_categoriser',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.case_categorizer_notes'
        db.add_column(u'leads_picassoleads', 'case_categorizer_notes',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.case_notes_for_designer'
        db.add_column(u'leads_picassoleads', 'case_notes_for_designer',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.case_type'
        db.add_column(u'leads_picassoleads', 'case_type',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.design_completion_date'
        db.add_column(u'leads_picassoleads', 'design_completion_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.designer'
        db.add_column(u'leads_picassoleads', 'designer',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.designer_email'
        db.add_column(u'leads_picassoleads', 'designer_email',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.desktop_score'
        db.add_column(u'leads_picassoleads', 'desktop_score',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.gcases_id'
        db.add_column(u'leads_picassoleads', 'gcases_id',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.gdrive_link'
        db.add_column(u'leads_picassoleads', 'gdrive_link',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.googler_cases_alias'
        db.add_column(u'leads_picassoleads', 'googler_cases_alias',
                      self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.googler_corporate_email'
        db.add_column(u'leads_picassoleads', 'googler_corporate_email',
                      self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.invision_link'
        db.add_column(u'leads_picassoleads', 'invision_link',
                      self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.invision_password'
        db.add_column(u'leads_picassoleads', 'invision_password',
                      self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.link_to_mocks_drive_internal'
        db.add_column(u'leads_picassoleads', 'link_to_mocks_drive_internal',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.no_of_mocks_delivered'
        db.add_column(u'leads_picassoleads', 'no_of_mocks_delivered',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.picasso_lead_age_days'
        db.add_column(u'leads_picassoleads', 'picasso_lead_age_days',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.picasso_lead_source'
        db.add_column(u'leads_picassoleads', 'picasso_lead_source',
                      self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.picasso_lead_stage'
        db.add_column(u'leads_picassoleads', 'picasso_lead_stage',
                      self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.picasso_market_served'
        db.add_column(u'leads_picassoleads', 'picasso_market_served',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.picasso_program_categorization'
        db.add_column(u'leads_picassoleads', 'picasso_program_categorization',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.picasso_reference_id'
        db.add_column(u'leads_picassoleads', 'picasso_reference_id',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.email_p'
        db.add_column(u'leads_picassoleads', 'email_p',
                      self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.speed_score'
        db.add_column(u'leads_picassoleads', 'speed_score',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.standardised_template_link'
        db.add_column(u'leads_picassoleads', 'standardised_template_link',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.url_2'
        db.add_column(u'leads_picassoleads', 'url_2',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.url_3'
        db.add_column(u'leads_picassoleads', 'url_3',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PicassoLeads.user_experience_score'
        db.add_column(u'leads_picassoleads', 'user_experience_score',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.actual_deployment_date'
        db.add_column(u'leads_wppleads', 'actual_deployment_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.actual_mock_review_date'
        db.add_column(u'leads_wppleads', 'actual_mock_review_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.actual_stage_review_date'
        db.add_column(u'leads_wppleads', 'actual_stage_review_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.actual_ui_ux_date'
        db.add_column(u'leads_wppleads', 'actual_ui_ux_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.additional_notes_if_any'
        db.add_column(u'leads_wppleads', 'additional_notes_if_any',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.advertiser_email_3'
        db.add_column(u'leads_wppleads', 'advertiser_email_3',
                      self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.advertiser_role'
        db.add_column(u'leads_wppleads', 'advertiser_role',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.advertisers_e_mail_wpp'
        db.add_column(u'leads_wppleads', 'advertisers_e_mail_wpp',
                      self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.advertiser_telephone_3'
        db.add_column(u'leads_wppleads', 'advertiser_telephone_3',
                      self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.adwords_account_status'
        db.add_column(u'leads_wppleads', 'adwords_account_status',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.conversion_goal'
        db.add_column(u'leads_wppleads', 'conversion_goal',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.dead_lead_date'
        db.add_column(u'leads_wppleads', 'dead_lead_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.delivery_pod'
        db.add_column(u'leads_wppleads', 'delivery_pod',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.design_effort'
        db.add_column(u'leads_wppleads', 'design_effort',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.design_owner'
        db.add_column(u'leads_wppleads', 'design_owner',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.dev_owner'
        db.add_column(u'leads_wppleads', 'dev_owner',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.development_effort'
        db.add_column(u'leads_wppleads', 'development_effort',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.email_mandatory'
        db.add_column(u'leads_wppleads', 'email_mandatory',
                      self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.engagement_effort'
        db.add_column(u'leads_wppleads', 'engagement_effort',
                      self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.first_name_3'
        db.add_column(u'leads_wppleads', 'first_name_3',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.google_account_manager'
        db.add_column(u'leads_wppleads', 'google_account_manager',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.invision_links'
        db.add_column(u'leads_wppleads', 'invision_links',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.appointment_time_in_ist'
        db.add_column(u'leads_wppleads', 'appointment_time_in_ist',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.last_name_3'
        db.add_column(u'leads_wppleads', 'last_name_3',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.lead_source_c'
        db.add_column(u'leads_wppleads', 'lead_source_c',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.lead_via_live_transfer'
        db.add_column(u'leads_wppleads', 'lead_via_live_transfer',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.lead_source'
        db.add_column(u'leads_wppleads', 'lead_source',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.advertiser_location'
        db.add_column(u'leads_wppleads', 'advertiser_location',
                      self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.no_of_pages'
        db.add_column(u'leads_wppleads', 'no_of_pages',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.planned_deployment_date'
        db.add_column(u'leads_wppleads', 'planned_deployment_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.planned_stage_review_date'
        db.add_column(u'leads_wppleads', 'planned_stage_review_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.priority'
        db.add_column(u'leads_wppleads', 'priority',
                      self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.qa_owner'
        db.add_column(u'leads_wppleads', 'qa_owner',
                      self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.reschedule_email_schedule_time'
        db.add_column(u'leads_wppleads', 'reschedule_email_schedule_time',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.role_2'
        db.add_column(u'leads_wppleads', 'role_2',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.role_3'
        db.add_column(u'leads_wppleads', 'role_3',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.role_others1'
        db.add_column(u'leads_wppleads', 'role_others1',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.role_others2'
        db.add_column(u'leads_wppleads', 'role_others2',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.role_others'
        db.add_column(u'leads_wppleads', 'role_others',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.technology'
        db.add_column(u'leads_wppleads', 'technology',
                      self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.testing_effort'
        db.add_column(u'leads_wppleads', 'testing_effort',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.tracking_codes'
        db.add_column(u'leads_wppleads', 'tracking_codes',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.screenshare_scheduled'
        db.add_column(u'leads_wppleads', 'screenshare_scheduled',
                      self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WPPLeads.why_deferred'
        db.add_column(u'leads_wppleads', 'why_deferred',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Leads.wpp_treatment_type'
        db.delete_column(u'leads_leads', 'wpp_treatment_type')

        # Adding field 'Leads.google_rep_location'
        db.add_column(u'leads_leads', 'google_rep_location',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.google_rep_manager_email'
        db.add_column(u'leads_leads', 'google_rep_manager_email',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.google_rep_manager_name'
        db.add_column(u'leads_leads', 'google_rep_manager_name',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.primary_contact_role'
        db.add_column(u'leads_leads', 'primary_contact_role',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.webmaster_phone'
        db.add_column(u'leads_leads', 'webmaster_phone',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.webmaster_name'
        db.add_column(u'leads_leads', 'webmaster_name',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.webmaster_email'
        db.add_column(u'leads_leads', 'webmaster_email',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.user_list_id_1'
        db.add_column(u'leads_leads', 'user_list_id_1',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.rlsa_bid_adjustment_1'
        db.add_column(u'leads_leads', 'rlsa_bid_adjustment_1',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.internale_cid_1'
        db.add_column(u'leads_leads', 'internale_cid_1',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.override_existing_bid_modifiers_1'
        db.add_column(u'leads_leads', 'override_existing_bid_modifiers_1',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.campaign_id_1'
        db.add_column(u'leads_leads', 'campaign_id_1',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.user_list_id_2'
        db.add_column(u'leads_leads', 'user_list_id_2',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.rlsa_bid_adjustment_2'
        db.add_column(u'leads_leads', 'rlsa_bid_adjustment_2',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.internale_cid_2'
        db.add_column(u'leads_leads', 'internale_cid_2',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.override_existing_bid_modifiers_2'
        db.add_column(u'leads_leads', 'override_existing_bid_modifiers_2',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.campaign_id_2'
        db.add_column(u'leads_leads', 'campaign_id_2',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.user_list_id_3'
        db.add_column(u'leads_leads', 'user_list_id_3',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.rlsa_bid_adjustment_3'
        db.add_column(u'leads_leads', 'rlsa_bid_adjustment_3',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.internale_cid_3'
        db.add_column(u'leads_leads', 'internale_cid_3',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.override_existing_bid_modifiers_3'
        db.add_column(u'leads_leads', 'override_existing_bid_modifiers_3',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.campaign_id_3'
        db.add_column(u'leads_leads', 'campaign_id_3',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.user_list_id_4'
        db.add_column(u'leads_leads', 'user_list_id_4',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.rlsa_bid_adjustment_4'
        db.add_column(u'leads_leads', 'rlsa_bid_adjustment_4',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.internale_cid_4'
        db.add_column(u'leads_leads', 'internale_cid_4',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.override_existing_bid_modifiers_4'
        db.add_column(u'leads_leads', 'override_existing_bid_modifiers_4',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.campaign_id_4'
        db.add_column(u'leads_leads', 'campaign_id_4',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.user_list_id_5'
        db.add_column(u'leads_leads', 'user_list_id_5',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.rlsa_bid_adjustment_5'
        db.add_column(u'leads_leads', 'rlsa_bid_adjustment_5',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.internale_cid_5'
        db.add_column(u'leads_leads', 'internale_cid_5',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.override_existing_bid_modifiers_5'
        db.add_column(u'leads_leads', 'override_existing_bid_modifiers_5',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.campaign_id_5'
        db.add_column(u'leads_leads', 'campaign_id_5',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Leads.additional_support_beyond_case'
        db.add_column(u'leads_leads', 'additional_support_beyond_case',
                      self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Leads.additional_description'
        db.alter_column(u'leads_leads', 'additional_description', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True))

        # Changing field 'Leads.area_tobe_improved'
        db.alter_column(u'leads_leads', 'area_tobe_improved', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True))
        # Adding field 'SfdcUsers.process_type'
        db.add_column('sfdc_users', 'process_type',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Adding field 'SfdcUsers.shift_start'
        db.add_column('sfdc_users', 'shift_start',
                      self.gf('django.db.models.fields.TimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SfdcUsers.shift_end'
        db.add_column('sfdc_users', 'shift_end',
                      self.gf('django.db.models.fields.TimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SfdcUsers.location'
        db.add_column('sfdc_users', 'location',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'TagLeadDetail'
        db.delete_table(u'leads_tagleaddetail')

        # Deleting field 'PicassoLeads.approximate_tat'
        db.delete_column(u'leads_picassoleads', 'approximate_tat')

        # Deleting field 'PicassoLeads.email'
        db.delete_column(u'leads_picassoleads', 'email')

        # Deleting field 'PicassoLeads.case_categoriser'
        db.delete_column(u'leads_picassoleads', 'case_categoriser')

        # Deleting field 'PicassoLeads.case_categorizer_notes'
        db.delete_column(u'leads_picassoleads', 'case_categorizer_notes')

        # Deleting field 'PicassoLeads.case_notes_for_designer'
        db.delete_column(u'leads_picassoleads', 'case_notes_for_designer')

        # Deleting field 'PicassoLeads.case_type'
        db.delete_column(u'leads_picassoleads', 'case_type')

        # Deleting field 'PicassoLeads.design_completion_date'
        db.delete_column(u'leads_picassoleads', 'design_completion_date')

        # Deleting field 'PicassoLeads.designer'
        db.delete_column(u'leads_picassoleads', 'designer')

        # Deleting field 'PicassoLeads.designer_email'
        db.delete_column(u'leads_picassoleads', 'designer_email')

        # Deleting field 'PicassoLeads.desktop_score'
        db.delete_column(u'leads_picassoleads', 'desktop_score')

        # Deleting field 'PicassoLeads.gcases_id'
        db.delete_column(u'leads_picassoleads', 'gcases_id')

        # Deleting field 'PicassoLeads.gdrive_link'
        db.delete_column(u'leads_picassoleads', 'gdrive_link')

        # Deleting field 'PicassoLeads.googler_cases_alias'
        db.delete_column(u'leads_picassoleads', 'googler_cases_alias')

        # Deleting field 'PicassoLeads.googler_corporate_email'
        db.delete_column(u'leads_picassoleads', 'googler_corporate_email')

        # Deleting field 'PicassoLeads.invision_link'
        db.delete_column(u'leads_picassoleads', 'invision_link')

        # Deleting field 'PicassoLeads.invision_password'
        db.delete_column(u'leads_picassoleads', 'invision_password')

        # Deleting field 'PicassoLeads.link_to_mocks_drive_internal'
        db.delete_column(u'leads_picassoleads', 'link_to_mocks_drive_internal')

        # Deleting field 'PicassoLeads.no_of_mocks_delivered'
        db.delete_column(u'leads_picassoleads', 'no_of_mocks_delivered')

        # Deleting field 'PicassoLeads.picasso_lead_age_days'
        db.delete_column(u'leads_picassoleads', 'picasso_lead_age_days')

        # Deleting field 'PicassoLeads.picasso_lead_source'
        db.delete_column(u'leads_picassoleads', 'picasso_lead_source')

        # Deleting field 'PicassoLeads.picasso_lead_stage'
        db.delete_column(u'leads_picassoleads', 'picasso_lead_stage')

        # Deleting field 'PicassoLeads.picasso_market_served'
        db.delete_column(u'leads_picassoleads', 'picasso_market_served')

        # Deleting field 'PicassoLeads.picasso_program_categorization'
        db.delete_column(u'leads_picassoleads', 'picasso_program_categorization')

        # Deleting field 'PicassoLeads.picasso_reference_id'
        db.delete_column(u'leads_picassoleads', 'picasso_reference_id')

        # Deleting field 'PicassoLeads.email_p'
        db.delete_column(u'leads_picassoleads', 'email_p')

        # Deleting field 'PicassoLeads.speed_score'
        db.delete_column(u'leads_picassoleads', 'speed_score')

        # Deleting field 'PicassoLeads.standardised_template_link'
        db.delete_column(u'leads_picassoleads', 'standardised_template_link')

        # Deleting field 'PicassoLeads.url_2'
        db.delete_column(u'leads_picassoleads', 'url_2')

        # Deleting field 'PicassoLeads.url_3'
        db.delete_column(u'leads_picassoleads', 'url_3')

        # Deleting field 'PicassoLeads.user_experience_score'
        db.delete_column(u'leads_picassoleads', 'user_experience_score')

        # Deleting field 'WPPLeads.actual_deployment_date'
        db.delete_column(u'leads_wppleads', 'actual_deployment_date')

        # Deleting field 'WPPLeads.actual_mock_review_date'
        db.delete_column(u'leads_wppleads', 'actual_mock_review_date')

        # Deleting field 'WPPLeads.actual_stage_review_date'
        db.delete_column(u'leads_wppleads', 'actual_stage_review_date')

        # Deleting field 'WPPLeads.actual_ui_ux_date'
        db.delete_column(u'leads_wppleads', 'actual_ui_ux_date')

        # Deleting field 'WPPLeads.additional_notes_if_any'
        db.delete_column(u'leads_wppleads', 'additional_notes_if_any')

        # Deleting field 'WPPLeads.advertiser_email_3'
        db.delete_column(u'leads_wppleads', 'advertiser_email_3')

        # Deleting field 'WPPLeads.advertiser_role'
        db.delete_column(u'leads_wppleads', 'advertiser_role')

        # Deleting field 'WPPLeads.advertisers_e_mail_wpp'
        db.delete_column(u'leads_wppleads', 'advertisers_e_mail_wpp')

        # Deleting field 'WPPLeads.advertiser_telephone_3'
        db.delete_column(u'leads_wppleads', 'advertiser_telephone_3')

        # Deleting field 'WPPLeads.adwords_account_status'
        db.delete_column(u'leads_wppleads', 'adwords_account_status')

        # Deleting field 'WPPLeads.conversion_goal'
        db.delete_column(u'leads_wppleads', 'conversion_goal')

        # Deleting field 'WPPLeads.dead_lead_date'
        db.delete_column(u'leads_wppleads', 'dead_lead_date')

        # Deleting field 'WPPLeads.delivery_pod'
        db.delete_column(u'leads_wppleads', 'delivery_pod')

        # Deleting field 'WPPLeads.design_effort'
        db.delete_column(u'leads_wppleads', 'design_effort')

        # Deleting field 'WPPLeads.design_owner'
        db.delete_column(u'leads_wppleads', 'design_owner')

        # Deleting field 'WPPLeads.dev_owner'
        db.delete_column(u'leads_wppleads', 'dev_owner')

        # Deleting field 'WPPLeads.development_effort'
        db.delete_column(u'leads_wppleads', 'development_effort')

        # Deleting field 'WPPLeads.email_mandatory'
        db.delete_column(u'leads_wppleads', 'email_mandatory')

        # Deleting field 'WPPLeads.engagement_effort'
        db.delete_column(u'leads_wppleads', 'engagement_effort')

        # Deleting field 'WPPLeads.first_name_3'
        db.delete_column(u'leads_wppleads', 'first_name_3')

        # Deleting field 'WPPLeads.google_account_manager'
        db.delete_column(u'leads_wppleads', 'google_account_manager')

        # Deleting field 'WPPLeads.invision_links'
        db.delete_column(u'leads_wppleads', 'invision_links')

        # Deleting field 'WPPLeads.appointment_time_in_ist'
        db.delete_column(u'leads_wppleads', 'appointment_time_in_ist')

        # Deleting field 'WPPLeads.last_name_3'
        db.delete_column(u'leads_wppleads', 'last_name_3')

        # Deleting field 'WPPLeads.lead_source_c'
        db.delete_column(u'leads_wppleads', 'lead_source_c')

        # Deleting field 'WPPLeads.lead_via_live_transfer'
        db.delete_column(u'leads_wppleads', 'lead_via_live_transfer')

        # Deleting field 'WPPLeads.lead_source'
        db.delete_column(u'leads_wppleads', 'lead_source')

        # Deleting field 'WPPLeads.advertiser_location'
        db.delete_column(u'leads_wppleads', 'advertiser_location')

        # Deleting field 'WPPLeads.no_of_pages'
        db.delete_column(u'leads_wppleads', 'no_of_pages')

        # Deleting field 'WPPLeads.planned_deployment_date'
        db.delete_column(u'leads_wppleads', 'planned_deployment_date')

        # Deleting field 'WPPLeads.planned_stage_review_date'
        db.delete_column(u'leads_wppleads', 'planned_stage_review_date')

        # Deleting field 'WPPLeads.priority'
        db.delete_column(u'leads_wppleads', 'priority')

        # Deleting field 'WPPLeads.qa_owner'
        db.delete_column(u'leads_wppleads', 'qa_owner')

        # Deleting field 'WPPLeads.reschedule_email_schedule_time'
        db.delete_column(u'leads_wppleads', 'reschedule_email_schedule_time')

        # Deleting field 'WPPLeads.role_2'
        db.delete_column(u'leads_wppleads', 'role_2')

        # Deleting field 'WPPLeads.role_3'
        db.delete_column(u'leads_wppleads', 'role_3')

        # Deleting field 'WPPLeads.role_others1'
        db.delete_column(u'leads_wppleads', 'role_others1')

        # Deleting field 'WPPLeads.role_others2'
        db.delete_column(u'leads_wppleads', 'role_others2')

        # Deleting field 'WPPLeads.role_others'
        db.delete_column(u'leads_wppleads', 'role_others')

        # Deleting field 'WPPLeads.technology'
        db.delete_column(u'leads_wppleads', 'technology')

        # Deleting field 'WPPLeads.testing_effort'
        db.delete_column(u'leads_wppleads', 'testing_effort')

        # Deleting field 'WPPLeads.tracking_codes'
        db.delete_column(u'leads_wppleads', 'tracking_codes')

        # Deleting field 'WPPLeads.screenshare_scheduled'
        db.delete_column(u'leads_wppleads', 'screenshare_scheduled')

        # Deleting field 'WPPLeads.why_deferred'
        db.delete_column(u'leads_wppleads', 'why_deferred')

        # Adding field 'Leads.wpp_treatment_type'
        db.add_column(u'leads_leads', 'wpp_treatment_type',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Leads.google_rep_location'
        db.delete_column(u'leads_leads', 'google_rep_location')

        # Deleting field 'Leads.google_rep_manager_email'
        db.delete_column(u'leads_leads', 'google_rep_manager_email')

        # Deleting field 'Leads.google_rep_manager_name'
        db.delete_column(u'leads_leads', 'google_rep_manager_name')

        # Deleting field 'Leads.primary_contact_role'
        db.delete_column(u'leads_leads', 'primary_contact_role')

        # Deleting field 'Leads.webmaster_phone'
        db.delete_column(u'leads_leads', 'webmaster_phone')

        # Deleting field 'Leads.webmaster_name'
        db.delete_column(u'leads_leads', 'webmaster_name')

        # Deleting field 'Leads.webmaster_email'
        db.delete_column(u'leads_leads', 'webmaster_email')

        # Deleting field 'Leads.user_list_id_1'
        db.delete_column(u'leads_leads', 'user_list_id_1')

        # Deleting field 'Leads.rlsa_bid_adjustment_1'
        db.delete_column(u'leads_leads', 'rlsa_bid_adjustment_1')

        # Deleting field 'Leads.internale_cid_1'
        db.delete_column(u'leads_leads', 'internale_cid_1')

        # Deleting field 'Leads.override_existing_bid_modifiers_1'
        db.delete_column(u'leads_leads', 'override_existing_bid_modifiers_1')

        # Deleting field 'Leads.campaign_id_1'
        db.delete_column(u'leads_leads', 'campaign_id_1')

        # Deleting field 'Leads.user_list_id_2'
        db.delete_column(u'leads_leads', 'user_list_id_2')

        # Deleting field 'Leads.rlsa_bid_adjustment_2'
        db.delete_column(u'leads_leads', 'rlsa_bid_adjustment_2')

        # Deleting field 'Leads.internale_cid_2'
        db.delete_column(u'leads_leads', 'internale_cid_2')

        # Deleting field 'Leads.override_existing_bid_modifiers_2'
        db.delete_column(u'leads_leads', 'override_existing_bid_modifiers_2')

        # Deleting field 'Leads.campaign_id_2'
        db.delete_column(u'leads_leads', 'campaign_id_2')

        # Deleting field 'Leads.user_list_id_3'
        db.delete_column(u'leads_leads', 'user_list_id_3')

        # Deleting field 'Leads.rlsa_bid_adjustment_3'
        db.delete_column(u'leads_leads', 'rlsa_bid_adjustment_3')

        # Deleting field 'Leads.internale_cid_3'
        db.delete_column(u'leads_leads', 'internale_cid_3')

        # Deleting field 'Leads.override_existing_bid_modifiers_3'
        db.delete_column(u'leads_leads', 'override_existing_bid_modifiers_3')

        # Deleting field 'Leads.campaign_id_3'
        db.delete_column(u'leads_leads', 'campaign_id_3')

        # Deleting field 'Leads.user_list_id_4'
        db.delete_column(u'leads_leads', 'user_list_id_4')

        # Deleting field 'Leads.rlsa_bid_adjustment_4'
        db.delete_column(u'leads_leads', 'rlsa_bid_adjustment_4')

        # Deleting field 'Leads.internale_cid_4'
        db.delete_column(u'leads_leads', 'internale_cid_4')

        # Deleting field 'Leads.override_existing_bid_modifiers_4'
        db.delete_column(u'leads_leads', 'override_existing_bid_modifiers_4')

        # Deleting field 'Leads.campaign_id_4'
        db.delete_column(u'leads_leads', 'campaign_id_4')

        # Deleting field 'Leads.user_list_id_5'
        db.delete_column(u'leads_leads', 'user_list_id_5')

        # Deleting field 'Leads.rlsa_bid_adjustment_5'
        db.delete_column(u'leads_leads', 'rlsa_bid_adjustment_5')

        # Deleting field 'Leads.internale_cid_5'
        db.delete_column(u'leads_leads', 'internale_cid_5')

        # Deleting field 'Leads.override_existing_bid_modifiers_5'
        db.delete_column(u'leads_leads', 'override_existing_bid_modifiers_5')

        # Deleting field 'Leads.campaign_id_5'
        db.delete_column(u'leads_leads', 'campaign_id_5')

        # Deleting field 'Leads.additional_support_beyond_case'
        db.delete_column(u'leads_leads', 'additional_support_beyond_case')


        # Changing field 'Leads.additional_description'
        db.alter_column(u'leads_leads', 'additional_description', self.gf('django.db.models.fields.CharField')(max_length=3000, null=True))

        # Changing field 'Leads.area_tobe_improved'
        db.alter_column(u'leads_leads', 'area_tobe_improved', self.gf('django.db.models.fields.CharField')(max_length=3000, null=True))
        # Deleting field 'SfdcUsers.process_type'
        db.delete_column('sfdc_users', 'process_type')

        # Deleting field 'SfdcUsers.shift_start'
        db.delete_column('sfdc_users', 'shift_start')

        # Deleting field 'SfdcUsers.shift_end'
        db.delete_column('sfdc_users', 'shift_end')

        # Deleting field 'SfdcUsers.location'
        db.delete_column('sfdc_users', 'location')


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
            'appointment_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 10, 25, 0, 0)'}),
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
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 10, 25, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'modified_by_user'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 10, 25, 0, 0)', 'auto_now': 'True', 'blank': 'True'})
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
        u'leads.leads': {
            'Meta': {'object_name': 'Leads'},
            'additional_description': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'additional_support_beyond_case': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'appointment_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'appointment_date_in_ist': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
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
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 10, 25, 0, 0)'}),
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
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 10, 25, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
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
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 10, 25, 0, 0)'}),
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
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 10, 25, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
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
            'adwords_cid_submitted': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'agency_bundle_number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'agency_email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'agency_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'agency_phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'agency_poc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'agency_service_case_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'appointment_sub_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'auth_email_sent': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'campaign_created_by_gsr': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'campaign_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'client_web_inventory': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'cms_platform': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'dead_lead_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dynamic_variable_set': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'feed_upload_method': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'gcase_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'gcss_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'gcss_status_approved_by': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implemented_code_is': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'is_backup_taken': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'last_contacted_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'lead_difficulty_level': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'lead_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leads.Leads']"}),
            'list_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'live_transfer': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'mc_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mouse_control_approved_by': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mouse_control_taken': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'number_of_dails': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'opt_in_percent': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'payment_gateway': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pla_sub_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'products_uploaded': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'qc_by': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'qc_comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'qc_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'recommended_bid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'recommended_budget': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'recommended_mobile_bid_modifier': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'regalix_sme': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rlsa_auth_approval': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rlsa_tag_team_contacted': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'secured_checkout': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'service_segment': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'shopping_polices_verified': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'shopping_troubleshoot_issue_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sqo_sto_comments': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'tag_via_gtm': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'type_of_policy_violation': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'})
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
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 10, 25, 0, 0)'}),
            'external_customer_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 10, 25, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
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
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 10, 25, 0, 0)'}),
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
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 10, 25, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'url_1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_2': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_3': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_4': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_5': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'why_deferred': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['leads']