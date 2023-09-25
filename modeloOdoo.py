#-*- coding: utf-8 -*-

## Questão 3 ##
from odoo import api, models, fields, _

## Tarefa 1 ##
class AccountForeignExchangeRate(models.Model):
    _name = 'account.foreign.exchange.rate'
    _description = "account.foreign.exchange.rate"

    date = fields.Date(string="Data taxa", help="Data em que a taxa deve ser aplicada")
    currency_from_id = fields.Many2one('res.currency', string="Moeda Origem", help="Moeda da qual converte-se o valor original")
    currency_to_id = fields.Many2one('res.currency', string="Moeda Destino", help="Moeda para qual o valor original deve ser convertido")
    exchange_rate = fields.float(string="Taxa", help="Taxa de conversão")

## Tarefa 2 ##
class AccountMove(models.Model):
    _name_ = 'account.move'
    _inherit = "account.move"

    currency_id = fields.Many2one('res.currency',
                                  string="Moeda",
                                  help="Moeda representada pelo valor da transação")

## Tarefa 3 ##
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('currency_id', self.company_id.currency_id.id) <> self.company_id.currency_id.id:
                taxa = self.env['account.foreign.exchange.rate'].search([('currency_from_id', '=', self.currency_id.id),
                                                                         ('currency_to_id', '=',
                                                                          self.company_id.currency_id.id),
                                                                         ('date', '<=', fields.Date.today())],
                                                                        order='date'
                                                                        )
                if taxa:
                    value = vals.get('value', 0) * taxa[len(taxa)-1].exchange_rate
                    vals.update({'currency_id': self.company_id.currency_id.id,
                                 'value': value })
        return super(AccountMove, self).create(vals_list)