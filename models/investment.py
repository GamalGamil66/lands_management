from odoo import models, fields, api, _

class Investment(models.Model):
    _name = 'lm.investment'
    _description = 'الفرصة'
    # _rec_name = 'username'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char(string='الاسم', required=True)
    description = fields.Text(string='الوصف')
    activity_classification = fields.Char(string='تصنيف النشاط')
    main_sector_id = fields.Many2one('lm.main_sector', string='القطاع الرئيسي')
    sub_sector_id = fields.Many2one('lm.sub_sector', string='القطاع الفرعي')
    state = fields.Selection([
        ('draft', 'مسودة'),
        ('submitted', 'تم التقديم'),
        ('reviewed', 'تم المراجعة'),
        ('approved', 'تم الموافقة')],
        string='الحالة')
    #location
    governorate = fields.Char(string='المحافظة')
    district = fields.Char(string='المديرية')
    city = fields.Char(string='المدينة')
    neighborhood = fields.Char(string='الحي')
    street = fields.Char(string='الشارع')
    subunit = fields.Char(string='الوحدة')
    x_coordinates = fields.Char(string='إحداثيات X')
    y_coordinates = fields.Char(string='إحداثيات Y')
    product_ids = fields.One2many('lm.product', 'investment_id', string='المنتجات')
    # location_id = fields.Many2one('lm.location', string='الموقع')
    land_usage_ids = fields.One2many('lm.land_usage', 'investment_id', string='استخدام الأرض')

    #financials
    investment_cost = fields.Float(string='التكلفة الاستثمارية')
    equipment_value = fields.Float(string='قيمة المعدات')
    financials_currency_id = fields.Many2one('res.currency', string='العملة')

    lands_area_space = fields.Float(string='اجمالي مساحة الأراضي', compute='_compute_lands_area_space')
    @api.depends('land_usage_ids.area_m2')
    def _compute_lands_area_space(self):
        for record in self:
            record.lands_area_space = sum(usage.area_m2 for usage in record.land_usage_ids)

    # funding_sources_ids = fields.One2many('lm.funding_sources', 'investment_id', string='المصادر المالية')
    labor_ids = fields.One2many('lm.labor', 'investment_id', string='العمالة')
    time_line_ids = fields.One2many('lm.timeline', 'investment_id', string='الجدول الزمني')
    investor_id = fields.Many2one('lm.investor', string='المستثمر')

class Product(models.Model):
    _name = 'lm.product'
    _description = 'المنتج/الخدمة'
    # _rec_name = 'username'
    product_name = fields.Char(string='الاسم')
    unit = fields.Char(string='الوحدة')
    capacity = fields.Float(string='الطاقة الإنتاجية القصوى سنويًا')
    notes = fields.Text(string='ملاحظات')
    investment_id = fields.Many2one('lm.investment', string='الاستثمار')
    investment_request_id = fields.Many2one('lm.investment_request', string='طلب الاستثمار')

# class ProductUnit(models.Model):
#     _name = 'lm.product_unit'
#     _description = 'وحدة المنتج'
#     # _rec_name = 'username'
#     name = fields.Char(string='الاسم')
#     product_ids = fields.One2many('lm.product', 'unit_id', string='المنتجات')

# class Location(models.Model):
#     _name = 'lm.location'
#     _description = 'الموقع'
#     # _rec_name = 'username'
#     governorate = fields.Char(string='المحافظة')
#     district = fields.Char(string='المديرية')
#     city = fields.Char(string='المدينة')
#     neighborhood = fields.Char(string='الحي')
#     street = fields.Char(string='الشارع')
#     subunit = fields.Char(string='الوحدة')
#     x_coordinates = fields.Char(string='إحداثيات X')
#     y_coordinates = fields.Char(string='إحداثيات Y')
#     investment_id = fields.One2many('lm.investment', 'location_id', string='الاستثمارات')

class LandUsage(models.Model):
    _name = 'lm.land_usage'
    _description = 'استخدام الأرض'
    # _rec_name = 'username'
    use_type = fields.Char(string='الاستخدام')
    area_m2 = fields.Float(string='المساحة بالمتر المربع')
    note = fields.Text(string='ملاحظات')
    investment_id = fields.Many2one('lm.investment', string='الاستثمار')
    investment_request_id = fields.Many2one('lm.investment_request', string='طلب الاستثمار')

# class Financials(models.Model):
#     _name = 'lm.financials'
#     _description = 'المؤشرات المالية'
#     # _rec_name = 'username'
#     investment_cost = fields.Float(string='التكلفة الاستثمارية')
#     equipment_value = fields.Float(string='قيمة المعدات')
#     currency_id = fields.Many2one('res.currency', string='العملة')
#     investment_id = fields.Many2one('lm.investment', string='الاستثمار')

class FundingSources(models.Model):
    _name = 'lm.funding_sources'
    _description = 'المصادر المالية'
    # _rec_name = 'username'
    funding_type = fields.Selection([
        ('self_funding', 'التمويل الذاتي'),
        ('loan_funding', 'تمويل القروض'),
        ('bank_facility', 'التسهيلات البنكية'),
        ('other_funding', 'تمويل آخر'),
        ('total_funding', 'إجمالي التمويل')
    ], string='المصدر')
    local_amount = fields.Float(string='المبلغ المحلي')
    foreign_amount = fields.Float(string='المبلغ الأجنبي')
    currency_id = fields.Many2one('res.currency', string='العملة')
    subtotal = fields.Float(string='المجموع الفرعي', compute='_compute_subtotal')
    # investment_id = fields.Many2one('lm.investment', string='الاستثمار')
    investment_request_id = fields.Many2one('lm.investment_request', string='طلب الاستثمار')

    @api.depends('local_amount', 'foreign_amount')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.local_amount + record.foreign_amount

class Labor(models.Model):
    _name = 'lm.labor'
    _description = 'العمالة'
    # _rec_name = 'username'
    type = fields.Selection([
        ('local', 'محلي'),
        ('foreign', 'أجنبي')
    ], string='النوع', required=True)
    category = fields.Selection([
        ('administrative', 'إداري'),
        ('technical', 'فني'),
        ('other', 'آخر')
    ], string='الفئة')
    count = fields.Integer(string='العدد')
    #currency_id = fields.Many2one('res.currency', string='العملة')
    notes = fields.Text(string='ملاحظات')
    specialization = fields.Char(string='التخصص')
    nationality = fields.Many2one('res.country', string='الجنسية')
    duration = fields.Char(string='المدة')
    investment_id = fields.Many2one('lm.investment', string='الاستثمار')
    investment_request_id = fields.Many2one('lm.investment_request', string='طلب الاستثمار')

class Timeline(models.Model):
    _name = 'lm.timeline'
    _description = 'الجدول الزمني'
    # _rec_name = 'username'
    task_name = fields.Char(string='اسم المهمة', required=True)
    duration_days = fields.Integer(string='المدة (بالأيام)')
    note = fields.Text(string='ملاحظات')
    investment_id = fields.Many2one('lm.investment', string='الاستثمار')
    investment_request_id = fields.Many2one('lm.investment_request', string='طلب الاستثمار')

class MainSector(models.Model):
    _name = 'lm.main_sector'
    _description = 'القطاع الرئيسي'
    # _rec_name = 'username'
    name = fields.Char(string='الاسم', required=True)
    investment_ids = fields.One2many('lm.investment', 'main_sector_id', string='الاستثمارات')
    investment_request_ids = fields.One2many('lm.investment_request', 'main_sector_id', string='طلبات الاستثمار')
class SubSector(models.Model):
    _name = 'lm.sub_sector'
    _description = 'القطاع الفرعي'
    # _rec_name = 'username'
    name = fields.Char(string='الاسم', required=True)
    main_sector_id = fields.Many2one('lm.main_sector', string='القطاع الرئيسي')
    investment_ids = fields.One2many('lm.investment', 'sub_sector_id', string='الاستثمارات')
    investment_request_ids =fields.One2many('lm.investment_request', 'sub_sector_id', string='طلبات الاستثمار')