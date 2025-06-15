from odoo import models, fields, api, _

class InvestmentRequest(models.Model):
    _name = 'lm.investment_request'
    _description = 'طلب استثمار'
    _rec_name = 'investment_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    request_date = fields.Date(string='تاريخ الطلب', required=True, default=fields.Datetime.now)
    request_type = fields.Selection([
        ('chance', 'فرصة'),
        ('project', 'مشروع'),],
        string='نوع الطلب', default='project')
    # investment_id = fields.Many2one('lm.investment', string='الاستثمار', required=True)
    # investor_id = fields.Many2one('lm.investor', string='المستثمر', required=True)
    funding_sources_ids = fields.One2many('lm.funding_sources', 'investment_request_id', string='المصادر المالية')

    investment_name = fields.Char(string='اسم الفرصة', required=True)
    description = fields.Text(string='الوصف')
    activity_classification = fields.Char(string='تصنيف النشاط')
    main_sector_id = fields.Many2one('lm.main_sector', string='القطاع الرئيسي')
    sub_sector_id = fields.Many2one('lm.sub_sector', string='القطاع الفرعي')
    state = fields.Selection([
        ('draft', 'مسودة'),
        ('confirmed', 'تم التأكيد'),
        ('reviewed', 'تم المراجعة'),
        ('first_submitted', 'تسليم اولي'),
        ('followed_up','تم المتابعة'),
        ('contracted', 'تم العقد'),
        ('evaluated','تم التقييم'),
        ('cancelled', 'تم الالغاء'),
        ('rejected', 'تم الرفض')],
         string='الحالة',default="draft")
    #location
    governorate = fields.Char(string='المحافظة')
    district = fields.Char(string='المديرية')
    city = fields.Char(string='المدينة')
    neighborhood = fields.Char(string='الحي')
    street = fields.Char(string='الشارع')
    subunit = fields.Char(string='الوحدة')
    x_coordinates = fields.Char(string='إحداثيات X')
    y_coordinates = fields.Char(string='إحداثيات Y')
    product_ids = fields.One2many('lm.product', 'investment_request_id', string='المنتجات')
    # location_id = fields.Many2one('lm.location', string='الموقع')
    land_usage_ids = fields.One2many('lm.land_usage', 'investment_request_id', string='استخدام الأرض')

    #financials
    investment_cost = fields.Float(string='التكلفة الاستثمارية')
    equipment_value = fields.Float(string='قيمة المعدات')
    financials_currency_id = fields.Many2one('res.currency', string='العملة')
    
    lands_area_space = fields.Float(string='اجمالي مساحة الأراضي', compute='_compute_lands_area_space')
    @api.depends('land_usage_ids.area_m2')
    def _compute_lands_area_space(self):
        for record in self:
            record.lands_area_space = sum(usage.area_m2 for usage in record.land_usage_ids)
            
    # funding_sources_ids = fields.One2many('lm.funding_sources', 'investment_request_id', string='المصادر المالية')
    labor_ids = fields.One2many('lm.labor', 'investment_request_id', string='العمالة')
    time_line_ids = fields.One2many('lm.timeline', 'investment_request_id', string='الجدول الزمني')
    investor_id = fields.Many2one('lm.investor', string='المستثمر')

    investor_name = fields.Char(string='اسم المستثمر', required=True)
    legal_form = fields.Selection([
        ('sole_proprietorship', 'ملكية فردية'),
        ('partnership', 'شراكة'),
        ('limited_liability_company', 'شركة ذات مسؤولية محدودة'),
        ('public_company', 'شركة مساهمة')],
        string='الشكل القانوني')
    nationality = fields.Many2one('res.country', string='الجنسية')
    commercial_reg = fields.Char(string='السجل التجاري')
    id_number = fields.Char(string='رقم الهوية', unique=True)
    address = fields.Text(string='العنوان')
    phone = fields.Char(string='الهاتف')
    mobile = fields.Char(string='الجوال')
    email = fields.Char(string='البريد الإلكتروني')
    website = fields.Char(string='الموقع الإلكتروني')
    po_box = fields.Char(string='صندوق البريد')

    evaluation_report_id = fields.Many2one('lm.evaluation_report', string='تقرير تقييم')
    followup_report_id = fields.Many2one('project.followup.report', string='تقرير متابعة')
    contract_id = fields.Many2one('lm.contract', string='عقد')
    delivery_report_id = fields.Many2one('lm.delivery_report', string='تقرير تسليم')
    land_request_review_id = fields.Many2one('land.request.review', string='تقرير مراجعة طلب الأراضي')


    def action_confirm(self):
        for rec in self:
            print("dd")
            rec.state = 'reviewed'
    def action_cancel(self):
        for rec in self:
            print("dd")
            rec.state = 'draft'
    def action_review(self):
        print("dd")
    def action_first_submit(self):
        print("dd")
    def action_follow_up(self):
        print("dd")
    def action_contract(self):
        print("dd")
    def action_evaluate(self):
        print("dd")
    def action_view_first_submit(self):
        #open report
        return self.env.ref('lands_management.action_print_investment_request').report_action(self)

    def action_delivery_report_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Delivery Report Wizard',
            'res_model': 'delivery.report.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_investment_request_id': self.id},
        }
    
    def action_evaluation_report_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Evaluation Report Wizard',
            'res_model': 'evaluation.report.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_investment_request_id': self.id},
        }
    
    def action_project_followup_report_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Project Followup Report Wizard',
            'res_model': 'project.followup.report.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_investment_request_id': self.id},
        }
    
    def action_contract_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Contract Wizard',
            'res_model': 'contract.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_investment_request_id': self.id},
        }
    def action_land_request_review_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Land Request Review Wizard',
            'res_model': 'land.request.review.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_investment_request_id': self.id},
        }

    def open_contract(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Contract',
            'res_model': 'lm.contract',
            'res_id': self.contract_id.id,
            'view_mode': 'form',
            'target': 'current'
        }
    def open_delivery_report(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Delivery Report',
            'res_model': 'lm.delivery_report',
            'res_id': self.delivery_report_id.id,
            'view_mode': 'form',
            'target': 'current'
        }
    
    def open_evaluation_report(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Evaluation Report',
            'res_model': 'lm.evaluation_report',
            'res_id': self.evaluation_report_id.id,
            'view_mode': 'form',
            'target': 'current'
        }

    def open_project_followup_report(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Project Followup Report',
            'res_model': 'lm.project_followup_report',
            'res_id': self.followup_report_id.id,
            'view_mode': 'form',
            'target': 'current'
        }
    
    def open_land_request_review(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Land Request Review',
            'res_model': 'land.request.review',
            'res_id': self.land_request_review_id.id,
            'view_mode': 'form',
            'target': 'current'
        }