from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Subject(models.Model):
    _name = "edu.subject"
    _description = "Subject"

    name = fields.Char(string="Subject Name", required=True)
    code = fields.Char(string="Subject Code", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('code'):
                vals['code'] = self.env['ir.sequence'].next_by_code('edu.subject.code') or 'SUB-NEW'
        return super(Subject, self).create(vals_list)

    @api.constrains('name')
    def __checkname(self):
        for rec in self:
            stripped_name = rec.name.strip()
            
            if not stripped_name:
                raise ValidationError('Subject Name must not be empty or just whitespace.')

            # Ensure the name only contains alphabets and spaces (no special characters or numbers)
            if not all(word.isalpha() or word.isspace() for word in stripped_name):
                raise ValidationError("Subject Name should only contain alphabets and spaces.")

            # Ensure no excessive spaces between words (more than one space between words)
            if '  ' in stripped_name:  # Check for multiple consecutive spaces
                raise ValidationError("Subject Name must not contain excessive spaces between words.")

    @api.constrains('code')
    def _check_code(self):
        for record in self:
            # Ensure code is unique
            existing_subject = self.search([('code', '=', record.code)], limit=1)
            if existing_subject and existing_subject != record:
                raise ValidationError("Subject Code must be unique.")
