{
    "name": "Palomar Filter Invoice",
    "summary": "Palomar Filter Invoice",
    "version": "17.0.1.0.0",
    "description": "Palomar Filter Invoice",
    "company": "Xtendoo",
    "website": "http://www.xtendoo.es",
    "depends": [
        'sale',
        'base',
        'account',
    ],
    "license": "AGPL-3",
    "data": [
        'views/account_move.xml',
    ],
    'post_init_hook': 'post_init_hook',
    "installable": True,
}
