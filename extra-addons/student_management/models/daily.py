from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DailyRecord(models.Model):
    _name = "edu.daily.record"
    _description = "Daily Record of Student Activities"
    _order = "date desc"

    date = fields.Date(default=fields.Date.today, required=True, string="Date")
    class_id = fields.Many2one('batch.class', string="Class/Batch", required=True)
    subject_id = fields.Many2one('edu.subject', string="Subject", required=True)
    teacher_id = fields.Many2one('edu.teacher', string="Teacher", required=True)
    topic = fields.Char(string="Topic Covered", required=True)
    notes = fields.Text(string="Additional Notes")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], default='draft', string="Status")

    student_line_ids = fields.One2many(
        'edu.daily.record.line',
        'record_id',
        string="Student Records"
    )

    @api.onchange('class_id')
    # def _onchange_class_id(self):
    #     if self.class_id:
    #         lines = [(0, 0, {
    #             'student_id': student.id,
    #             'status': 'present',
    #         }) for student in self.class_id.student_ids]

    #         self.student_line_ids = [(5, 0, 0)] + lines
    #     else:
    #         self.student_line_ids = [(5, 0, 0)]
        # @api.onchange('class_id')
    def _onchange_class_id(self):
        if self.class_id:
            # Update the domain of the subject field based on the selected class_id
            return {
                'domain': {
                    'subject_id': [('class_id', '=', self.class_id.id)]
                }
            }
        return {
            'domain': {
                'subject_id': []
            }
        }
    def action_confirm(self):
        self.state = 'done'

    def action_reset(self):
        self.state = 'draft'

    @api.constrains('topic')
    def check(self):
        for rec in self:
            stripped_name = rec.topic.strip()
            if not stripped_name:
                raise ValidationError('Field must not be empty or just whitespace.')

            # Ensure the topic only contains alphabets and spaces (no special characters or numbers)
            if not all(word.isalpha() or word.isspace() for word in stripped_name):
                raise ValidationError("Field should only contain alphabets and spaces.")

            # Ensure no excessive spaces between words (more than one space between words)
            if '  ' in stripped_name:  # Check for multiple consecutive spaces
                raise ValidationError("Field must not contain excessive spaces between words.")

class DailyRecordLine(models.Model):
    _name = "edu.daily.record.line"
    _description = "Daily Record Line for Each Student"

    record_id = fields.Many2one(
        'edu.daily.record',
        string="Daily Record",
        required=True,
        ondelete='cascade'
    )
    student_id = fields.Many2one('student.model', string="Student")  # Ensure this is the correct model
    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent')
    ], default='present', string="Attendance Status")
    remarks = fields.Text(string="Remarks")
