
class SalesforceLeads(object):

    SANDBOX_BASIC_LEADS_ARGS = {'first_name': 'first_name',
                                'last_name': 'last_name',
                                'gref': '00Nd0000005WYgk',  # Full Name
                                'emailref': 'email',  # Rep Email
                                'manager_name': '00Nd00000075Crj',  # Manager Name
                                'manager_email': '00Nd00000077r3s',  # Manager Email
                                'team': '00Nd0000005XIWB',  # Team
                                'service_segment': '00Nd0000007e2AF',  # Service Segment
                                # 'g_cases_id': '00Nd0000007dWIH',  # G Cases Id
                                'g_cases_id': '00Nd0000007f0fj',
                                'country': '00Nd0000005WYga',  # Country
                                'cid': '00Nd0000005WYgV',  # Customer ID
                                'language': '00Nd0000007clUn',  # Language
                                'tzone': '00Nd0000005WYhT',  # Time Zone

                                # Advertiser Details
                                'advertiser_name': '00Nd0000007esJ1',  # Advertiser Name
                                'advertiser_location': '00Nd0000007es7U',  # Advertiser Location
                                'aemail': '00Nd0000005WcNw',  # Advertiser Email
                                'phone': 'phone',  # Advertiser phone
                                'company': 'company',  # Advertiser Company

                                # Webmaster Details
                                'fopt': '00Nd0000005WYgp',  # Webmaster First Name
                                'lopt': '00Nd0000005WYgu',  # Webmaster Last Name
                                'webmaster_name': '00Nd0000007fJ3Q',    # Webmaster Name
                                'web_access': '00Nd0000007esIm',  # Web Access
                                'web_master_email': '00Nd0000007esIh',  # Webmaster Email
                                'popt': '00Nd0000007esIc',  # Webmaster Phone
                                'change_lead_owner': '00Nd0000007elYB',   # Default value for Change Lead Owner

                                # Agency Details
                                'agency_name': '00Nd0000007fGgD',
                                'agency_email': '00Nd0000007fGgI',
                                'agency_phone': '00Nd0000007fGgN',
                                'agency_poc': '00Nd0000007fIl7',

                                'rep_location': '00Nd0000007fJ3L',

                                # Agency Unique Field
                                'agency_bundle': '00Nd0000007fIdD',

                                # Bundle Unique Field
                                'bundle_bundle': '00Nd0000007f4St',

                                # WPP Related Fields
                                'invision_link': '00Nd0000007fa8K',
                                'conversion_goal': '00Nd0000007fa8P',
                                'wpp_lead_status': '00Nd0000007faZ6',
                                'wpp_aemail': '00Nd0000007fk3S',
                                'treatment_type': '00Nd0000008MFng',
                                'ab_testing': '00Nd0000008MFnl',
                                'tracking_code': '00Nd0000008MFnq',
                                'role_other1': '00Nd0000008MP6r',
                                'additional_notes': '00Nd0000007eiKf',
                                'advertiser_role1': '00Nd0000008MVDh',
                                'picasso_lead_status': '00Nd0000007xSwh',

                                # Appointment IST time
                                'appointment_in_ist': '00Nd0000007fnbe',

                                # Appointment PST time
                                'appointment_in_pst': '00Nd0000008M53B',

                                # Lead Type
                                'lead_type': '00Nd0000007fftD',

                                # 'first_name2': '00Nd0000005WYgp',
                                # 'last_name2': '00Nd0000005WYgu',
                                'phone2': '00Nd0000005WYgz',
                                'wpp_aemail2': '00Nd0000005WYh4',
                                'advertiser_role2': '00Nd00000081NuM',
                                'role_other2': '00Nd00000081R68',

                                'first_name3': '00Nd00000081NuR',
                                'last_name3': '00Nd00000081NuW',
                                'wpp_aemail3': '00Nd00000081Nub',
                                'phone3': '00Nd00000081Nug',
                                'advertiser_role3': '00Nd00000081Nul',
                                'role_other3': '00Nd00000081R6D',

                                'Campaign_ID': 'Campaign_ID',
                                'oid': 'oid',
                                '__VIEWSTATE': '__VIEWSTATE',
                                }

    PRODUCTION_BASIC_LEADS_ARGS = {'first_name': 'first_name',
                                   'last_name': 'last_name',
                                   'gref': '00Nd0000005WYgk',  # Full Name
                                   'emailref': 'email',  # Rep Email
                                   'manager_name': '00Nd00000075Crj',  # Manager Name
                                   'manager_email': '00Nd00000077r3s',  # Manager Email
                                   'team': '00Nd0000005XIWB',  # Team
                                   'service_segment': '00Nd0000007e2AF',  # Service Segment
                                   # 'g_cases_id': '00Nd0000007dWIH',  # G Cases Id
                                   'g_cases_id': '00Nd0000007f0fj',
                                   'country': '00Nd0000005WYga',  # Country
                                   'cid': '00Nd0000005WYgV',  # Customer ID
                                   'language': '00Nd0000007clUn',  # Language
                                   'tzone': '00Nd0000005WYhT',  # Time Zone

                                   # Advertiser Details
                                   'advertiser_name': '00Nd0000007esJ1',  # Advertiser Name
                                   'advertiser_location': '00Nd0000007es7U',  # Advertiser Location
                                   'aemail': '00Nd0000005WcNw',  # Advertiser Email
                                   'phone': 'phone',  # Advertiser phone
                                   'company': 'company',  # Advertiser Company

                                   # Webmaster Details
                                   'fopt': '00Nd0000005WYgp',  # Webmaster First Name
                                   'lopt': '00Nd0000005WYgu',  # Webmaster Last Name
                                   'webmaster_name': '00Nd0000007fJ3Q',    # Webmaster Name
                                   'web_access': '00Nd0000007esIm',  # Web Access
                                   'web_master_email': '00Nd0000007esIh',  # Webmaster Email
                                   'popt': '00Nd0000007esIc',  # Webmaster Phone
                                   'change_lead_owner': '00Nd0000007elYB',   # Default value for Change Lead Owner

                                   # Agency Details
                                   'agency_name': '00Nd0000007fGgD',
                                   'agency_email': '00Nd0000007fGgI',
                                   'agency_phone': '00Nd0000007fGgN',
                                   'agency_poc': '00Nd0000007fIl7',

                                   'rep_location': '00Nd0000007fJ3L',

                                   # Agency Unique Field
                                   'agency_bundle': '00Nd0000007fIdD',

                                   # Bundle Unique Field
                                   'bundle_bundle': '00Nd0000007f4St',

                                   # WPP Related Fields
                                   'invision_link': '00Nd0000007fa8K',
                                   'conversion_goal': '00Nd0000007fa8P',
                                   'wpp_lead_status': '00Nd0000007faZ6',
                                   'wpp_aemail': '00Nd0000007fk3S',
                                   'treatment_type': '00Nd0000008MFng',
                                   'ab_testing': '00Nd0000008MFnl',
                                   'tracking_code': '00Nd0000008MFnq',
                                   'role_other1': '00Nd0000008MP6r',
                                   'additional_notes': '00Nd0000007eiKf',
                                   'advertiser_role1': '00Nd0000008MVDh',
                                   'picasso_lead_status': '00Nd0000007xSwh',

                                   # Appointment IST time
                                   'appointment_in_ist': '00Nd0000007fnbe',

                                   # Appointment PST time
                                   'appointment_in_pst': '00Nd0000008M53B',

                                   # Lead Type
                                   'lead_type': '00Nd0000007fftD',

                                   # 'first_name2': '00Nd0000005WYgp',
                                   # 'last_name2': '00Nd0000005WYgu',
                                   'phone2': '00Nd0000005WYgz',
                                   'wpp_aemail2': '00Nd0000005WYh4',
                                   'advertiser_role2': '00Nd00000081NuM',
                                   'role_other2': '00Nd00000081R68',

                                   'first_name3': '00Nd00000081NuR',
                                   'last_name3': '00Nd00000081NuW',
                                   'wpp_aemail3': '00Nd00000081Nub',
                                   'phone3': '00Nd00000081Nug',
                                   'advertiser_role3': '00Nd00000081Nul',
                                   'role_other3': '00Nd00000081R6D',

                                   'Campaign_ID': 'Campaign_ID',
                                   'oid': 'oid',
                                   '__VIEWSTATE': '__VIEWSTATE',
                                   }

    SANDBOX_TAG_LEAD_ARGS = {'first_name': 'first_name',
                             'last_name': 'last_name',
                             'tag_datepick': '00Nd0000005WYlL',  # TAG Appointment Date
                             'setup_datepick': '00Nd0000005WYlL',  # Shopping Appointment Date
                             'tag_primary_role': '00Nd0000005WayR',  # Role
                             'dynamic_conversion_tracking': '',
                             # Code Type 1 Details
                             'ctype1': '00Nd0000005WYhJ',  # Code Type1
                             'url1': '00Nd0000005WYhE',   # URL1
                             'code1': '00Nd0000005WYh9',   # Code1
                             'comment1': '00Nd0000005WZIe',  # Comments1
                             'rbid1': '00Nd0000007fJ3V',  # Recommended Bid1
                             'rbudget1': '00Nd0000007fJ4E',  # Recommended Budget1
                             'ga_setup1': '00Nd0000007fIlH',  # Is GS Setup1
                             'analytics_code1': '00Nd0000008MVDI',  # analytics_code1
                             'call_extension1': '00Nd0000008Mi5L',  # Created Call Extension1
                             'product_behaviour1': '00Nd0000008Mi5f',  # Product Behaviour1
                             'cartpage_behaviour1': '00Nd0000008Mi64',  # Cart Page Behaviour1
                             'checkout_process1': '00Nd0000008Mi6T',  # Check Out Behaviour1
                             'transaction_behaviour1': '00Nd0000008Mi6s',  # Transaction Behaviour1

                             'user_list_id1': '00Nd0000008N42s',  # User List ID 1 for RLSA Bulk Implementation
                             'rsla_bid_adjustment1': '00Nd0000008N445',  # RLSA Bid Adjustment 1 for RLSA Bulk Implementation
                             'internal_cid1': '00Nd0000008N8wL',  # RLSA Internal Xustomer ID 1
                             'campaign_ids1': '00Nd0000008N8x4',  # RLSA campaign Ids 1
                             'rsla_policies1': '00Nd0000008N43g',  # RLSA Policies 1 for RLSA Bulk Implementation
                             'create_new_bid_modifiers1': '00Nd0000008N8yC',  # RLSA New Bid Modifiers 1 for RLSA Bulk Implementation
                             'overwrite_existing_bid_modifiers1': '00Nd0000008N8xY',  # RLSA Exist Bid Modifiers 1 for RLSA Bulk Implementation

                             # Code Type 2 Details
                             'ctype2': '00Nd0000005WYkS',  # Code Type2
                             'url2': '00Nd0000005WYi9',   # URL2
                             'code2': '00Nd0000005WYiv',   # Code2
                             'comment2': '00Nd0000005WYjy',  # Comments2
                             'rbid2': '00Nd0000007fJ3a',  # Recommended Bid2
                             'rbudget2': '00Nd0000007fJ4J',  # Recommended Budget2
                             'ga_setup2': '00Nd0000007fJ1y',  # Is GS Setup2
                             'analytics_code2': '00Nd0000008MVDN',  # analytics_code2
                             'call_extension2': '00Nd0000008MhD9',  # Created Call Extension2
                             'product_behaviour2': '00Nd0000008Mi5k',  # Product Behaviour2
                             'cartpage_behaviour2': '00Nd0000008Mi69',  # Cart Page Behaviour2
                             'checkout_process2': '00Nd0000008Mi6Y',  # Check Out Behaviour2
                             'transaction_behaviour2': '00Nd0000008Mi6x',  # Transaction Behaviour2

                             'user_list_id2': '00Nd0000008N42x',  # User List ID 2 for RLSA Bulk Implementation
                             'rsla_bid_adjustment2': '00Nd0000008N44A',  # RLSA Bid Adjustment 2 for RLSA Bulk Implementation
                             'internal_cid2': '00Nd0000008N8wV',  # RLSA Internal Xustomer ID 2
                             'campaign_ids2': '00Nd0000008N8x9',  # RLSA campaign Ids 2
                             'rsla_policies2': '00Nd0000008N43l',  # RLSA Policies 2 for RLSA Bulk Implementation
                             'create_new_bid_modifiers2': '00Nd0000008N8yM',  # RLSA New Bid Modifiers 2 for RLSA Bulk Implementation
                             'overwrite_existing_bid_modifiers2': '00Nd0000008N8xd',  # RLSA Exist Bid Modifiers 2 for RLSA Bulk Implementation

                             # Code Type 3 Details
                             'ctype3': '00Nd0000005WYkX',  # Code Type3
                             'url3': '00Nd0000005WYjU',   # URL3
                             'code3': '00Nd0000005WYj5',   # Code3
                             'comment3': '00Nd0000005WYjB',  # Comments3
                             'rbid3': '00Nd0000007fJ3f',  # Recommended Bid3
                             'rbudget3': '00Nd0000007fJ4O',  # Recommended Budget3
                             'ga_setup3': '00Nd0000007fJ23',  # Is GS Setup3
                             'analytics_code3': '00Nd0000008MVDS',  # analytics_code3
                             'call_extension3': '00Nd0000008Mi5Q',  # Created Call Extension3
                             'product_behaviour3': '00Nd0000008Mi5p',  # Product Behaviour3
                             'cartpage_behaviour3': '00Nd0000008Mi6E',  # Cart Page Behaviour3
                             'checkout_process3': '00Nd0000008Mi6d',  # Check Out Behaviour3
                             'transaction_behaviour3': '00Nd0000008Mi72',  # Transaction Behaviour3

                             'user_list_id3': '00Nd0000008N432',  # User List ID 3 for RLSA Bulk Implementation
                             'rsla_bid_adjustment3': '00Nd0000008N44F',  # RLSA Bid Adjustment 3 for RLSA Bulk Implementation
                             'internal_cid3': '00Nd0000008N8wk',  # RLSA Internal Xustomer ID 3
                             'campaign_ids3': '00Nd0000008N8xE',  # RLSA campaign Ids 3
                             'rsla_policies3': '00Nd0000008N43q',  # RLSA Policies 3 for RLSA Bulk Implementation
                             'create_new_bid_modifiers3': '00Nd0000008N8yR',  # RLSA New Bid Modifiers 3 for RLSA Bulk Implementation
                             'overwrite_existing_bid_modifiers3': '00Nd0000008N8xi',  # RLSA Exist Bid Modifiers 3 for RLSA Bulk Implementation

                             # Code Type 4 Details
                             'ctype4': '00Nd0000005WYkm',  # Code Type4
                             'url4': '00Nd0000005WYjZ',   # URL4
                             'code4': '00Nd0000005WYjA',   # Code4
                             'comment4': '00Nd0000005WYkI',  # Comments4
                             'rbid4': '00Nd0000007fJ44',  # Recommended Bid4
                             'rbudget4': '00Nd0000007fJ4Y',  # Recommended Budget4
                             'ga_setup4': '00Nd0000007fJ28',  # Is GS Setup4
                             'analytics_code4': '00Nd0000008MVDX',  # analytics_code4
                             'call_extension4': '00Nd0000008Mi5V',  # Created Call Extension4
                             'product_behaviour4': '00Nd0000008Mi5u',  # Product Behaviour4
                             'cartpage_behaviour4': '00Nd0000008Mi6J',  # Cart Page Behaviour4
                             'checkout_process4': '00Nd0000008Mi6i',  # Check Out Behaviour4
                             'transaction_behaviour4': '00Nd0000008Mi77',  # Transaction Behaviour4

                             'user_list_id4': '00Nd0000008N437',  # User List ID 4 for RLSA Bulk Implementation
                             'rsla_bid_adjustment4': '00Nd0000008N44K',  # RLSA Bid Adjustment 4 for RLSA Bulk Implementation
                             'internal_cid4': '00Nd0000008N8wu',  # RLSA Internal Xustomer ID 4
                             'campaign_ids4': '00Nd0000008N8xO',  # RLSA campaign Ids 4
                             'rsla_policies4': '00Nd0000008N43v',  # RLSA Policies 4 for RLSA Bulk Implementation
                             'create_new_bid_modifiers4': '00Nd0000008N8yg',  # RLSA New Bid Modifiers 4 for RLSA Bulk Implementation
                             'overwrite_existing_bid_modifiers4': '00Nd0000008N8xn',  # RLSA Exist Bid Modifiers 4 for RLSA Bulk Implementation


                             # Code Type 4 Details
                             'ctype5': '00Nd0000005WYl6',  # Code Type5
                             'url5': '00Nd0000005WYjo',   # URL5
                             'code5': '00Nd0000005WYiw',   # Code5
                             'comment5': '00Nd0000005WYkN',  # Comments5
                             'rbid5': '00Nd0000007fJ49',  # Recommended Bid5
                             'rbudget5': '00Nd0000007fJ4d',  # Recommended Budget5
                             'ga_setup5': '00Nd0000007fJ2D',  # Is GS Setup5
                             'analytics_code5': '00Nd0000008MVDc',  # analytics_code5
                             'call_extension5': '00Nd0000008Mi5a',  # Created Call Extension5
                             'product_behaviour5': '00Nd0000008Mi5z',  # Product Behaviour5
                             'cartpage_behaviour5': '00Nd0000008Mi6O',  # Cart Page Behaviour5
                             'checkout_process5': '00Nd0000008Mi6n',  # Check Out Behaviour5
                             'transaction_behaviour5': '00Nd0000008Mi7C',  # Transaction Behaviour5

                             'user_list_id5': '00Nd0000008N43C',  # User List ID 5 for RLSA Bulk Implementation
                             'rsla_bid_adjustment5': '00Nd0000008N44P',  # RLSA Bid Adjustment 5 for RLSA Bulk Implementation
                             'internal_cid5': '00Nd0000008N8wz',  # RLSA Internal Xustomer ID 5
                             'campaign_ids5': '00Nd0000008N8xT',  # RLSA campaign Ids 5
                             'rsla_policies5': '00Nd0000008N440',  # RLSA Policies 5 for RLSA Bulk Implementation
                             'create_new_bid_modifiers5': '00Nd0000008N8yl',  # RLSA New Bid Modifiers 5 for RLSA Bulk Implementation
                             'overwrite_existing_bid_modifiers5': '00Nd0000008N8xx',  # RLSA Exist Bid Modifiers 5 for RLSA Bulk Implementation

                             'tag_via_gtm': '00Nd0000007esIr',
                             'picasso_objective_list[]': '00Nd0000007xSXh',
                             'picasso_pod': '00Nd0000007xVWc',  # Picasso POD name
                             }

    PRODUCTION_TAG_LEADS_ARGS = {'first_name': 'first_name',
                                 'last_name': 'last_name',
                                 'tag_datepick': '00Nd0000005WYlL',  # TAG Appointment Date
                                 'setup_datepick': '00Nd0000005WYlL',  # Shopping Appointment Date
                                 'tag_primary_role': '00Nd0000005WayR',  # Role
                                 'dynamic_conversion_tracking': '00Nd00000081fGG',  # Dynamic value for conversion tracking
                                 # Code Type 1 Details
                                 'ctype1': '00Nd0000005WYhJ',  # Code Type1
                                 'url1': '00Nd0000005WYhE',   # URL1
                                 'code1': '00Nd0000005WYh9',   # Code1
                                 'comment1': '00Nd0000005WZIe',  # Comments1
                                 'rbid1': '00Nd0000007fJ3V',  # Recommended Bid1
                                 'rbudget1': '00Nd0000007fJ4E',  # Recommended Budget1
                                 'ga_setup1': '00Nd0000007fIlH',  # Is GS Setup1
                                 'analytics_code1': '00Nd0000008MVDI',  # analytics_code1
                                 'call_extension1': '00Nd0000008Mi5L',  # Created Call Extension1
                                 'product_behaviour1': '00Nd0000008Mi5f',  # Product Behaviour1
                                 'cartpage_behaviour1': '00Nd0000008Mi64',  # Cart Page Behaviour1
                                 'checkout_process1': '00Nd0000008Mi6T',  # Check Out Behaviour1
                                 'transaction_behaviour1': '00Nd0000008Mi6s',  # Transaction Behaviour1

                                 'user_list_id1': '00Nd0000008N42s',  # User List ID 1 for RLSA Bulk Implementation
                                 'rsla_bid_adjustment1': '00Nd0000008N445',  # RLSA Bid Adjustment 1 for RLSA Bulk Implementation
                                 'internal_cid1': '00Nd0000008N8wL',  # RLSA Internal Xustomer ID 1
                                 'campaign_ids1': '00Nd0000008N8x4',  # RLSA campaign Ids 1
                                 'rsla_policies1': '00Nd0000008N43g',  # RLSA Policies 1 for RLSA Bulk Implementation
                                 'create_new_bid_modifiers1': '00Nd0000008N8yC',  # RLSA New Bid Modifiers 1 for RLSA Bulk Implementation
                                 'overwrite_existing_bid_modifiers1': '00Nd0000008N8xY',  # RLSA Exist Bid Modifiers 1 for RLSA Bulk Implementation

                                 # Code Type 2 Details
                                 'ctype2': '00Nd0000005WYkS',  # Code Type2
                                 'url2': '00Nd0000005WYi9',   # URL2
                                 'code2': '00Nd0000005WYiv',   # Code2
                                 'comment2': '00Nd0000005WYjy',  # Comments2
                                 'rbid2': '00Nd0000007fJ3a',  # Recommended Bid2
                                 'rbudget2': '00Nd0000007fJ4J',  # Recommended Budget2
                                 'ga_setup2': '00Nd0000007fJ1y',  # Is GS Setup2
                                 'analytics_code2': '00Nd0000008MVDN',  # analytics_code2
                                 'call_extension2': '00Nd0000008MhD9',  # Created Call Extension2
                                 'product_behaviour2': '00Nd0000008Mi5k',  # Product Behaviour2
                                 'cartpage_behaviour2': '00Nd0000008Mi69',  # Cart Page Behaviour2
                                 'checkout_process2': '00Nd0000008Mi6Y',  # Check Out Behaviour2
                                 'transaction_behaviour2': '00Nd0000008Mi6x',  # Transaction Behaviour2

                                 'user_list_id2': '00Nd0000008N42x',  # User List ID 2 for RLSA Bulk Implementation
                                 'rsla_bid_adjustment2': '00Nd0000008N44A',  # RLSA Bid Adjustment 2 for RLSA Bulk Implementation
                                 'internal_cid2': '00Nd0000008N8wV',  # RLSA Internal Xustomer ID 2
                                 'campaign_ids2': '00Nd0000008N8x9',  # RLSA campaign Ids 2
                                 'rsla_policies2': '00Nd0000008N43l',  # RLSA Policies 2 for RLSA Bulk Implementation
                                 'create_new_bid_modifiers2': '00Nd0000008N8yM',  # RLSA New Bid Modifiers 2 for RLSA Bulk Implementation
                                 'overwrite_existing_bid_modifiers2': '00Nd0000008N8xd',  # RLSA Exist Bid Modifiers 2 for RLSA Bulk Implementation

                                 # Code Type 3 Details
                                 'ctype3': '00Nd0000005WYkX',  # Code Type3
                                 'url3': '00Nd0000005WYjU',   # URL3
                                 'code3': '00Nd0000005WYj5',   # Code3
                                 'comment3': '00Nd0000005WYjB',  # Comments3
                                 'rbid3': '00Nd0000007fJ3f',  # Recommended Bid3
                                 'rbudget3': '00Nd0000007fJ4O',  # Recommended Budget3
                                 'ga_setup3': '00Nd0000007fJ23',  # Is GS Setup3
                                 'analytics_code3': '00Nd0000008MVDS',  # analytics_code3
                                 'call_extension3': '00Nd0000008Mi5Q',  # Created Call Extension3
                                 'product_behaviour3': '00Nd0000008Mi5p',  # Product Behaviour3
                                 'cartpage_behaviour3': '00Nd0000008Mi6E',  # Cart Page Behaviour3
                                 'checkout_process3': '00Nd0000008Mi6d',  # Check Out Behaviour3
                                 'transaction_behaviour3': '00Nd0000008Mi72',  # Transaction Behaviour3

                                 'user_list_id3': '00Nd0000008N432',  # User List ID 3 for RLSA Bulk Implementation
                                 'rsla_bid_adjustment3': '00Nd0000008N44F',  # RLSA Bid Adjustment 3 for RLSA Bulk Implementation
                                 'internal_cid3': '00Nd0000008N8wk',  # RLSA Internal Xustomer ID 3
                                 'campaign_ids3': '00Nd0000008N8xE',  # RLSA campaign Ids 3
                                 'rsla_policies3': '00Nd0000008N43q',  # RLSA Policies 3 for RLSA Bulk Implementation
                                 'create_new_bid_modifiers3': '00Nd0000008N8yR',  # RLSA New Bid Modifiers 3 for RLSA Bulk Implementation
                                 'overwrite_existing_bid_modifiers3': '00Nd0000008N8xi',  # RLSA Exist Bid Modifiers 3 for RLSA Bulk Implementation

                                 # Code Type 4 Details
                                 'ctype4': '00Nd0000005WYkm',  # Code Type4
                                 'url4': '00Nd0000005WYjZ',   # URL4
                                 'code4': '00Nd0000005WYjA',   # Code4
                                 'comment4': '00Nd0000005WYkI',  # Comments4
                                 'rbid4': '00Nd0000007fJ44',  # Recommended Bid4
                                 'rbudget4': '00Nd0000007fJ4Y',  # Recommended Budget4
                                 'ga_setup4': '00Nd0000007fJ28',  # Is GS Setup4
                                 'analytics_code4': '00Nd0000008MVDX',  # analytics_code4
                                 'call_extension4': '00Nd0000008Mi5V',  # Created Call Extension4
                                 'product_behaviour4': '00Nd0000008Mi5u',  # Product Behaviour4
                                 'cartpage_behaviour4': '00Nd0000008Mi6J',  # Cart Page Behaviour4
                                 'checkout_process4': '00Nd0000008Mi6i',  # Check Out Behaviour4
                                 'transaction_behaviour4': '00Nd0000008Mi77',  # Transaction Behaviour4

                                 'user_list_id4': '00Nd0000008N437',  # User List ID 4 for RLSA Bulk Implementation
                                 'rsla_bid_adjustment4': '00Nd0000008N44K',  # RLSA Bid Adjustment 4 for RLSA Bulk Implementation
                                 'internal_cid4': '00Nd0000008N8wu',  # RLSA Internal Xustomer ID 4
                                 'campaign_ids4': '00Nd0000008N8xO',  # RLSA campaign Ids 4
                                 'rsla_policies4': '00Nd0000008N43v',  # RLSA Policies 4 for RLSA Bulk Implementation
                                 'create_new_bid_modifiers4': '00Nd0000008N8yg',  # RLSA New Bid Modifiers 4 for RLSA Bulk Implementation
                                 'overwrite_existing_bid_modifiers4': '00Nd0000008N8xn',  # RLSA Exist Bid Modifiers 4 for RLSA Bulk Implementation

                                 # Code Type 4 Details
                                 'ctype5': '00Nd0000005WYl6',  # Code Type5
                                 'url5': '00Nd0000005WYjo',   # URL5
                                 'code5': '00Nd0000005WYiw',   # Code5
                                 'comment5': '00Nd0000005WYkN',  # Comments5
                                 'rbid5': '00Nd0000007fJ49',  # Recommended Bid5
                                 'rbudget5': '00Nd0000007fJ4d',  # Recommended Budget5
                                 'ga_setup5': '00Nd0000007fJ2D',  # Is GS Setup5
                                 'analytics_code5': '00Nd0000008MVDc',  # analytics_code5
                                 'call_extension5': '00Nd0000008Mi5a',  # Created Call Extension5
                                 'product_behaviour5': '00Nd0000008Mi5z',  # Product Behaviour5
                                 'cartpage_behaviour5': '00Nd0000008Mi6O',  # Cart Page Behaviour5
                                 'checkout_process5': '00Nd0000008Mi6n',  # Check Out Behaviour5
                                 'transaction_behaviour5': '00Nd0000008Mi7C',  # Transaction Behaviour5

                                 'user_list_id5': '00Nd0000008N43C',  # User List ID 5 for RLSA Bulk Implementation
                                 'rsla_bid_adjustment5': '00Nd0000008N44P',  # RLSA Bid Adjustment 5 for RLSA Bulk Implementation
                                 'internal_cid5': '00Nd0000008N8wz',  # RLSA Internal Xustomer ID 5
                                 'campaign_ids5': '00Nd0000008N8xT',  # RLSA campaign Ids 5
                                 'rsla_policies5': '00Nd0000008N440',  # RLSA Policies 5 for RLSA Bulk Implementation
                                 'create_new_bid_modifiers5': '00Nd0000008N8yl',  # RLSA New Bid Modifiers 5 for RLSA Bulk Implementation
                                 'overwrite_existing_bid_modifiers5': '00Nd0000008N8xx',  # RLSA Exist Bid Modifiers 5 for RLSA Bulk Implementation

                                 'tag_via_gtm': '00Nd0000007esIr',
                                 'picasso_objective_list[]': '00Nd0000007xSXh',
                                 'picasso_pod': '00Nd0000007xVWc',  # Picasso POD name
                                 }

    SANDBOX_SHOPPING_ARGS = {'shop_primary_role': '00Nd0000005WayR',
                             'setup_datepick': '00Nd0000005WYlL',  # Shopping Appointment Date
                             'ctype1': '00Nd0000005WYhJ',  # Code Type Shopping
                             'comment1': '00Nd0000005WZIe',  # Comments1
                             'mc_id': '00Nd00000077T9o',  # MC-ID
                             'web_client_inventory': '00Nd00000077T9t',  # Web Inventory
                             'rbid': '00Nd00000077T9y',  # Recommended Bid1s
                             'rbudget': '00Nd00000077TA3',  # Recommended Budget1
                             'rbidmodifier': '00Nd00000077TA8',  # Recommended Mobile Bid Modifier
                             'shopping_url': '00Nd0000005WYhE',  # Shopping URL
                             'is_shopping_policies': '00Nd0000007esIw',  # Shopping policies
                             }
    PRODUCTION_SHOPPING_ARGS = {'shop_primary_role': '00Nd0000005WayR',
                                'setup_datepick': '00Nd0000005WYlL',  # Shopping Appointment Date
                                'ctype1': '00Nd0000005WYhJ',  # Code Type Shopping
                                'comment1': '00Nd0000005WZIe',  # Comments1
                                'mc_id': '00Nd00000077T9o',  # MC-ID
                                'web_client_inventory': '00Nd00000077T9t',  # Web Inventory
                                'rbid': '00Nd00000077T9y',  # Recommended Bid1s
                                'rbudget': '00Nd00000077TA3',  # Recommended Budget1
                                'rbidmodifier': '00Nd00000077TA8',  # Recommended Mobile Bid Modifier
                                'shopping_url': '00Nd0000005WYhE',  # Shopping URL
                                'is_shopping_policies': '00Nd0000007esIw',  # Shopping policies
                                }
