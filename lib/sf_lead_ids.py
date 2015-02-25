
class SalesforceLeads(object):
    SANDBOX_BASIC_LEADS_ARGS = {'gref': '00Nd0000005WYgk',  # Full Name
                                'emailref': 'email',  # Rep Email
                                'manager_name': '00Nd00000075Crj',  # Manager Name
                                'manager_email': '00Nd00000077r3s',  # Manager Email
                                'team': '00Nd0000005XIWB',  # Team
                                'service_segment': '00Nd0000007e2AF',  # Service Segment
                                'g_cases_id': '00Nd0000007dWIH',  # G Cases Id
                                'country': '00Nd0000005WYga',  # Country
                                'aemail': '00Nd0000005WcNw',  # Advertiser Email
                                'phone': '00Nd0000005WYgz',  # Advertiser phone
                                'company': 'company',  # Advertiser Company
                                'cid': '00Nd0000005WYgV',  # Customer ID
                                'language': '00Nd0000007clUn',  # Language
                                'tzone': '00Nd0000005WYhT',  # Time Zone
                                # Sandbox ID's
                                'advertiser_name': '00NZ0000001X6y7',  # Advertiser Name
                                'first_name': 'first_name',  # First Name
                                'last_name': 'last_name',  # Last Name
                                'advertiser_location': '00Nd0000007es7U',  # Advertiser Location
                                'web_access': '00Nd0000007esIm',  # Web Access
                                'web_master_email': '00NZ0000001X6yC',  # Webmaster Email
                                'popt': '00Nd0000007esIc',  # Webmaster Phone
                                # Webmaster Details
                                'fopt': '00Nd0000005WYgp',  # Webmaster First Name
                                'lopt': '00Nd0000005WYgu',  # Webmaster Last Name
                                'change_lead_owner': '00Nd0000007elYB',    # Default value for Change Lead Owner
                                'Campaign_ID': 'Campaign_ID',
                                'oid': 'oid',
                                '__VIEWSTATE': '__VIEWSTATE',
                                }

    PRODUCTION_BASIC_LEADS_ARGS = {'gref': '00Nd0000005WYgk',  # Full Name
                                   'emailref': 'email',  # Rep Email
                                   'manager_name': '00Nd00000075Crj',  # Manager Name
                                   'manager_email': '00Nd00000077r3s',  # Manager Email
                                   'team': '00Nd0000005XIWB',  # Team
                                   'service_segment': '00Nd0000007e2AF',  # Service Segment
                                   'g_cases_id': '00Nd0000007dWIH',  # G Cases Id
                                   'country': '00Nd0000005WYga',  # Country
                                   'aemail': '00Nd0000005WcNw',  # Advertiser Email
                                   'phone': '00Nd0000005WYgz',  # Advertiser phone
                                   'company': 'company',  # Advertiser Company
                                   'cid': '00Nd0000005WYgV',  # Customer ID
                                   'language': '00Nd0000007clUn',  # Language
                                   'tzone': '00Nd0000005WYhT',  # Time Zone
                                   # Production ID's
                                   'advertiser_name': '00Nd0000007esJ1',  # Advertiser Name
                                   'advertiser_location': '00Nd0000007es7U',  # Advertiser Location
                                   'web_access': '00Nd0000007esIm',  # Web Access
                                   'web_master_email': '00Nd0000007esIh',  # Webmaster Email
                                   'popt': '00Nd0000007esIc',  # Webmaster Phone
                                   'change_lead_owner': '00Nd0000007elYB',   # Default value for Change Lead Owner
                                   # Webmaster Details
                                   'fopt': '00Nd0000005WYgp',  # Webmaster First Name
                                   'lopt': '00Nd0000005WYgu',  # Webmaster Last Name
                                   'Campaign_ID': 'Campaign_ID',
                                   'oid': 'oid',
                                   '__VIEWSTATE': '__VIEWSTATE',
                                   }
    SANDBOX_TAG_LEAD_ARGS = {'tag_datepick': '00Nd0000005WYlL',  # TAG Appointment Date
                             'tag_primary_role': '00Nd0000005WayR',  # Role
                             # Code Type 1 Details
                             'ctype1': '00Nd0000005WYhJ',  # Code Type1
                             'url1': '00Nd0000005WYhE',   # URL1
                             'code1': '00Nd0000005WYh9',   # Code1
                             'comment1': '00Nd0000005WZIe',  # Comments1
                             # Code Type 2 Details
                             'ctype2': '00Nd0000005WYkS',  # Code Type2
                             'url2': '00Nd0000005WYi9',   # URL2
                             'code2': '00Nd0000005WYiv',   # Code2
                             'comment2': '00Nd0000005WYjy',  # Comments2
                             # Code Type 3 Details
                             'ctype3': '00Nd0000005WYkX',  # Code Type3
                             'url3': '00Nd0000005WYjU',   # URL3
                             'code3': '00Nd0000005WYj5',   # Code3
                             'comment3': '00Nd0000005WYjB',  # Comments3
                             # Code Type 4 Details
                             'ctype4': '00Nd0000005WYkm',  # Code Type4
                             'url4': '00Nd0000005WYjZ',   # URL4
                             'code4': '00Nd0000005WYjA',   # Code4
                             'comment4': '00Nd0000005WYkI',  # Comments4
                             # Code Type 4 Details
                             'ctype5': '00Nd0000005WYl6',  # Code Type4
                             'url5': '00Nd0000005WYjo',   # URL4
                             'code5': '00Nd0000005WYiw',   # Code4
                             'comment5': '00Nd0000005WYkN',  # Comments4
                             'tag_via_gtm': '00Nd0000007esIr',
                             }
    PRODUCTION_TAG_LEADS_ARGS = {'first_name': 'first_name',
                                 'last_name': 'last_name',
                                 'tag_datepick': '00Nd0000005WYlL',  # TAG Appointment Date
                                 'tag_primary_role': '00Nd0000005WayR',  # Role
                                 # Code Type 1 Details
                                 'ctype1': '00Nd0000005WYhJ',  # Code Type1
                                 'url1': '00Nd0000005WYhE',   # URL1
                                 'code1': '00Nd0000005WYh9',   # Code1
                                 'comment1': '00Nd0000005WZIe',  # Comments1
                                 # Code Type 2 Details
                                 'ctype2': '00Nd0000005WYkS',  # Code Type2
                                 'url2': '00Nd0000005WYi9',   # URL2
                                 'code2': '00Nd0000005WYiv',   # Code2
                                 'comment2': '00Nd0000005WYjy',  # Comments2
                                 # Code Type 3 Details
                                 'ctype3': '00Nd0000005WYkX',  # Code Type3
                                 'url3': '00Nd0000005WYjU',   # URL3
                                 'code3': '00Nd0000005WYj5',   # Code3
                                 'comment3': '00Nd0000005WYjB',  # Comments3
                                 # Code Type 4 Details
                                 'ctype4': '00Nd0000005WYkm',  # Code Type4
                                 'url4': '00Nd0000005WYjZ',   # URL4
                                 'code4': '00Nd0000005WYjA',   # Code4
                                 'comment4': '00Nd0000005WYkI',  # Comments4
                                 # Code Type 4 Details
                                 'ctype5': '00Nd0000005WYl6',  # Code Type4
                                 'url5': '00Nd0000005WYjo',   # URL4
                                 'code5': '00Nd0000005WYiw',   # Code4
                                 'comment5': '00Nd0000005WYkN',  # Comments4
                                 'tag_via_gtm': '00Nd0000007esIr',
                                 }
    SANDBOX_SHOPPING_ARGS = {'shop_primary_role': '00Nd0000005WayR',
                             'setup_datepick': '00Nd0000005WYlL',  # Shopping Appointment Date
                             'ctype1': '00Nd0000005WYhJ',  # Code Type Shopping
                             'mc_id': '00Nd00000077T9o',  # MC-ID
                             'web_client_inventory': '00Nd00000077T9t',  # Web Inventory
                             'rbid': '00Nd00000077T9y',  # Recommended Bid
                             'rbudget': '00Nd00000077TA3',  # Recommended Budget
                             'rbidmodifier': '00Nd00000077TA8',  # Recommended Mobile Bid Modifier
                             'shopping_url': '00Nd0000005WYhE',  # Shopping URL
                             'is_shopping_policies': '00Nd0000007esIw',  # Shopping policies
                             }
    PRODUCTION_SHOPPING_ARGS = {'shop_primary_role': '00Nd0000005WayR',
                                'setup_datepick': '00Nd0000005WYlL',  # Shopping Appointment Date
                                'ctype1': '00Nd0000005WYhJ',  # Code Type Shopping
                                'mc_id': '00Nd00000077T9o',  # MC-ID
                                'web_client_inventory': '00Nd00000077T9t',  # Web Inventory
                                'rbid': '00Nd00000077T9y',  # Recommended Bid
                                'rbudget': '00Nd00000077TA3',  # Recommended Budget
                                'rbidmodifier': '00Nd00000077TA8',  # Recommended Mobile Bid Modifier
                                'shopping_url': '00Nd0000005WYhE',  # Shopping URL
                                'is_shopping_policies': '00Nd0000007esIw',  # Shopping policies
                                }
