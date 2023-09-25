# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from odoo import models, fields, api, _
import json, requests

class AccountInvoiceIntegration(models.Model):
    _name = "account.invoice.integration"
    _description = "account.invoice.integration"

    invoice_id = fields.Many2one('account.invoice', string='Pedido')
    external_system_id = fields.Char(string='ID Externo')
    state = fields.Selection([('pendente', 'Pendente'), ('sucesso', 'Sucesso'), ('erro', 'Erro'),],
                             string='Status',
                             readonly=True, default='pendente')
    response_message = fields.Text(string='Mensagem')

class AccountMove(models.Model):
    _name = "account.move"
    _description = "account.move"

    _inherit = "account.move"

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled')
    ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')

    integration_ids = fields.One2many('account.invoice.integration', 'invoice_id',
                                      string='Integração')

    @api.constrains('state')
    def integra_api_externa_quando_confirma(self):
        for invoice in self.invoice_id:
            if invoice.state == 'posted':
                if invoice.integration_ids and invoice.integration_ids[0].state == 'sucesso':
                    break
                response = requests.post('127.0.0.1:5000/gerafatura', json=invoice.__dict__)
                response_status = 'sucesso' if response.status_code == 200 else 'erro'
                content = json.loads(response.content)
                if invoice.integration_ids:
                    invoice.integration_ids[0].status = response_status
                    invoice.integration_ids[0].response_message = response.text
                else:
                    invoice.integration_ids.create({'invoice_id': invoice.id,
                                                    'external_system_id': int(content['id']),
                                                    'state': response_status,
                                                    'response_message': response.text})
        pass
