# -*- coding: utf-8 -*-
{
    'name': "Asterisk log",

    'summary': """
        Vos appels dans un seul clique""",

    'description': """
        Ce module permet de lister vos appels dans Asterisk ....
    """,

    'author': "MLMConseil",
    'website': "http://www.mlmconseil.dz",
    'sequence': 3,

    'category': 'Phone',
    'version': '0.1',

    'depends': ['base'],

    
    'data': [
        # 'security/ir.model.access.csv',
        'asterisk_log.xml',
		
    ],
    
    'demo': [
        'demo.xml',
    ],
    'installable': True,
    #'application': False,
    'auto_install': False,
}