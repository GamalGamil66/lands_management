from odoo import models, fields, api

class DeliveryReport(models.Model):
    _name = 'lm.delivery_report'
    _description = 'محضر التسليم'
    name = fields.Char("الاسم")
    preparatory_task_ids = fields.One2many('lm.preparatory_task', 'delivery_report_id', string='الأعمال التحضيرية')

    investment_request_ids = fields.One2many('lm.investment_request', 'delivery_report_id', string='طلبات الاستثمار')

    state = fields.Selection([
        ('draft', 'مسودة'),
        ('confirmed', 'تم التأكيد')],
         string='الحالة',default="draft")
    
    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'
            record.investment_request_ids.write({'state': 'first_submitted'})

class PreparatoryTask(models.Model):
    _name = 'lm.preparatory_task'
    _description = 'الأعمال التحضيرية المطلوبة من المستثمر (محضر التسليم)'
    _order = 'sequence, id'

    sequence = fields.Integer(string='م', default=10)
    description = fields.Text(string='الوصف', required=True) # 
    duration_weeks = fields.Integer(string='المدة الزمنية اللازمة (أسابيع)') # 
    task_type = fields.Selection([
        ('technical_soil_test', 'اعمال فنية لاختبار التربة وفحصها'),
        ('technical_engineering_plans', 'اعداد المخططات الفنية/الهندسية'),
        ('feasibility_study', 'اعداد دراسة الجدوى الاقتصادية'),
        ('environmental_impact_study', 'اعداد دراسة تقييم الأثر البيئي'),
        ('investment_license_period', 'فترة الحصول على ترخيص المشروع'),
        ('other_works', 'اعمال اخرى تحدد')
    ], string='نوع المهمة', required=True)
    other_work = fields.Char(string='تفاصيل العمل الاخر') # 
    notes = fields.Text(string='ملاحظات') # 
    delivery_report_id = fields.Many2one('lm.delivery_report',string='محضر التسليم')