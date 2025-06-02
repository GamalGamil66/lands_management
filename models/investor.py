from odoo import models, fields, api, _

class Investor(models.Model): 
    _name = 'lm.investor'
    _description = 'المستثمر'
    _rec_name = 'investor_name'
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
    registered_company_ids = fields.One2many('lm.registered_company', 'investor_id', string='الشركات المسجلة')
    company_authorized_agent_ids = fields.One2many('lm.company_authorized_agent', 'investor_id', string='وكيل الشركة المفوض')

class RegisteredCompany(models.Model):
    _name = 'lm.registered_company'
    _description = 'الشركة المسجلة'
    # _rec_name = 'username'
    company_name = fields.Char(string='اسم الشركة', required=True)
    legal_form = fields.Selection([
        ('sole_proprietorship', 'ملكية فردية'),
        ('partnership', 'شراكة'),
        ('limited_liability_company', 'شركة ذات مسؤولية محدودة'),
        ('public_company', 'شركة مساهمة')],
        string='الشكل القانوني')
    reg_number = fields.Char(string='رقم التسجيل')
    reg_date = fields.Date(string='تاريخ التسجيل')
    nationality = fields.Many2one('res.country', string='الجنسية')
    activity = fields.Char(string='النشاط')
    location = fields.Char(string='الموقع')
    contact_name = fields.Char(string='اسم جهة الاتصال')
    role = fields.Char(string='الدور')
    phones = fields.Char(string='أرقام الهواتف')
    email = fields.Char(string='البريد الإلكتروني')
    investor_id = fields.Many2one('lm.investor', string='المستثمر')

class CompanyAuthorizedAgent(models.Model):
    _name = 'lm.company_authorized_agent'
    _description = 'وكيل الشركة المفوض'
    # _rec_name = 'username'
    agent_name = fields.Char(string='اسم الوكيل', required=True)
    authorization_type = fields.Selection([
        ('general', 'عام'),
        ('limited', 'محدود')],
        string='نوع التفويض')
    phones = fields.Char(string='أرقام الهواتف')
    email = fields.Char(string='البريد الإلكتروني')
    id_number = fields.Char(string='رقم الهوية', unique=True)
    id_date = fields.Date(string='تاريخ الهوية')
    attachments = fields.One2many('lm.company_authorized_agent_attachment', 'company_authorized_agent', string='مرفقات وكيل الشركة المفوض')
    investor_id = fields.Many2one('lm.investor', string='المستثمر')

class CompanyAuthorizedAgentAttachment(models.Model):
    _name = 'lm.company_authorized_agent_attachment'
    _description = 'مرفقات وكيل الشركة المفوض'
    # _rec_name = 'username'
    attachment = fields.Binary(string='المرفق', required=True)
    company_authorized_agent = fields.Many2one('lm.company_authorized_agent', string='وكيل الشركة المفوض')