from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError
import re
import imghdr
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
  

    subject_ids = fields.Many2many(
        'edu.subject',
        
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
           vals['employee_id'] = self.env['ir.sequence'].next_by_code('edu.teacher.code') or 'New'
        return super(Teacher, self).create(vals_list)
    @api.constrains('name')
    def _checkname(self):
        for rec in self:
            stripped_name =rec.name.strip()
            if not stripped_name:
                raise ValidationError('Field must not be empty or just whitespace.')

                # Ensure the name only contains alphabets and spaces (no special characters or numbers)
            if not all(word.isalpha() or word.isspace() for word in stripped_name):
                raise ValidationError("Field should only contain alphabets and spaces.")

                # Ensure no excessive spaces between words (more than one space between words)
            if '  ' in stripped_name:  # Check for multiple consecutive spaces
                raise ValidationError("Field must not contain excessive spaces between words.")
    @api.constrains('employee_id')
    def _checkid(self):
        for rec in self:
            existing_student=self.search([('employee_id','=',rec.employee_id)],limit=1)
            if existing_student and existing_student != rec:
                raise ValidationError("Student ID must be unique.")
    @api.constrains('contact')
    def _checkcontact(self):
        for record in self:
            if len(record.parent_contact) != 10:
                raise ValidationError('Parent Contact must be exactly 10 digits.')
            
            # Ensure the contact is numeric and doesn't contain alphabetic characters
            if not record.parent_contact.isdigit():
                raise ValidationError('Parent Contact must contain only numeric characters.')

            # Ensure the phone number matches a valid pattern (numbers, spaces, +, -, (, ))
            if record.parent_contact and not re.match(r'^[\d\+\-\(\) ]+$', record.parent_contact):
                raise ValidationError("Parent Contact must be a valid phone number, containing only numbers, spaces, and symbols like +, -, (, ).")
    @api.constrains('email')
    def _checkemail(self):
        for rec in self:
            if not rec.email :
                raise ValidationError("email is required")
            if rec.email :
                email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_regex,rec.email):
                     raise ValidationError("Please enter a valid email address.")
    @api.constrains('subject_ids')
    def _check_subjects(self):
        for rec in self:
            if not rec.subject_ids:
                raise ValidationError("At least one subject must be selected.")
    @api.constrains('photo')
    def __check(self):
        max_size = 1 * 1024 * 1024  # 1 MB
        for record in self:
            if not record.photo:
                raise ValidationError('Image should be uploaded')    
            if record.photo and len(record.photo) > max_size:
                raise ValidationError("The photo size must not exceed 1 MB.")
            if record.photo:  
                img_type = imghdr.what(None, h=record.photo)
                if img_type not in ['jpeg', 'png','jpg']:  # Valid image types
                    raise ValidationError("Photo must be in JPG or PNG format.")

            


