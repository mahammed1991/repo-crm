
class SalesforceLeads(object):
    SANDBOX_BASIC_LEADS_ARGS = {'gref': '00Nd0000005WYgk',  # Full Name
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
                                'advertiser_name': '00NZ0000001X6y7',  # Advertiser Name
                                'first_name': 'first_name',  # First Name
                                'last_name': 'last_name',  # Last Name
                                'advertiser_location': '00Nd0000007es7U',  # Advertiser Location
                                'aemail': '00Nd0000005WcNw',  # Advertiser Email
                                'phone': '00Nd0000005WYgz',  # Advertiser phone
                                'company': 'company',  # Advertiser Company

                                # Webmaster Details
                                'fopt': '00Nd0000005WYgp',  # Webmaster First Name
                                'lopt': '00Nd0000005WYgu',  # Webmaster Last Name
                                'web_access': '00Nd0000007esIm',  # Web Access
                                'web_master_email': '00NZ0000001X6yC',  # Webmaster Email
                                'popt': '00Nd0000007esIc',  # Webmaster Phone
                                'change_lead_owner': '00Nd0000007elYB',    # Default value for Change Lead Owner

                                # Agency Details
                                'agency_name': '00NZ0000001XR8H',
                                'agency_email': '00NZ0000001XR8M',
                                'agency_phone': '00NZ0000001XR8R',
                                'agency_poc': '00NZ0000001Xdfh',

                                # Agency Unique Field
                                'agency_bundle': '00NZ0000001XIJB',

                                # Bundle Unique Field
                                'bundle_bundle': '00Nd0000007f4St',

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
                                   'cid': '00Nd0000005WYgV',  # Customer ID
                                   'language': '00Nd0000007clUn',  # Language
                                   'tzone': '00Nd0000005WYhT',  # Time Zone

                                   # Advertiser Details
                                   'advertiser_name': '00Nd0000007esJ1',  # Advertiser Name
                                   'advertiser_location': '00Nd0000007es7U',  # Advertiser Location
                                   'aemail': '00Nd0000005WcNw',  # Advertiser Email
                                   'phone': '00Nd0000005WYgz',  # Advertiser phone
                                   'company': 'company',  # Advertiser Company

                                   # Webmaster Details
                                   'fopt': '00Nd0000005WYgp',  # Webmaster First Name
                                   'lopt': '00Nd0000005WYgu',  # Webmaster Last Name
                                   'web_access': '00Nd0000007esIm',  # Web Access
                                   'web_master_email': '00Nd0000007esIh',  # Webmaster Email
                                   'popt': '00Nd0000007esIc',  # Webmaster Phone
                                   'change_lead_owner': '00Nd0000007elYB',   # Default value for Change Lead Owner

                                   # Agency Details
                                   'agency_name': '00Nd0000007fGgD',
                                   'agency_email': '00Nd0000007fGgI',
                                   'agency_phone': '00Nd0000007fGgN',
                                   'agency_poc': '00Nd0000007fIl7',

                                   # Agency Unique Field
                                   'agency_bundle': '00Nd0000007fIdD',

                                   # Bundle Unique Field
                                   'bundle_bundle': '00Nd0000007f4St',

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
                             'ga_setup1': '00NZ0000001Xdfm',  # Is GS Setup1
                             # Code Type 2 Details
                             'ctype2': '00Nd0000005WYkS',  # Code Type2
                             'url2': '00Nd0000005WYi9',   # URL2
                             'code2': '00Nd0000005WYiv',   # Code2
                             'comment2': '00Nd0000005WYjy',  # Comments2
                             'ga_setup2': '00NZ0000001Xdfm',  # Is GS Setup2
                             # Code Type 3 Details
                             'ctype3': '00Nd0000005WYkX',  # Code Type3
                             'url3': '00Nd0000005WYjU',   # URL3
                             'code3': '00Nd0000005WYj5',   # Code3
                             'comment3': '00Nd0000005WYjB',  # Comments3
                             'ga_setup3': '00NZ0000001Xdfm',  # Is GS Setup3
                             # Code Type 4 Details
                             'ctype4': '00Nd0000005WYkm',  # Code Type4
                             'url4': '00Nd0000005WYjZ',   # URL4
                             'code4': '00Nd0000005WYjA',   # Code4
                             'comment4': '00Nd0000005WYkI',  # Comments4
                             'ga_setup4': '00NZ0000001Xdfm',  # Is GS Setup4
                             # Code Type 5 Details
                             'ctype5': '00Nd0000005WYl6',  # Code Type5
                             'url5': '00Nd0000005WYjo',   # URL5
                             'code5': '00Nd0000005WYiw',   # Code5
                             'comment5': '00Nd0000005WYkN',  # Comments5
                             'ga_setup5': '00NZ0000001Xdfm',  # Is GS Setup5
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
                                 'ga_setup1': '00Nd0000007fIlH',  # Is GS Setup1
                                 # Code Type 2 Details
                                 'ctype2': '00Nd0000005WYkS',  # Code Type2
                                 'url2': '00Nd0000005WYi9',   # URL2
                                 'code2': '00Nd0000005WYiv',   # Code2
                                 'comment2': '00Nd0000005WYjy',  # Comments2
                                 'ga_setup2': '00Nd0000007fIlH',  # Is GS Setup2
                                 # Code Type 3 Details
                                 'ctype3': '00Nd0000005WYkX',  # Code Type3
                                 'url3': '00Nd0000005WYjU',   # URL3
                                 'code3': '00Nd0000005WYj5',   # Code3
                                 'comment3': '00Nd0000005WYjB',  # Comments3
                                 'ga_setup3': '00Nd0000007fIlH',  # Is GS Setup3
                                 # Code Type 4 Details
                                 'ctype4': '00Nd0000005WYkm',  # Code Type4
                                 'url4': '00Nd0000005WYjZ',   # URL4
                                 'code4': '00Nd0000005WYjA',   # Code4
                                 'comment4': '00Nd0000005WYkI',  # Comments4
                                 'ga_setup4': '00Nd0000007fIlH',  # Is GS Setup4
                                 # Code Type 4 Details
                                 'ctype5': '00Nd0000005WYl6',  # Code Type5
                                 'url5': '00Nd0000005WYjo',   # URL5
                                 'code5': '00Nd0000005WYiw',   # Code5
                                 'comment5': '00Nd0000005WYkN',  # Comments5
                                 'ga_setup5': '00Nd0000007fIlH',  # Is GS Setup5
                                 'tag_via_gtm': '00Nd0000007esIr',
                                 }
    SANDBOX_SHOPPING_ARGS = {'shop_primary_role': '00Nd0000005WayR',
                             'setup_datepick': '00Nd0000005WYlL',  # Shopping Appointment Date
                             'ctype1': '00Nd0000005WYhJ',  # Code Type Shopping
                             'comment1': '00Nd0000005WZIe',  # Comments1
                             'mc_id': '00Nd00000077T9o',  # MC-ID
                             'web_client_inventory': '00Nd00000077T9t',  # Web Inventory
                             'rbid': '00Nd00000077T9y',  # Recommended Bid1
                             'rbid2': '00Nd00000077T9y',  # Recommended Bid2
                             'rbid3': '00Nd00000077T9y',  # Recommended Bid3
                             'rbid4': '00Nd00000077T9y',  # Recommended Bid4
                             'rbid5': '00Nd00000077T9y',  # Recommended Bid5

                             'rbudget': '00Nd00000077TA3',  # Recommended Budget1
                             'rbudget2': '00Nd00000077TA3',  # Recommended Budget2
                             'rbudget3': '00Nd00000077TA3',  # Recommended Budget3
                             'rbudget4': '00Nd00000077TA3',  # Recommended Budget4
                             'rbudget5': '00Nd00000077TA3',  # Recommended Budget5

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
                                'rbid2': '00Nd00000077T9y',  # Recommended Bid2
                                'rbid3': '00Nd00000077T9y',  # Recommended Bid3
                                'rbid4': '00Nd00000077T9y',  # Recommended Bid4
                                'rbid5': '00Nd00000077T9y',  # Recommended Bid5

                                'rbudget': '00Nd00000077TA3',  # Recommended Budget1
                                'rbudget2': '00Nd00000077TA3',  # Recommended Budget2
                                'rbudget3': '00Nd00000077TA3',  # Recommended Budget3
                                'rbudget4': '00Nd00000077TA3',  # Recommended Budget4
                                'rbudget5': '00Nd00000077TA3',  # Recommended Budget5

                                'rbidmodifier': '00Nd00000077TA8',  # Recommended Mobile Bid Modifier
                                'shopping_url': '00Nd0000005WYhE',  # Shopping URL
                                'is_shopping_policies': '00Nd0000007esIw',  # Shopping policies
                                }
