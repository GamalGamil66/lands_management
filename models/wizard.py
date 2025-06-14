from odoo import models, fields, api, _


class DeliveryReportWizard(models.TransientModel):
    _name = 'delivery.report.wizard'
    _description = 'Wizard: Create Delivery Report'

    investment_request_id = fields.Many2one('lm.investment_request', string='Investment Request', required=True)
    name = fields.Char(string='Name', default=lambda self: _('Delivery Report'))

    def action_create(self):
        self.ensure_one()
        delivery_report = self.env['lm.delivery_report'].create({
            'name': self.name,
            'investment_request_ids': self.investment_request_id,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': _('Delivery Report'),
            'res_model': 'lm.delivery_report',
            'view_mode': 'form',
            'res_id': delivery_report.id,
            'target': 'current'
        }


class EvaluationReportWizard(models.TransientModel):
    _name = 'evaluation.report.wizard'
    _description = 'Wizard: Create Evaluation Report'

    investment_request_id = fields.Many2one('lm.investment_request', string='Investment Request', required=True)
    name = fields.Char(string='Name', default=lambda self: _('Evaluation Report'))

    def action_create(self):
        self.ensure_one()
        evaluation_report = self.env['lm.evaluation_report'].create({
            'name': self.name,
            'investment_request_ids': self.investment_request_id,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': _('Evaluation Report'),
            'res_model': 'lm.evaluation_report',
            'view_mode': 'form',
            'res_id': evaluation_report.id,
            'target': 'current'
        }


class ProjectFollowupReportWizard(models.TransientModel):
    _name = 'project.followup.report.wizard'
    _description = 'Wizard: Create Project Follow-up Report'

    investment_request_id = fields.Many2one('lm.investment_request', string='Investment Request', required=True)
    name = fields.Char(string='Name', default=lambda self: _('Project Follow-up Report'))

    def action_create(self):
        self.ensure_one()
        followup_report = self.env['project.followup.report'].create({
            'name': self.name,
            'investment_request_ids': self.investment_request_id,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': _('Project Follow-up Report'),
            'res_model': 'project.followup.report',
            'view_mode': 'form',
            'res_id': followup_report.id,
            'target': 'current'
        }


class ContractWizard(models.TransientModel):
    _name = 'contract.wizard'
    _description = 'Wizard: Create Contract'

    investment_request_id = fields.Many2one('lm.investment_request', string='Investment Request', required=True)
    name = fields.Char(string='Name', default=lambda self: _('Contract'))

    def action_create(self):
        self.ensure_one()
        contract = self.env['lm.contract'].create({
            'name': self.name,
            'investment_request_ids': self.investment_request_id,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': _('Contract'),
            'res_model': 'lm.contract',
            'view_mode': 'form',
            'res_id': contract.id,
            'target': 'current'
        }
