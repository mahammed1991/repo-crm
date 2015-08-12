# -*- coding: utf-8 -*-
import csv

from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.conf import settings


class Migration(SchemaMigration):

    current_dir = settings.BASE_DIR + '/leads/migrations/'

    def forwards(self, orm):
        db.execute('INSERT INTO regalix_teams (id, team_name) values (1, %s)', ['default team'])

        # Add timezone data from csv file
        csvfile = open(Migration.current_dir + 'timezones.csv', 'rb')
        zone_reader = csv.DictReader(csvfile, ('zone_name', 'time_value'))

        for tz in zone_reader:
            db.execute('INSERT INTO timezone (zone_name, time_value) values (%s, %s)', [tz['zone_name'], tz['time_value']])

        csvfile.close()

        # Add Locations data from csv file
        loc_csvfile = open(Migration.current_dir + 'locations.csv', 'rb')
        loc_reader = csv.DictReader(loc_csvfile, ('location_name',))

        for loc in loc_reader:
            db.execute('INSERT INTO locations (location_name) values (%s)', [loc['location_name']])

        loc_csvfile.close()

    def backwards(self, orm):
        db.execute("DELETE FROM regalix_teams WHERE ID=1")

        # Remove timezone data in csv file
        csvfile = open(Migration.current_dir + 'timezones.csv', 'rb')
        zone_reader = csv.DictReader(csvfile, ('zone_name', 'time_value'))

        for tz in zone_reader:
            db.execute('DELETE FROM timezone WHERE zone_name=%s and time_value=%s', [tz['zone_name'], tz['time_value']])

        csvfile.close()

        # Remove Locations data in csv file
        loc_csvfile = open(Migration.current_dir + 'locations.csv', 'rb')
        loc_reader = csv.DictReader(loc_csvfile, ('location_name',))

        for loc in loc_reader:
            db.execute('DELETE FROM locations WHERE location_name=%s', [loc['location_name']])

        loc_csvfile.close()

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
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 18, 0, 0)'}),
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
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 18, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'url_1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_2': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_3': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_4': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_5': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'leads.location': {
            'Meta': {'ordering': "['location_name']", 'object_name': 'Location', 'db_table': "'locations'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'time_zone': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['leads.Timezone']", 'symmetrical': 'False'})
        },
        u'leads.regalixteams': {
            'Meta': {'ordering': "['team_name']", 'object_name': 'RegalixTeams', 'db_table': "'regalix_teams'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['leads.Location']", 'symmetrical': 'False'}),
            'team_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'leads.timezone': {
            'Meta': {'ordering': "['zone_name']", 'object_name': 'Timezone', 'db_table': "'timezone'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_value': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'zone_name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['leads']