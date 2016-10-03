# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Help'
        db.delete_table(u'main_help')

        # Adding model 'PortalUsers'
        db.create_table('portal_users', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal(u'main', ['PortalUsers'])

        # Adding M2M table for field managers on 'PortalUsers'
        m2m_table_name = db.shorten_name('portal_users_managers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_portalusers', models.ForeignKey(orm[u'main.portalusers'], null=False)),
            ('to_portalusers', models.ForeignKey(orm[u'main.portalusers'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_portalusers_id', 'to_portalusers_id'])

        # Adding model 'FeedbackComment'
        db.create_table('feedback_comments', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feedback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Feedback'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1500)),
            ('comment_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['FeedbackComment'])

        # Adding model 'Feedback'
        db.create_table('feedback', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='feedback_by', to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('cid', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('advertiser_name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['leads.Location'])),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('feedback_type', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('status', self.gf('django.db.models.fields.CharField')(default='NEW', max_length=20)),
            ('lead_owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lead_owner', to=orm['main.PortalUsers'])),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('resolved_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='resolved_by', null=True, to=orm['auth.User'])),
            ('resolved_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Feedback'])


    def backwards(self, orm):
        # Adding model 'Help'
        db.create_table(u'main_help', (
            ('issue_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('issue_cid', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('issue_faced', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('issue_noc', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issue_desc', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'main', ['Help'])

        # Deleting model 'PortalUsers'
        db.delete_table('portal_users')

        # Removing M2M table for field managers on 'PortalUsers'
        db.delete_table(db.shorten_name('portal_users_managers'))

        # Deleting model 'FeedbackComment'
        db.delete_table('feedback_comments')

        # Deleting model 'Feedback'
        db.delete_table('feedback')


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
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
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
        u'leads.location': {
            'Meta': {'ordering': "['location_name']", 'object_name': 'Location', 'db_table': "'locations'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'time_zone': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['leads.Timezone']", 'symmetrical': 'False'})
        },
        u'leads.timezone': {
            'Meta': {'ordering': "['zone_name']", 'object_name': 'Timezone', 'db_table': "'timezone'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_value': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'zone_name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'main.feedback': {
            'Meta': {'object_name': 'Feedback', 'db_table': "'feedback'"},
            'advertiser_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'feedback_type': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'lead_owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lead_owner'", 'to': u"orm['main.PortalUsers']"}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leads.Location']"}),
            'resolved_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'resolved_by'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'resolved_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'NEW'", 'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'feedback_by'", 'to': u"orm['auth.User']"})
        },
        u'main.feedbackcomment': {
            'Meta': {'ordering': "['-created_date']", 'object_name': 'FeedbackComment', 'db_table': "'feedback_comments'"},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1500'}),
            'comment_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Feedback']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'main.portalusers': {
            'Meta': {'object_name': 'PortalUsers', 'db_table': "'portal_users'"},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'managers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['main.PortalUsers']", 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        u'main.userdetails': {
            'Meta': {'object_name': 'UserDetails'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'user_manager_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_manager_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user_supporting_region': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['main']