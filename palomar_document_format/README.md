# Palomar Document Format

Módulo de personalización de los informes de impresión (factura y
presupuesto/pedido de venta) para Palomar.

## Factura

Hereda la plantilla QWeb `account.report_invoice_document` y modifica el bloque
de cuenta bancaria que el core de Odoo renderiza dentro del nodo
`<p name="payment_communication">` (el que aparece junto a "Comunicaciones de
pago").

La cuenta bancaria de la empresa (`o.partner_bank_id`) **solo se imprime cuando
la forma de pago de la factura contiene la palabra "transferencia"** (comparación
insensible a mayúsculas/minúsculas).

La forma de pago se evalúa sobre `o.payment_mode_id`, campo aportado por el
módulo OCA `account_payment_partner`.

## Presupuesto / pedido de venta

Hereda `sale.report_saleorder_document` y añade, justo después de las condiciones
del documento, el bloque:

```
Transferencias:
ES29 0049 0107 6828 1027 4592 BANCO SANTANDER
```

Ese bloque **solo se imprime cuando la forma de pago del pedido contiene la
palabra "transferencia"**. La forma de pago se evalúa sobre `doc.payment_mode_id`
(campo aportado por el módulo OCA `account_payment_sale`).

> **Importante (configuración en producción):** el texto de transferencias venía
> hasta ahora de los **Términos y condiciones por defecto de venta**
> (Ajustes → Ventas), que es un campo de texto estático y por eso se imprimía
> siempre. Para que la condición funcione hay que **retirar esas líneas del
> campo de términos** (y de los presupuestos existentes que ya lo tengan
> copiado en su campo de condiciones). A partir de ahí, este módulo se encarga
> de imprimirlo solo cuando corresponde.

### Casos

| Forma de pago              | ¿Se muestra la cuenta bancaria? |
| -------------------------- | ------------------------------- |
| `Transferencia bancaria`   | Sí                              |
| `Recibo domiciliado`       | No                              |
| Sin forma de pago definida | No                              |

## Detalles técnicos

- La factura usa `position="attributes"` sobre el nodo original (**no se elimina
  el nodo**, solo se reemplaza su `t-if`).
- El informe de venta añade el bloque con `position="after"` sobre el nodo
  `order_note`.
- Ambas herencias se aplican con `priority="99"` para asegurar que se añaden por
  encima de otras herencias activas de los mismos informes.

## Instalación

1. Actualizar la lista de aplicaciones.
2. Instalar **Palomar Document Format** (`palomar_document_format`).
3. Retirar el bloque "Transferencias: ES29..." de los Términos y condiciones por
   defecto de venta.
4. Imprimir una factura y un presupuesto para verificar el comportamiento.

## Dependencias

- `account`
- `account_payment_partner` (OCA)
- `sale`
- `account_payment_sale` (OCA)

## Licencia

AGPL-3
