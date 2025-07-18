{
    'name': "Lands Management",
    'version': '1.0',
    'depends': ['base','mail','web'],
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
        'data/land_request_review.xml',
        'views/land_request_review.xml',
        'views/Contract.xml',
        'views/FollowupReport.xml',
        'views/EvaluationReport.xml',
        'views/DeliveryReport.xml',
        'views/wizard_views.xml',
    ],
    'application': True
}