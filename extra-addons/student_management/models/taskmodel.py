from odoo import models,fields,api
from datetime import date
class Tasks(models.Model):
    _name='edu.task'
    _description='Internal Task'
    _order="deadline,priority"
    name=fields.Char(string="Task Title",required=True)
    description=fields.Text(string="Task Description")
    teacher_id=fields.Many2one('edu.teacher',string="Assigned To")
    priority=fields.Selection([('0','Low'),('1','Medium'),('2','High')],default='1',string="Priority")
    deadline=fields.Date(string="Deadline")
    stage_id=fields.Many2one('academy.task.stage',string="Stage")
    is_overdue = fields.Boolean(
        compute="_compute_is_overdue",
        string="Overdue",
        store=True,default="To-Do"
    )
    @api.depends('deadline')
    def _compute_is_overdue(self):
        today=date.today()
        for rec in self:
           rec.is_overdue = bool(rec.deadline and rec.deadline < today)
    
         
class AcademyTask(models.Model):
       _name = "academy.task.stage"
       _description = "Task Stage"
       _order = "sequence"
       name = fields.Char(required=True)
       sequence = fields.Integer(default=1)
       color_index = fields.Integer("Color Index")