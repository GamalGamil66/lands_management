{
    'name': "Lands Management",
    'version': '1.0',
    'depends': ['base','mail'],
    'author': "Gamal",
    'category': '',
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/investor_view.xml',
        'views/investment_view.xml',
        'views/sectors_view.xml',
        'views/investment_review_view.xml',
        'views/investment_request_view.xml',
        'reports/report_investment_request.xml',
    ],
    'application': True
}