# -*- coding: utf-8 -*-
{
    'name': 'Screen configuration',
    'version': '2.0',
    'category': 'Point of Sale',
    'sequence': 6,
    'author': 'Bima Wijaya',
    'summary': 'screen configuration',
    'description': """
Add POS configuration to show or hide price on POS screen. 
""",
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_view.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    'installable': True,
}
