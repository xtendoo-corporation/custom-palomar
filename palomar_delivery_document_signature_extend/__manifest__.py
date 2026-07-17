{
    "name": "Delivery Document Signature Extend",
    "summary": "Extend the delivery document signature to include NIF",
    "version": "17.0.1.0.0",
    "author": "Abraham Carrasco Molina, Xtendoo",
    "license": "AGPL-3",
    "website": "https://xtendoo.es",
    "category": "Warehouse",
    "depends": [
        "base",
        "stock",
        "web",
    ],
    "data": [
        "views/report_delivery_document.xml",
        "views/view_picking_form.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'palomar_delivery_document_signature_extend/static/src/views/fields/custom_signature_dialog.js',
            'palomar_delivery_document_signature_extend/static/src/views/fields/custom_signature_dialog.xml',
            'palomar_delivery_document_signature_extend/static/src/views/fields/signature_field_custom.js',
            'palomar_delivery_document_signature_extend/static/src/views/fields/signature_field_custom.xml',
        ]
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
