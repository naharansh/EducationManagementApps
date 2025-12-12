from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError

class Tasks(models.Model):
    _name = 'edu.task'
    _description = 'Internal Task'
    _order = "deadline,priority"

    name = fields.Char(string="Task Title", required=True)
    description = fields.Text(string="Task Description")
    teacher_id = fields.Many2one('edu.teacher', string="Assigned To",required=True)
    priority = fields.Selection([('0', 'Low'), ('1', 'Medium'), ('2', 'High')], default='1', string="Priority")
    deadline = fields.Date(string="Deadline", default=lambda self: fields.Date.today())
    stage_id = fields.Many2one('academy.task.stage', string="Stage",required=True)
    is_overdue = fields.Boolean(
        compute="_compute_is_overdue",
        string="Overdue",
        store=False  # Set to False if you don't need to store it
    )

    @api.depends('deadline')
    def _compute_is_overdue(self):
        today = date.today()
        for rec in self:
            rec.is_overdue = bool(rec.deadline and rec.deadline < today)

    @api.constrains('name')
    def _checkname(self):
        for rec in self:
            stripped_name = rec.name.strip()
            if not stripped_name:
                raise ValidationError('Task title must not be empty or just whitespace.')

            # Ensure the name only contains alphabets and spaces (no special characters or numbers)
            if not all(word.isalpha() or word.isspace() for word in stripped_name):
                raise ValidationError("Task title should only contain alphabets and spaces.")

            # Ensure no excessive spaces between words (more than one space between words)
            if '  ' in stripped_name:  # Check for multiple consecutive spaces
                raise ValidationError("Task title must not contain excessive spaces between words.")

    @api.constrains('description')
    def _checkdescription(self):
        for rec in self:
            if not rec.description or not rec.description.strip():
                raise ValidationError('Task description is required and cannot be empty or just whitespace.')

         
class AcademyTask(models.Model):
       _name = "academy.task.stage"
       _description = "Task Stage"
       _order = "sequence"
       name = fields.Char(required=True)
       sequence = fields.Integer(default=1)
       color_index = fields.Integer("Color Index")