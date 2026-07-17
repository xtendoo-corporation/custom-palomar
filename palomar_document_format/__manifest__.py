{
    "name": "Palomar Document Format",
    "summary": "Muestra la cuenta bancaria en la factura y el presupuesto/pedido "
    "solo cuando la forma de pago es una transferencia.",
    "version": "17.0.1.0.0",
    "category": "Accounting",
    "author": "Xtendoo (https://xtendoo.es)",
    "website": "https://xtendoo.es",
    "license": "AGPL-3",
    "depends": [
        "account",
        "account_payment_partner",
        "sale",
        "account_payment_sale",
    ],
    "data": [
        "views/report_invoice_document.xml",
        "views/report_saleorder_document.xml",
    ],
    "installable": True,
    "auto_install": False,
}
