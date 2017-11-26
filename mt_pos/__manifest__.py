# -*- coding: utf-8 -*-
{
    'name': "POS Password Restriction For Discount & Lock POS Screen",

    'summary': """
	1. Password Registration For Point Of Sale Config
	2. Lock POS Front-End Screen with Custom Pop-ups
	3. Discount Permission in POS-Front-End
	""",

    'description': """
    """,

    'author': "Bite Pue MM Team, Myanmar",
    'category': 'Point Of Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','point_of_sale'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}
