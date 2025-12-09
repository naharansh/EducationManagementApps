from odoo import models, fields, api

class Teacher(models.Model):
    _name = 'edu.teacher'
    _description = 'Teacher'
    _order = 'name'
    _rec_name = "name"


    name = fields.Char(string="Teacher Name", required=True)
    employee_id = fields.Char(
        string="Employee ID",
        readonly=True,
    )
    contact = fields.Char(string="Contact Number")
    email = fields.Char(string="Email")
    photo = fields.Binary(string="Photo")
    phone = fields.Char(string="Phone Number")


    subject_ids = fields.Many2many(
        'edu.subject',
        
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
           vals['employee_id'] = self.env['ir.sequence'].next_by_code('edu.teacher.code') or 'New'
        return super(Teacher, self).create(vals_list)