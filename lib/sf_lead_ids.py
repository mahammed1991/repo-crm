
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
                                #'web_access': '00Nd0000007esIm',  # Web Access
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
                                #picasso new fields
                                'corp_email': '00N7A000000ZOdl',
                                'advertiser_email': '00N7A000000ZOkm',
                                'cases_alias': '00N7A000000ZOlB',
                                'market_selector': '00N7A000000ZOlk',
                                'picasso_type': '00N7A000000ZQAC',
                                # ETO Ldap
                                'eto_ldap': '00N7A000000ZQ8p',
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
                                   #'web_access': '00Nd0000007esIm',  # Web Access
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

                                   #Additional ETO-LDAP field
                                   'eto_ldap': '00Nd0000008SWkF',
                                   }

    SANDBOX_TAG_LEAD_ARGS = {'first_name': 'first_name',
                             'last_name': 'last_name',
                             'tag_datepick': '00Nd0000005WYlL',  # TAG Appointment Date
                             'setup_datepick': '00Nd0000005WYlL',  # Shopping Appointment Date
                             'tag_primary_role': '00Nd0000005WayR',  # Role
                             'dynamic_conversion_tracking': '00N7A000000I22d',
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

                             'tag_via_gtm': '00Nd0000007esIr',
                             'picasso_objective_list[]': '00Nd0000007xSXh',
                             'picasso_pod': '00Nd0000007xVWc',  # Picasso POD name
                             'unique_ref_id': '00N7A000000HAhN',  # picasso unique id
                             'picasso_tat': '00N7A000000I6pe',  # picasso TAT
                             'picasso_auto_number': '00N7A000000SrlK',  # picasso auto number
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

                                 'tag_via_gtm': '00Nd0000007esIr',
                                 'picasso_objective_list[]': '00Nd0000007xSXh',
                                 'picasso_pod': '00Nd0000007xVWc',  # Picasso POD name
                                 'unique_ref_id': '00Nd00000081spN',  # picasso unique id
                                 'picasso_tat': '00Nd00000081yHV',  # picasso TAT
                                 'picasso_auto_number': '00Nd00000082aQm',  # picasso auto number
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
                             'shopping_campaign_issues': '00N7A000000Siv6',  # Field which store issue type
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
                                'shopping_campaign_issues': '00Nd00000082TgW',  # Field which store issue type
                                }
    SANDBOX_RLSA_ARGS = {'user_list_id1': '00Nd0000008N42s',  # User List ID 1 for RLSA Bulk Implementation
                         'rsla_bid_adjustment1': '00Nd0000008N445',  # RLSA Bid Adjustment 1 for RLSA Bulk Implementation
                         'internal_cid1': '00Nd0000008N8wL',  # RLSA Internal Xustomer ID 1
                         'campaign_ids1': '00Nd0000008N8x4',  # RLSA campaign Ids 1
                         'create_new_bid_modifiers1': '00Nd0000008N8yC',  # RLSA New Bid Modifiers 1 for RLSA Bulk Implementation
                         'overwrite_existing_bid_modifiers1': '00Nd0000008N8xY',  # RLSA Exist Bid Modifiers 1 for RLSA Bulk Implementation

                         'user_list_id2': '00Nd0000008N42x',  # User List ID 2 for RLSA Bulk Implementation
                         'rsla_bid_adjustment2': '00Nd0000008N44A',  # RLSA Bid Adjustment 2 for RLSA Bulk Implementation
                         'internal_cid2': '00Nd0000008N8wV',  # RLSA Internal Xustomer ID 2
                         'campaign_ids2': '00Nd0000008N8x9',  # RLSA campaign Ids 2
                         'create_new_bid_modifiers2': '00Nd0000008N8yM',  # RLSA New Bid Modifiers 2 for RLSA Bulk Implementation
                         'overwrite_existing_bid_modifiers2': '00Nd0000008N8xd',  # RLSA Exist Bid Modifiers 2 for RLSA Bulk Implementation

                         'user_list_id3': '00Nd0000008N432',  # User List ID 3 for RLSA Bulk Implementation
                         'rsla_bid_adjustment3': '00Nd0000008N44F',  # RLSA Bid Adjustment 3 for RLSA Bulk Implementation
                         'internal_cid3': '00Nd0000008N8wk',  # RLSA Internal Xustomer ID 3
                         'campaign_ids3': '00Nd0000008N8xE',  # RLSA campaign Ids 3
                         'create_new_bid_modifiers3': '00Nd0000008N8yR',  # RLSA New Bid Modifiers 3 for RLSA Bulk Implementation
                         'overwrite_existing_bid_modifiers3': '00Nd0000008N8xi',  # RLSA Exist Bid Modifiers 3 for RLSA Bulk Implementation

                         'user_list_id4': '00Nd0000008N437',  # User List ID 4 for RLSA Bulk Implementation
                         'rsla_bid_adjustment4': '00Nd0000008N44K',  # RLSA Bid Adjustment 4 for RLSA Bulk Implementation
                         'internal_cid4': '00Nd0000008N8wu',  # RLSA Internal Xustomer ID 4
                         'campaign_ids4': '00Nd0000008N8xO',  # RLSA campaign Ids 4
                         'create_new_bid_modifiers4': '00Nd0000008N8yg',  # RLSA New Bid Modifiers 4 for RLSA Bulk Implementation
                         'overwrite_existing_bid_modifiers4': '00Nd0000008N8xn',  # RLSA Exist Bid Modifiers 4 for RLSA Bulk Implementation


                         'user_list_id5': '00Nd0000008N43C',  # User List ID 5 for RLSA Bulk Implementation
                         'rsla_bid_adjustment5': '00Nd0000008N44P',  # RLSA Bid Adjustment 5 for RLSA Bulk Implementation
                         'internal_cid5': '00Nd0000008N8wz',  # RLSA Internal Xustomer ID 5
                         'campaign_ids5': '00Nd0000008N8xT',  # RLSA campaign Ids 5
                         'create_new_bid_modifiers5': '00Nd0000008N8yl',  # RLSA New Bid Modifiers 5 for RLSA Bulk Implementation
                         'overwrite_existing_bid_modifiers5': '00Nd0000008N8xx',  # RLSA Exist Bid Modifiers 5 for RLSA Bulk Implementation

                         }
    PRODUCTION_RLSA_ARGS = {'user_list_id1': '00Nd0000008N42s',  # User List ID 1 for RLSA Bulk Implementation
                            'rsla_bid_adjustment1': '00Nd0000008N445',  # RLSA Bid Adjustment 1 for RLSA Bulk Implementation
                            'internal_cid1': '00Nd0000008N8wL',  # RLSA Internal Xustomer ID 1
                            'campaign_ids1': '00Nd0000008N8x4',  # RLSA campaign Ids 1
                            'create_new_bid_modifiers1': '00Nd0000008N8yC',  # RLSA New Bid Modifiers 1 for RLSA Bulk Implementation
                            'overwrite_existing_bid_modifiers1': '00Nd0000008N8xY',  # RLSA Exist Bid Modifiers 1 for RLSA Bulk Implementation

                            'user_list_id2': '00Nd0000008N42x',  # User List ID 2 for RLSA Bulk Implementation
                            'rsla_bid_adjustment2': '00Nd0000008N44A',  # RLSA Bid Adjustment 2 for RLSA Bulk Implementation
                            'internal_cid2': '00Nd0000008N8wV',  # RLSA Internal Xustomer ID 2
                            'campaign_ids2': '00Nd0000008N8x9',  # RLSA campaign Ids 2
                            'create_new_bid_modifiers2': '00Nd0000008N8yM',  # RLSA New Bid Modifiers 2 for RLSA Bulk Implementation
                            'overwrite_existing_bid_modifiers2': '00Nd0000008N8xd',  # RLSA Exist Bid Modifiers 2 for RLSA Bulk Implementation

                            'user_list_id3': '00Nd0000008N432',  # User List ID 3 for RLSA Bulk Implementation
                            'rsla_bid_adjustment3': '00Nd0000008N44F',  # RLSA Bid Adjustment 3 for RLSA Bulk Implementation
                            'internal_cid3': '00Nd0000008N8wk',  # RLSA Internal Xustomer ID 3
                            'campaign_ids3': '00Nd0000008N8xE',  # RLSA campaign Ids 3
                            'create_new_bid_modifiers3': '00Nd0000008N8yR',  # RLSA New Bid Modifiers 3 for RLSA Bulk Implementation
                            'overwrite_existing_bid_modifiers3': '00Nd0000008N8xi',  # RLSA Exist Bid Modifiers 3 for RLSA Bulk Implementation

                            'user_list_id4': '00Nd0000008N437',  # User List ID 4 for RLSA Bulk Implementation
                            'rsla_bid_adjustment4': '00Nd0000008N44K',  # RLSA Bid Adjustment 4 for RLSA Bulk Implementation
                            'internal_cid4': '00Nd0000008N8wu',  # RLSA Internal Xustomer ID 4
                            'campaign_ids4': '00Nd0000008N8xO',  # RLSA campaign Ids 4
                            'create_new_bid_modifiers4': '00Nd0000008N8yg',  # RLSA New Bid Modifiers 4 for RLSA Bulk Implementation
                            'overwrite_existing_bid_modifiers4': '00Nd0000008N8xn',  # RLSA Exist Bid Modifiers 4 for RLSA Bulk Implementation


                            'user_list_id5': '00Nd0000008N43C',  # User List ID 5 for RLSA Bulk Implementation
                            'rsla_bid_adjustment5': '00Nd0000008N44P',  # RLSA Bid Adjustment 5 for RLSA Bulk Implementation
                            'internal_cid5': '00Nd0000008N8wz',  # RLSA Internal Xustomer ID 5
                            'campaign_ids5': '00Nd0000008N8xT',  # RLSA campaign Ids 5
                            'create_new_bid_modifiers5': '00Nd0000008N8yl',  # RLSA New Bid Modifiers 5 for RLSA Bulk Implementation
                            'overwrite_existing_bid_modifiers5': '00Nd0000008N8xx',  # RLSA Exist Bid Modifiers 5 for RLSA Bulk Implementation
                            }
    GOOGLE_FORM_FIELDS = {  'advertiser_name': 'entry.1188542696',
                            'aemail': 'entry.1788130986',
                            'cid': 'entry.1316565280',
                            'company': 'entry.1775166236',
                            'country': 'entry.1320886132',
                            'emailref': 'entry.1798356961',
                            'eto_ldap': 'entry.987152811',
                            'g_cases_id': 'entry.131955320',
                            'gref': 'entry.1184993473',
                            'language': 'entry.67038829',
                            'manager_email': 'entry.1363863642',
                            'manager_name': 'entry.1804367188',
                            'phone': 'entry.1143944166',
                            'popt': 'entry.2066285918',
                            'region': 'entry.415026115',
                            'rep_location': 'entry.574822536',
                            'team': 'entry.1892690962',
                            'tzone': 'entry.90911376',
                            'web_master_email': 'entry.2030163503',
                            'webmaster_name': 'entry.252625587',

                            #  Tag Fields
                            'ctype1': 'entry.681140147',
                            'url1': 'entry.1882609979',
                            'code1': 'entry.406511040',
                            'comment1': 'entry.844017316',
                            'ga_setup1': 'entry.95155047',
                            'analytics_code1': 'entry.213494926',
                            'call_extension1': 'entry.774904788',

                            'ctype2': 'entry.786000779',
                            'url2': 'entry.786383423',
                            'code2': 'entry.414196118',
                            'comment2': 'entry.907186352',
                            'ga_setup2': 'entry.1498927589',
                            'analytics_code2': 'entry.213494926',
                            'call_extension2': 'entry.774904788',

                            'ctype3': 'entry.403116742',
                            'url3': 'entry.855157412',
                            'code3': 'entry.704991401',
                            'comment3': 'entry.2090881147',
                            'ga_setup3': 'entry.1176854708',
                            'analytics_code3': 'entry.645983348',
                            'call_extension3': 'entry.367865630',

                            'ctype4': 'entry.139286178',
                            'url4': 'entry.1947399661',
                            'code4': 'entry.1149181904',
                            'comment4': 'entry.2070690220',
                            'ga_setup4': 'entry.579257169',
                            'analytics_code4': 'entry.711795656',
                            'call_extension4': 'entry.34052951',

                            'ctype5': 'entry.113173660',
                            'url5': 'entry.429278860',
                            'code5': 'entry.1664973693',
                            'comment5': 'entry.768003959',
                            'ga_setup5': 'entry.915928401',
                            'analytics_code5': 'entry.2045915679',
                            'call_extension5': 'entry.106190628',

                            'tag_contact_person_name': 'entry.2063272559',
                            'tag_primary_role': 'entry.1400432559',
                            'tag_datepick': 'entry.552178151',

                            #  Shopping
                            'rbid': 'entry.1563011418',
                            'rbidmodifier': 'entry.1742028508',
                            'rbudget': 'entry.1662192511',
                            'shopping_url': 'entry.1831519087',
                            'description': 'entry.785681716',
                            'mc_id': 'entry.229311894',
                            'shopping_campaign_issues': 'entry.1691278225',
                            'issues_description': 'entry.1403415245',

                            'shop_contact_person_name': 'entry.1060603606',
                            'shop_primary_role': 'entry.1351837283',
                            'setup_datepick': 'entry.1460666611',

                            #  RLSA Fields
                            'internal_cid1': 'entry.1941742213',
                            'authEmail': 'entry.830713560',
                            'comments': 'entry.1295983593',
                            'user_list_id1': 'entry.225610243',
                            'rsla_bid_adjustment1': 'entry.541709774',
                            'user_list_id2': 'entry.697559661',
                            'rsla_bid_adjustment2': 'entry.1745391788',
                            'user_list_id3': 'entry.1954825855',
                            'rsla_bid_adjustment3': 'entry.1919723385',
                            'user_list_id4': 'entry.127784518',
                            'rsla_bid_adjustment4': 'entry.1710613720',
                            'user_list_id5': 'entry.2064640159',
                            'rsla_bid_adjustment5': 'entry.1256315356',
                        }


    # SUBMIT PICASSO BUILD google sheets
    GOOGLE_PICASSO_BUILD_FORM_FIELDS =  {
                            'cid': 'entry.955236578',
                            'url1': 'entry.254552489',
                            'treatment_type': 'entry.1727939026',
                            'gref': 'entry.1745278576',
                            'team': 'entry.1341301914',
                            'picasso_pod': 'entry.1635462084',
                            'picasso_objective_list[]': 'entry.1157346905',
                            'tracking_code': 'entry.128502142',
                            'ab_testing': 'entry.1532547706',
                            'first_name': 'entry.1368522440',
                            'first_name2': 'entry.1717535950',
                            'last_name': 'entry.84679538',
                            'last_name2': 'entry.1923558617',
                            'wpp_aemail': 'entry.2078001533',
                            'wpp_aemail2': 'entry.1027376881',
                            'phone': 'entry.885187179',
                            'phone2': 'entry.143922862',
                            'advertiser_role1': 'entry.2043998837',
                            'advertiser_role2': 'entry.769255000',
                            'country': 'entry.1134302136',
                            'tzone': 'entry.239294134',
                            'tag_datepick': 'entry.1305368918',
                            'additional_notes': 'entry.1719133589'
                        }
    # SUBMIT PICASSO lead form
    GOOGLE_FORM_PICASSO_FIELDS = {
                           'gref': 'entry.1549122955',
                           'team': 'entry.1462749639',
                           'cid': 'entry.516568524',
                           'picasso_pod': 'entry.78629807',
                           'url1': 'entry.1406592858',
                           'additional_notes': 'entry.929766348',
                           'picasso_objective_list[]': 'entry.652078496',
                           }
