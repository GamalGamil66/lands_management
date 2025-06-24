# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class LandRequestReview(models.Model):
    _name = 'land.request.review'
    _description = 'Land Allocation Request Review' # Internal description
    _inherit = ['mail.thread', 'mail.activity.mixin'] # For chatter and activities
    _rec_name = 'name'

    name = fields.Char(
        string="مرجع المراجعة",  # Translated from "Review Reference"
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _('جديد'), # Translated from "New"
        help="Unique reference for this land request review."
    )
    review_form_type = fields.Char(
        string="نوع نموذج المراجعة",  # Translated from "Review Form Type"
        default="إستمارة رقم (٢)",
        readonly=True,
        help="Identifier for the type of review form being used."
    )
    reviewed_request_ref = fields.Char(
        string="مرجع الطلب المراجع",  # Translated from "Reviewed Request Reference"
        help="Reference of the original request being reviewed (Corresponds to: الموضوع: بشأن إستمارة رقم ( ) للبحث الآتي)."
    )
    # branch_id = fields.Many2one(
    #     comodel_name='land.authority.branch',
    #     string="فرع الهيئة",  # Translated from "Authority Branch"
    #     required=True,
    #     help="The authority branch conducting this review."
    # )
    applicant_id = fields.Many2one(
        comodel_name='res.partner',
        string="مقدم الطلب",  # Translated from "Applicant"
        help="The person or company that submitted the original request (Corresponds to: من / ...)."
    )
    request_summary = fields.Text(
        string="ملخص طلب المتقدم",  # Translated from "Applicant's Request Summary"
        help="Summary of the applicant's request (Corresponds to: تتلخص مطالبة المذكور بـ)."
    )
    submission_date = fields.Date(
        string="تاريخ إنشاء المراجعة",  # Translated from "Review Creation Date"
        default=fields.Date.context_today,
        readonly=True,
        help="Date this review record was created."
    )

    # --- Higher Authority Directives ---
    higher_authority_directive_source = fields.Char(
        string="مصدر توجيه السلطة العليا",  # Translated from "Higher Authority Directive Source"
        help="Source of the higher authority directive (Corresponds to: ...صادرة من)."
    )
    higher_authority_directive_number = fields.Char(
        string="رقم توجيه السلطة العليا",  # Translated from "Higher Authority Directive Number"
        help="Reference number of the directive (Corresponds to: ...برقم)."
    )
    higher_authority_directive_date = fields.Date(
        string="تاريخ توجيه السلطة العليا",  # Translated from "Higher Authority Directive Date"
        help="Date of the directive (Corresponds to: ...وتاريخ)."
    )

    # --- Head of Authority (HOA) Directives ---
    hoa_directive_number = fields.Char(
        string="رقم توجيه رئيس الهيئة",  # Translated from "HOA Directive Number"
        help="Reference number of the Head of Authority's directive (Corresponds to: توجيهات رئيس الهيئة برقم...)."
    )
    hoa_directive_date = fields.Date(
        string="تاريخ توجيه رئيس الهيئة",  # Translated from "HOA Directive Date"
        help="Date of the HOA's directive (Corresponds to: ...وتاريخ...)."
    )
    hoa_directive_stipulation = fields.Text(
        string="ما يقضي به توجيه رئيس الهيئة",  # Translated from "HOA Directive Stipulation"
        help="Details of what the HOA's directive stipulates (Corresponds to: ...تقضي بـ)."
    )

    # --- General Investment Authority (GIA) Prior Study Details ---
    gia_prior_study_notes = fields.Text(
        string="ملخص الدراسة السابقة للهيئة العامة للاستثمار",  # Translated from "GIA Prior Study Summary"
        help="Summary of prior study by GIA (Corresponds to: سبق دراسة المشروع من قبل الهيئة العامة للإستثمار وتضمن)."
    )
    gia_license_decision_number = fields.Char(
        string="رقم قرار/تسجيل الهيئة العامة للاستثمار",  # Translated from "GIA License/Registration Number"
        help="License or registration number from GIA (Corresponds to: ...قرار تسجيل 'الترخيص'...برقم...)."
    )
    gia_license_decision_date = fields.Date(
        string="تاريخ قرار/تسجيل الهيئة العامة للاستثمار",  # Translated from "GIA License/Registration Date"
        help="Date of GIA license or registration (Corresponds to: ...وتاريخ...)."
    )
    gia_land_opinion_request_number = fields.Char(
        string="رقم مذكرة طلب إبداء الرأي (هيئة الاستثمار)",  # Translated from "GIA Land Opinion Request Note Number"
        help="Note number for GIA's land opinion request (Corresponds to: ...مذكرة طلب إبداء رأي...برقم...)."
    )
    gia_land_opinion_request_date = fields.Date(
        string="تاريخ مذكرة طلب إبداء الرأي (هيئة الاستثمار)",  # Translated from "GIA Land Opinion Request Note Date"
        help="Date of GIA's land opinion request note (Corresponds to: ...وتاريخ...)."
    )

    # --- Document & Site Status ---
    missing_documents_details = fields.Text(
        string="تفاصيل الوثائق الناقصة",  # Translated from "Missing Documents Details"
        help="List or description of missing documents (Corresponds to: الوثائق الناقصة)."
    )
    previous_sites_status = fields.Text(
        string="حالة المواقع المحصل عليها سابقاً",  # Translated from "Status of Previously Obtained Sites"
        help="Status of any sites previously obtained by the applicant, if any (Corresponds to: الموقف من المواقع التي سبق له الحصول عليها (إن وجدت))."
    )

    # --- Review Opinion & Action (رأي) ---
    review_action = fields.Selection(
        string="إجراء المراجعة (الرأي)",  # Translated from "Review Action"
        required=False,
        selection=[
            ('file_request', 'إشعار صاحب الشأن وتعذر تلبية الطلب وحفظه'), # إشعار صاحب الشأن يتعذر تلبية الطلب ويحفظ الطلب بالملف
            ('refer_gia', 'إحالة إلى الهيئة العامة للاستثمار'), # حالة الطلب الى . (الهيئة العامة للإستثمار)
            ('refer_survey_dept', 'إحالة إلى إدارة المساحة') # حالة الطلب الى . (إدارة المساحة)
        ],
        tracking=True,
        help="The decided course of action based on the review."
    )
    file_request_reasons = fields.Text(
        string="أسباب حفظ/رفض الطلب",  # Translated from "Reasons for Filing/Rejection"
        help="Reasons if the request is to be filed or rejected (Corresponds to: للأسباب التالية). This field would typically be visible if 'Review Action' is 'Notify Applicant & File Request'."
    )
    action_report_recipient = fields.Char(
        string="موجه إليه الرد/التقرير",  # Translated from "Recipient of Response/Report"
        help="To whom the response or report should be addressed (Corresponds to: تحرير ردا / تقرير لـ)."
    )

    # --- GIA Referral Details (Conditional visibility in view) ---
    gia_referral_purpose = fields.Text(
        string="الغرض من الإحالة لهيئة الاستثمار",  # Translated from "Purpose of GIA Referral"
        default="لدراسة المشروع في إطار النافذة الواحدة للإستثمار للتأكد من جدوى المشروع وجدية المستثمر والتنفيذ للسير في إجراءات تسجيل المشروع الإستثماري وإستيفاء الوثائق والضمانات المطلوبة وفقاً لمحضر الضوابط والقواعد الإجراءات الموقعة بين الهيئتين بتاريخ ٢٠١٣/٨/٣ م ، وموافاتنا بالنتائج ليتم البت في الطلب في ضوء ذلك.",
        help="Detailed purpose for referring to GIA. Visible if action is 'Refer to GIA'."
    )
    gia_inter_authority_agreement_date = fields.Date(
        string="تاريخ المحضر بين الهيئتين (هيئة الاستثمار)",  # Translated from "Inter-Authority Agreement Date (GIA)"
        default=fields.Date.to_date('2013-08-03'),
        help="Date of the agreement between authorities mentioned in GIA referral. Visible if action is 'Refer to GIA'."
    )

    # --- Survey Department Referral Details (Conditional visibility in view) ---
    survey_dept_referral_purpose_template = fields.Text(
        string="نموذج الغرض (إدارة المساحة)", # Translated
        default="للنزول للمنطقة لبحث إمك    انية إسقاط المساحة المطلوبة للمشروع وقدرها {area} م٢ بموجب مذكرة طلب إبداء الرأي بشأن إمكانية تخصيص أرض للمشروع المرفقة، الصادرة من الهيئة العامة للإستثمار برقم {gia_opinion_req_num} بتاريخ {gia_opinion_req_date} م. المحالة الينا بمذكرة الهيئة رقم {hoa_referral_note_num} وتاريخ {hoa_referral_note_date} م حسب محضر الضوابط الموقع بين الهيئتين.",
        help="Template for survey department referral. Actual text might be constructed."
    )
    survey_dept_requested_area_sqm = fields.Float(
        string="المساحة المطلوبة للمسح (م٢)",  # Translated from "Requested Area for Survey (sqm)"
        help="Area in square meters requested for the project (Corresponds to: وقدرها ...... م٢). Visible if action is 'Refer to Survey Dept'."
    )
    survey_dept_gia_opinion_req_num = fields.Char(
        string="رقم طلب إبداء الرأي من هيئة الاستثمار (للمساحة)",  # Translated from "GIA Opinion Req. No. (for Survey)"
        help="GIA opinion request number related to survey (Corresponds to: ...برقم...). Visible if action is 'Refer to Survey Dept'."
    )
    survey_dept_gia_opinion_req_date = fields.Date(
        string="تاريخ طلب إبداء الرأي من هيئة الاستثمار (للمساحة)",  # Translated from "GIA Opinion Req. Date (for Survey)"
        help="Date of GIA opinion request for survey (Corresponds to: ...بتاريخ...). Visible if action is 'Refer to Survey Dept'."
    )
    survey_dept_hoa_referral_note_num = fields.Char(
        string="رقم مذكرة الإحالة من رئيس الهيئة (للمساحة)",  # Translated from "HOA Referral Note No. (to Survey)"
        help="HOA referral note number to survey department (Corresponds to: ...مذكرة الهيئة رقم...). Visible if action is 'Refer to Survey Dept'."
    )
    survey_dept_hoa_referral_note_date = fields.Date(
        string="تاريخ مذكرة الإحالة من رئيس الهيئة (للمساحة)",  # Translated from "HOA Referral Note Date (to Survey)"
        help="Date of HOA referral note to survey department (Corresponds to: ...وتاريخ...). Visible if action is 'Refer to Survey Dept'."
    )
    survey_dept_inter_authority_agreement_date = fields.Date(
        string="تاريخ المحضر بين الهيئتين (المساحة)",  # Translated from "Inter-Authority Agreement Date (Survey)"
        default=fields.Date.to_date('2013-08-03'),
        help="Date of the agreement between authorities mentioned in Survey referral. Visible if action is 'Refer to Survey Dept'."
    )

    # --- Signatories ---
    specialist_id = fields.Many2one(
        comodel_name='res.users',
        string="المختص",  # Translated from "Specialist"
        help="The specialist who conducted the review."
    )
    specialist_signature_date = fields.Date(
        string="تاريخ توقيع المختص",  # Translated from "Specialist Signature Date"
        help="Date the specialist signed off."
    )
    investment_director_id = fields.Many2one(
        comodel_name='res.users',
        string="مدير إدارة الإستثمار",  # Translated from "Director of Investment Dept."
        help="The Director of the Investment Department."
    )
    investment_director_signature_date = fields.Date(
        string="تاريخ توقيع المدير",  # Translated from "Director Signature Date"
        help="Date the Director signed off."
    )

    # --- Workflow State ---
    state = fields.Selection(
        string="الحالة",  # Translated from "Status"
        default='draft',
        selection=[
            ('draft', 'مسودة'),
            ('under_review', 'قيد المراجعة'),
            ('opinion_reached', 'تم التوصل إلى رأي'),
            ('referred_gia', 'أحيل إلى هيئة الاستثمار'),
            ('referred_survey', 'أحيل إلى إدارة المساحة'),
            ('filed', 'محفوظ/مرفوض'),
            ('completed', 'مكتمل')
        ],
        required=True,
        tracking=True,
        copy=False,
        help="Current stage of the review process."
    )

    investment_request_ids = fields.One2many('lm.investment_request', 'land_request_review_id', string='Investment Requests')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('جديد')) == _('جديد'): # Translated "New"
                sequence = self.env['ir.sequence'].next_by_code('land.request.review')
                vals['name'] = sequence or _('جديد') # Translated "New"
        return super(LandRequestReview, self).create(vals_list)

    def action_submit_for_review(self):
        for record in self:
            if record.state == 'draft':
                record.state = 'under_review'
        return True

    def action_set_opinion(self):
        for record in self:
            if not record.review_action:
                raise UserError(_("يرجى تحديد 'إجراء المراجعة (الرأي)' قبل تأكيد الرأي.")) # Translated
            record.state = 'opinion_reached'
        return True
        
    def action_proceed_after_opinion(self):
        for record in self:
            if record.state != 'opinion_reached':
                raise UserError(_("يجب التوصل إلى رأي قبل المتابعة.")) # Translated
            if record.review_action == 'file_request':
                record.state = 'filed'
            elif record.review_action == 'refer_gia':
                record.state = 'referred_gia'
            elif record.review_action == 'refer_survey_dept':
                record.state = 'referred_survey'
        return True

    def action_complete(self):
        for record in self:
            record.state = 'completed'
            record.investment_request_ids.write({'state': 'reviewed'})
        return True

    def action_reset_to_draft(self):
        for record in self:
            record.state = 'draft'
        return True

    # @api.onchange('review_action')
    # def _onchange_review_action(self):
    #     if self.review_action != 'refer_gia':
    #         self.gia_referral_purpose = self.env['land.request.review'].default_get(['gia_referral_purpose'])['gia_referral_purpose']
    #     if self.review_action != 'refer_survey_dept':
    #         self.survey_dept_requested_area_sqm = False
    #         self.survey_dept_gia_opinion_req_num = False
    #         self.survey_dept_gia_opinion_req_date = False
    #         self.survey_dept_hoa_referral_note_num = False
    #         self.survey_dept_hoa_referral_note_date = False
    #     if self.review_action != 'file_request':
    #         self.file_request_reasons = False
    