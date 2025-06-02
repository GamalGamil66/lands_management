from inspect import signature
from odoo import models, fields, api, _

class InvestmentReview(models.Model):
    _name = 'lm.investment_review'
    _description = 'تقييم الاستثمار'
    _rec_name = 'review_no'
    investment_id = fields.Many2one('lm.investment', string='الاستثمار', required=True)
    review_date = fields.Date(string='تاريخ التقييم')
    review_no = fields.Char(string='رقم التقييم')
    final_recommendation = fields.Selection([
        ('final_approve', 'الموافقة على طلب المستثمر والتوجيه باستكمال الإجراءات اللاحقة'),
        ('final_reject', 'عدم الموافقة على طلب المستثمر')], string='توصية الفريق النهائية', required=True)
    review_items = fields.One2many('lm.review_item', 'investment_review_id', string='عناصر التقييم')
    review_accept_conditions = fields.One2many('lm.review_accept_condition', 'investment_review_id', string='شروط الموافقة')
    review_reject_reasons = fields.One2many('lm.review_reject_reason', 'investment_review_id', string='أسباب الرفض')
    investor_clarification_requests = fields.One2many('lm.investor_clarification_request', 'investment_review_id', string='طلبات إيضاح/تعديل')
    review_team = fields.One2many('lm.review_team', 'investment_review_id', string='فريق المراجعة')

class ReviewItem(models.Model):
    _name = 'lm.review_item'
    _description = 'عنصر التقييم'
    
    name = fields.Char(string='اسم العنصر', required=True)
    result = fields.Selection([
        ('approve', 'موافقة'),
        ('approve_mod', 'موافقة مع التعديل'),
        ('reject', 'عدم موافقة')], string='نتيجة المراجعة', required=True)
    investment_review_id = fields.Many2one('lm.investment_review', string='تقييم الاستثمار', required=True)

class ReviewRejectReason(models.Model):
    _name = 'lm.review_reject_reason'
    _description = 'سبب رفض التقييم'
    
    name = fields.Char(string='اسم السبب', required=True)
    investment_review_id = fields.Many2one('lm.investment_review', string='تقييم الاستثمار', required=True)

class ReviewAcceptCondition(models.Model):
    _name = 'lm.review_accept_condition'
    _description = 'شرط الموافقة'
    
    name = fields.Char(string='اسم الشرط', required=True)
    investment_review_id = fields.Many2one('lm.investment_review', string='تقييم الاستثمار', required=True)

class InvestorClarificationRequest(models.Model):
    _name = 'lm.investor_clarification_request'
    _description = 'طلب إيضاح/تعديل'
    
    name = fields.Char(string='اسم الطلب', required=True)
    justification = fields.Text(string='التبرير', required=True)
    investment_review_id = fields.Many2one('lm.investment_review', string='تقييم الاستثمار', required=True)

class ReviewTeam(models.Model):
    _name = 'lm.review_team'
    _description = 'فريق المراجعة'
    
    name = fields.Char(string='اسم الفريق', required=True)
    characteristic = fields.Text(string='الصفة', required=True)
    signature = fields.Binary(string='التوقيع', required=True)
    signature_date = fields.Date(string='التاريخ', required=True)
    investment_review_id = fields.Many2one('lm.investment_review', string='تقييم الاستثمار', required=True)