from odoo import models, fields

class ProjectFollowupReport(models.Model):
    _name = 'project.followup.report'
    _description = 'تقرير متابعة مشروع'
    # In your project.followup.report model
    _rec_name = 'name'
    name = fields.Char(string="عنوان التقرير", required=True)

    report_date = fields.Date(string='تاريخ التقرير', default=fields.Date.context_today)

    task_evaluation_ids = fields.One2many(
        'project.followup.task.evaluation',
        'report_id',
        string='تقييم مستوى التنفيذ للأعمال'
    )

    # سادساً: نتائج التقييم الأساسية
    eval_committed_on_time = fields.Boolean(string='ملتزم وفقا للفترة الزمنية المحددة للمستثمر')
    eval_relatively_committed = fields.Boolean(string='ملتزم نسبياً')
    eval_deviation_percentage = fields.Float(string='نسبة الانحراف (%)')
    eval_late = fields.Boolean(string='متأخر')
    eval_no_work_done = fields.Boolean(string='لم يتم تنفيذ اي اعمال')

    # سابعاً: النتائج التقييم الأخرى
    other_evaluation_results = fields.Html(string='النتائج التقييم الأخرى')

    # ثامناً: التوصيات
    recommendations = fields.Html(string='التوصيات')

class ProjectFollowupTaskEvaluation(models.Model):
    _name = 'project.followup.task.evaluation'
    _description = 'تقييم اعمال الخطة لمتابعة المشروع'

    report_id = fields.Many2one('project.followup.report', string='مرجع التقرير', ondelete='cascade')
    statement = fields.Text(string='البيان', required=True)
    specified_time = fields.Char(string='الزمن المحدد')
    execution_level = fields.Text(string='مستوى التنفيذ')
    notes = fields.Text(string='الملاحظات')

    # To display nicely in list views if not part of a one2many form
    name = fields.Char(string="المهمة", compute='_compute_name', store=True)

    def _compute_name(self):
        for record in self:
            if record.statement and len(record.statement) > 50:
                record.name = record.statement[:50] + "..."
            else:
                record.name = record.statement