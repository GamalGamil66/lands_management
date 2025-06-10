from odoo import models, fields, api

class EvaluationReport(models.Model):
    _name = 'lm.evaluation_report'
    _description = 'تقرير متابعة'
    name = fields.Char("الاسم")
    project_detailed_activity_line_ids = fields.One2many('project.detailed.activity.line', 'evaluation_report_id', 'بنود تقييم نشاط مفصل للمشروع')

class ProjectDetailedActivityLine(models.Model):
    _name = 'project.detailed.activity.line'
    _description = 'بند تقييم نشاط مفصل للمشروع'
    
    activity_type = fields.Selection([
        ('land_settlement', 'اعمال تسوية الارض وتسويرها'),
        ('foundation_concrete', 'اعمال الاساسات والخرسانة'),
        ('construction_concrete_metal', 'الاعمال الانشائية والخرسانية والمعدنية'),
        ('equipment_purchase', 'شراء او استيراد الآلات والمعدات والتجهيزات والاثاث ... الخ'),
        ('equipment_installation', 'تركيب الآلات والمعدات والتجهيزات'),
        ('completion_all_works_installation', 'استكمال كافة الاعمال المدنية والانشائية وتركيب الآلات والمعدات والتجهيزات'),
        ('completion_other', 'اخرى تحدد (ضمن استكمال كافة الاعمال)'),
        ('trial_operation_start', 'البدء في التشغيل التجريبي')
        ], string='البيان', required=True)
    
    
    current_execution_level = fields.Text(string='مستوى التنفيذ الحالي')
    notes = fields.Text(string='الملاحظات')

    # For display purposes, if needed outside of a direct one2many context
    name = fields.Char(compute='_compute_name', string="وصف النشاط", store=True)
    evaluation_report_id = fields.Many2one('lm.evaluation_report', string="تقرير متابعة")

    @api.depends('activity_type')
    def _compute_name(self):
        activity_type_labels = dict(self._fields['activity_type'].selection)
        for record in self:
            base_name = activity_type_labels.get(record.activity_type, '')
            if record.activity_type not in ['completion_other']:
                record.name = base_name
            else:
                record.name = ''