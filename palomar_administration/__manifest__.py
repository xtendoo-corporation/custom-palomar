{
    "name": "Palomar Administration",
    "summary": "Administración de Palomar",
    "version": "17.0.1.0.0",
    "description": "Administración de Palomar",
    "company": "Xtendoo",
    "website": "http://www.xtendoo.es",
    "depends": [
        'sale',
        'base',
        'sale_margin',
        'product',
        'product_standard_margin',
    ],
    "license": "AGPL-3",
    "data": [
        "security/security_group.xml",
        "views/sale_order_view.xml",
        "views/product_view.xml",
        "views/account_move_report.xml",
        "views/account_move_views.xml",
    ],
    "installable": True,
}
