from inspect import signature
from xmlrpc.client import DateTime
from typing_extensions import Required
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
        string='الحالة')
    # investment_id = fields.Many2one('lm.investment', string='الاستثمار', required=True)
    # investor_id = fields.Many2one('lm.investor', string='المستثمر', required=True)
    funding_sources_ids = fields    .One2many('lm.funding_sources', 'investment_request_id', string='المصادر المالية')

    investment_name = fields.Char(string='اسم الفرصة', required=True)
    description = fields.Text(string='الوصف')
    activity_classification = fields.Char(string='تصنيف النشاط')
    main_sector_id = fields.Many2one('lm.main_sector', string='القطاع الرئيسي')
    sub_sector_id = fields.Many2one('lm.sub_sector', string='القطاع الفرعي')
    state = fields.Selection([
        ('draft', 'مسودة'),
        ('first_reviewed', 'مراجعة'),
        ('first_submitted', 'تسليم اولي'),
        ('second_reviewed','تقييم'),
        ('contracted', 'تم العقد'),
        ('cancelled', 'تم الالغاء')],
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


    def action_confirm(self):
        for rec in self:
            print("dd")
            rec.state = 'first_reviewed'
    def cans_confirm(self):
        for rec in self:
            print("dd")
            rec.state = 'draft'
    def action_first_review(self):
        print("dd")
    def action_first_submit(self):
        print("dd")