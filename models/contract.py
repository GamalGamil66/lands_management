from odoo import models, fields, api

# models.py

from odoo import models, fields, api

class Contract(models.Model):
    _name = 'lm.contract' # CHANGED
    _description = 'عقد انتفاع'

    name = fields.Char("الاسم")
    project_implementation_phase_ids = fields.One2many(
        'project.implementation.phase.data',
        'contract_id',
        string='مراحل التنفيذ',
        help='مراحل التنفيذ المرتبطة بهذا العقد'
    )

# models.py (continued)

class ProjectImplementationPhaseData(models.Model):
    _name = 'project.implementation.phase.data'
    _description = 'بيانات مراحل البرنامج الزمني للتنفيذ'
    _rec_name = 'display_name'

    contract_id = fields.Many2one(
        'lm.contract', # CHANGED
        string='العقد',
        ondelete='cascade',
        help='العقد المرتبط ببيانات مراحل التنفيذ هذه'
    )
    # ... rest of your fields remain the same ...
    project_or_certificate_ref = fields.Char(
        string='مرجع المشروع أو الشهادة',
        required=True,
        help="اسم المشروع أو رقم شهادة التسجيل التي يتبع لها هذا البرنامج الزمني."
    )
    phase_sequence = fields.Selection([
        ('first', 'المرحلة الأولى'),
        ('second', 'المرحلة الثانية'),
        ('third', 'المرحلة الثالثة')
        ], string='مراحل التنفيذ', required=True)
    
    implementation_start_date = fields.Date(string='تاريخ بدء التنفيذ')
    implementation_completion_date = fields.Date(string='تاريخ إتمام التنفيذ')
    commercial_activity_start_date = fields.Date(string='تاريخ بدء النشاط/الإنتاج التجاري')

    display_name = fields.Char(string="المعرف", compute='_compute_display_name', store=True)

    @api.depends('project_or_certificate_ref', 'phase_sequence')
    def _compute_display_name(self):
        for record in self:
            phase_display = dict(record._fields['phase_sequence'].selection).get(record.phase_sequence, '')
            record.display_name = f"{record.project_or_certificate_ref} - {phase_display}"

    _sql_constraints = [
        ('project_phase_unique', 'unique(project_or_certificate_ref, phase_sequence)',
         'يجب أن تكون المرحلة فريدة لكل مرجع مشروع أو شهادة!')
    ]