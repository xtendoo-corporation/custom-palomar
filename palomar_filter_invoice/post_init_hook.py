from odoo import api, models


def post_init_hook(env):
    # Usamos el cursor de la base de datos del entorno
    cr = env.cr

    # Ejecutar la consulta SQL directamente
    cr.execute("""
        UPDATE account_move
        SET in_payment_line = TRUE
        WHERE id IN (
            SELECT DISTINCT aml.move_id
            FROM account_payment_line apl
            JOIN account_move_line aml ON aml.id = apl.move_line_id
            JOIN account_payment_order apo ON apo.id = apl.order_id
            WHERE apo.state NOT IN ('draft', 'cancel')
        )
    """)
