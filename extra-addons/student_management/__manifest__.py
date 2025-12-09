{
    'name': "student_management",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
   'depends': ['base', 'calendar'],

    'data': [
        
        'security/ir.model.access.csv',

        # Sequences FIRST
        'data/edu_sequence.xml',
        'data/edu_classcodesequence.xml',
        'data/edu_teachersequence.xml',
        'data/edu_subjectsequence.xml',   
        'data/task_stage.xml',
        'views/student.xml',
        'views/classes.xml',
        'views/timetable.xml',
        'views/teacher.xml',
        'views/daily_record.xml',
        'views/attendence.xml',
        'views/fees.xml',
        'templates/template.xml',
        'views/task.xml',
        'views/report.xml',
        'views/menu.xml',
        'views/templates.xml',
        'views/reports.xml',],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets':{
        'web.assets_backend':[
            'student_management/static/src/style.css'
        ]
    }
}

