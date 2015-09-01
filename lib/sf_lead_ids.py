
class SalesforceLeads(object):

    SANDBOX_BASIC_LEADS_ARGS = {'first_name': 'first_name',
                                'last_name': 'last_name',
                                'gref': '00Nd0000005WYgk',  # Full Name
                                'emailref': 'email',  # Rep Email
                                'manager_name': '00Nd00000075Crj',  # Manager Name
                                'manager_email': '00Nd00000077r3s',  # Manager Email
                                'team': '00Nd0000005XIWB',  # Team
                                'service_segment': '00Nd0000007e2AF',  # Service Segment
                                'g_cases_id': '00Nd0000007dWIH',  # G Cases Id
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
                                'role_other': '00Nd0000008MP6r',
                                'additional_notes': '00Nd0000007eiKf',
                                'advertiser_role': '00Nd0000008MVDh',

                                # Appointment IST time
                                'appointment_in_ist': '00Nd0000007fnbe',

                                # Appointment PST time
                                'appointment_in_pst': '00Nd0000008M53B',

                                # Lead Type
                                'lead_type': '00Nd0000007fftD',

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
                                   'g_cases_id': '00Nd0000007dWIH',  # G Cases Id
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
                                   'role_other': '00Nd0000008MP6r',
                                   'additional_notes': '00Nd0000007eiKf',
                                   'advertiser_role': '00Nd0000008MVDh',

                                   # Appointment IST time
                                   'appointment_in_ist': '00Nd0000007fnbe',

                                   # Appointment PST time
                                   'appointment_in_pst': '00Nd0000008M53B',

                                   # Lead Type
                                   'lead_type': '00Nd0000007fftD',

                                   'Campaign_ID': 'Campaign_ID',
                                   'oid': 'oid',
                                   '__VIEWSTATE': '__VIEWSTATE',
                                   }

    SANDBOX_TAG_LEAD_ARGS = {'first_name': 'first_name',
                             'last_name': 'last_name',
                             'tag_datepick': '00Nd0000005WYlL',  # TAG Appointment Date
                             'setup_datepick': '00Nd0000005WYlL',  # Shopping Appointment Date
                             'tag_primary_role': '00Nd0000005WayR',  # Role
                             # Code Type 1 Details
                             'ctype1': '00Nd0000005WYhJ',  # Code Type1
                             'url1': '00Nd0000005WYhE',   # URL1
                             'code1': '00Nd0000005WYh9',   # Code1
                             'comment1': '00Nd0000005WZIe',  # Comments1
                             'rbid1': '00Nd0000007fJ3V',  # Recommended Bid1
                             'rbudget1': '00Nd0000007fJ4E',  # Recommended Budget1
                             'ga_setup1': '00Nd0000007fIlH',  # Is GS Setup1
                             'analytics_code1': '00Nd0000008MVDI',  # analytics_code1
                             'call_extension1': '',  # Created Call Extension1
                             'product_behaviour1': '',  # Product Behaviour1
                             'cartpage_behaviour1': '',  # Cart Page Behaviour1
                             'checkout_process1': '',  # Check Out Behaviour1
                             'transaction_behaviour1': '',  # Transaction Behaviour1

                             # Code Type 2 Details
                             'ctype2': '00Nd0000005WYkS',  # Code Type2
                             'url2': '00Nd0000005WYi9',   # URL2
                             'code2': '00Nd0000005WYiv',   # Code2
                             'comment2': '00Nd0000005WYjy',  # Comments2
                             'rbid2': '00Nd0000007fJ3a',  # Recommended Bid2
                             'rbudget2': '00Nd0000007fJ4J',  # Recommended Budget2
                             'ga_setup2': '00Nd0000007fJ1y',  # Is GS Setup2
                             'analytics_code2': '00Nd0000008MVDN',  # analytics_code2
                             'call_extension2': '',  # Created Call Extension2
                             'product_behaviour2': '',  # Product Behaviour2
                             'cartpage_behaviour2': '',  # Cart Page Behaviour2
                             'checkout_process2': '',  # Check Out Behaviour2
                             'transaction_behaviour2': '',  # Transaction Behaviour2

                             # Code Type 3 Details
                             'ctype3': '00Nd0000005WYkX',  # Code Type3
                             'url3': '00Nd0000005WYjU',   # URL3
                             'code3': '00Nd0000005WYj5',   # Code3
                             'comment3': '00Nd0000005WYjB',  # Comments3
                             'rbid3': '00Nd0000007fJ3f',  # Recommended Bid3
                             'rbudget3': '00Nd0000007fJ4O',  # Recommended Budget3
                             'ga_setup3': '00Nd0000007fJ23',  # Is GS Setup3
                             'analytics_code3': '00Nd0000008MVDS',  # analytics_code3
                             'call_extension3': '',  # Created Call Extension3
                             'product_behaviour3': '',  # Product Behaviour3
                             'cartpage_behaviour3': '',  # Cart Page Behaviour3
                             'checkout_process3': '',  # Check Out Behaviour3
                             'transaction_behaviour3': '',  # Transaction Behaviour3

                             # Code Type 4 Details
                             'ctype4': '00Nd0000005WYkm',  # Code Type4
                             'url4': '00Nd0000005WYjZ',   # URL4
                             'code4': '00Nd0000005WYjA',   # Code4
                             'comment4': '00Nd0000005WYkI',  # Comments4
                             'rbid4': '00Nd0000007fJ44',  # Recommended Bid4
                             'rbudget4': '00Nd0000007fJ4Y',  # Recommended Budget4
                             'ga_setup4': '00Nd0000007fJ28',  # Is GS Setup4
                             'analytics_code4': '00Nd0000008MVDX',  # analytics_code1
                             'call_extension4': '',  # Created Call Extension4
                             'product_behaviour4': '',  # Product Behaviour4
                             'cartpage_behaviour4': '',  # Cart Page Behaviour4
                             'checkout_process4': '',  # Check Out Behaviour4
                             'transaction_behaviour4': '',  # Transaction Behaviour4

                             # Code Type 4 Details
                             'ctype5': '00Nd0000005WYl6',  # Code Type5
                             'url5': '00Nd0000005WYjo',   # URL5
                             'code5': '00Nd0000005WYiw',   # Code5
                             'comment5': '00Nd0000005WYkN',  # Comments5
                             'rbid5': '00Nd0000007fJ49',  # Recommended Bid5
                             'rbudget5': '00Nd0000007fJ4d',  # Recommended Budget5
                             'ga_setup5': '00Nd0000007fJ2D',  # Is GS Setup5
                             'analytics_code5': '00Nd0000008MVDc',  # analytics_code1
                             'call_extension5': '',  # Created Call Extension5
                             'product_behaviour5': '',  # Product Behaviour5
                             'cartpage_behaviour5': '',  # Cart Page Behaviour5
                             'checkout_process5': '',  # Check Out Behaviour5
                             'transaction_behaviour5': '',  # Transaction Behaviour5

                             'tag_via_gtm': '00Nd0000007esIr',
                             }

    PRODUCTION_TAG_LEADS_ARGS = {'first_name': 'first_name',
                                 'last_name': 'last_name',
                                 'tag_datepick': '00Nd0000005WYlL',  # TAG Appointment Date
                                 'setup_datepick': '00Nd0000005WYlL',  # Shopping Appointment Date
                                 'tag_primary_role': '00Nd0000005WayR',  # Role
                                 # Code Type 1 Details
                                 'ctype1': '00Nd0000005WYhJ',  # Code Type1
                                 'url1': '00Nd0000005WYhE',   # URL1
                                 'code1': '00Nd0000005WYh9',   # Code1
                                 'comment1': '00Nd0000005WZIe',  # Comments1
                                 'rbid1': '00Nd0000007fJ3V',  # Recommended Bid1
                                 'rbudget1': '00Nd0000007fJ4E',  # Recommended Budget1
                                 'ga_setup1': '00Nd0000007fIlH',  # Is GS Setup1
                                 'analytics_code1': '00Nd0000008MVDI',  # analytics_code1
                                 'call_extension1': '',  # Created Call Extension1
                                 'product_behaviour1': '',  # Product Behaviour1
                                 'cartpage_behaviour1': '',  # Cart Page Behaviour1
                                 'checkout_process1': '',  # Check Out Behaviour1
                                 'transaction_behaviour1': '',  # Transaction Behaviour1
                                 # Code Type 2 Details
                                 'ctype2': '00Nd0000005WYkS',  # Code Type2
                                 'url2': '00Nd0000005WYi9',   # URL2
                                 'code2': '00Nd0000005WYiv',   # Code2
                                 'comment2': '00Nd0000005WYjy',  # Comments2
                                 'rbid2': '00Nd0000007fJ3a',  # Recommended Bid2
                                 'rbudget2': '00Nd0000007fJ4J',  # Recommended Budget2
                                 'ga_setup2': '00Nd0000007fJ1y',  # Is GS Setup2
                                 'analytics_code2': '00Nd0000008MVDN',  # analytics_code2
                                 'call_extension2': '',  # Created Call Extension2
                                 'product_behaviour2': '',  # Product Behaviour2
                                 'cartpage_behaviour2': '',  # Cart Page Behaviour2
                                 'checkout_process2': '',  # Check Out Behaviour2
                                 'transaction_behaviour2': '',  # Transaction Behaviour2
                                 # Code Type 3 Details
                                 'ctype3': '00Nd0000005WYkX',  # Code Type3
                                 'url3': '00Nd0000005WYjU',   # URL3
                                 'code3': '00Nd0000005WYj5',   # Code3
                                 'comment3': '00Nd0000005WYjB',  # Comments3
                                 'rbid3': '00Nd0000007fJ3f',  # Recommended Bid3
                                 'rbudget3': '00Nd0000007fJ4O',  # Recommended Budget3
                                 'ga_setup3': '00Nd0000007fJ23',  # Is GS Setup3
                                 'analytics_code3': '00Nd0000008MVDS',  # analytics_code3
                                 'call_extension3': '',  # Created Call Extension3
                                 'product_behaviour3': '',  # Product Behaviour3
                                 'cartpage_behaviour3': '',  # Cart Page Behaviour3
                                 'checkout_process3': '',  # Check Out Behaviour3
                                 'transaction_behaviour3': '',  # Transaction Behaviour3
                                 # Code Type 4 Details
                                 'ctype4': '00Nd0000005WYkm',  # Code Type4
                                 'url4': '00Nd0000005WYjZ',   # URL4
                                 'code4': '00Nd0000005WYjA',   # Code4
                                 'comment4': '00Nd0000005WYkI',  # Comments4
                                 'rbid4': '00Nd0000007fJ44',  # Recommended Bid4
                                 'rbudget4': '00Nd0000007fJ4Y',  # Recommended Budget4
                                 'ga_setup4': '00Nd0000007fJ28',  # Is GS Setup4
                                 'analytics_code4': '00Nd0000008MVDX',  # analytics_code4
                                 'call_extension4': '',  # Created Call Extension4
                                 'product_behaviour4': '',  # Product Behaviour4
                                 'cartpage_behaviour4': '',  # Cart Page Behaviour4
                                 'checkout_process4': '',  # Check Out Behaviour4
                                 'transaction_behaviour4': '',  # Transaction Behaviour4
                                 # Code Type 4 Details
                                 'ctype5': '00Nd0000005WYl6',  # Code Type5
                                 'url5': '00Nd0000005WYjo',   # URL5
                                 'code5': '00Nd0000005WYiw',   # Code5
                                 'comment5': '00Nd0000005WYkN',  # Comments5
                                 'rbid5': '00Nd0000007fJ49',  # Recommended Bid5
                                 'rbudget5': '00Nd0000007fJ4d',  # Recommended Budget5
                                 'ga_setup5': '00Nd0000007fJ2D',  # Is GS Setup5
                                 'analytics_code5': '00Nd0000008MVDc',  # analytics_code5
                                 'call_extension5': '',  # Created Call Extension5
                                 'product_behaviour5': '',  # Product Behaviour5
                                 'cartpage_behaviour5': '',  # Cart Page Behaviour5
                                 'checkout_process5': '',  # Check Out Behaviour5
                                 'transaction_behaviour5': '',  # Transaction Behaviour5

                                 'tag_via_gtm': '00Nd0000007esIr',
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
