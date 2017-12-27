# -*- coding: utf-8 -*-
{
    'name' : 'Attendance with fingerprint X302-S',
    'version' : '1.1',
    'summary': 'Send Invoices and Track Payments',
    'sequence': 30,
    'author': 'Bima Wijaya',
    'description': """
Syncrone fingerprint x302-s with ir cron.
    """,
    'category': 'Human resource',
    'website': '-',
    'depends' : ['hr_attendance'],
    'data': [
        'views/hr_employee.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
