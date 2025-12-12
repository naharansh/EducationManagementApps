from odoo import models,fields,api
from odoo.exceptions import ValidationError
from datetime import datetime
import re 
import imghdr
def validate_name(name):
    stripped_name =name.strip()
    if not stripped_name:
        raise ValidationError('Field must not be empty or just whitespace.')

        # Ensure the name only contains alphabets and spaces (no special characters or numbers)
    if not all(word.isalpha() or word.isspace() for word in stripped_name):
           raise ValidationError("Field should only contain alphabets and spaces.")

        # Ensure no excessive spaces between words (more than one space between words)
    if '  ' in stripped_name:  # Check for multiple consecutive spaces
          raise ValidationError("Field must not contain excessive spaces between words.")
class Student(models.Model):
    _name="student.model"
    _description="Student"
    name=fields.Char(string="Student Name",required=True)
    student_id=fields.Char(string="Student ID",readonly=True)
    dob=fields.Date(string="Date of Birth")
    photo = fields.Binary(string="Photo")
    parent_name = fields.Char(string="Parent Name")
    parent_contact = fields.Char(string="Parent Contact")
    address = fields.Text(string="Address")
    class_id = fields.Many2one('batch.class', string="Class")
    status = fields.Selection([('active','Active'),('inactive','Inactive'),('alumni','Alumni')], default='active')
    yearly_fee=fields.Float(string='Yearly Fee',required=True)
    fee_due_ids = fields.One2many(
    'edu.fee.due',
    'student_id',
    string="Fee Due Records"
    )

    remaining_yearly_fee = fields.Float(
     string="Remaining Yearly Fee",
     compute="_compute_remaining_yearly_fee",
     store=True
    )
    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            vals['student_id'] = self.env['ir.sequence'].next_by_code('student.model.code') or 'New'
        return super().create(vals_list)
    @api.constrains('class_id')
    def _check_class_capacity(self):
        for rec in self:
            if rec.class_id:
                cls = rec.class_id.sudo()
                count = self.env['student.model'].sudo().search_count([('class_id', '=', cls.id)])
                if cls.capacity and count > cls.capacity:
                    raise ValidationError(f"Cannot assign student to '{cls.name}': capacity of {cls.capacity} exceeded.")
    @api.depends('yearly_fee', 'fee_due_ids.paid_amount', )
    def _compute_remaining_yearly_fee(self):
     for student in self:
       
           total_paid = sum(
                float(d.paid_amount or 0.0)
                for d in student.fee_due_ids
               
            )

           student.remaining_yearly_fee = (student.yearly_fee or 0.0) - total_paid
    @api.constrains('name')
    def _check_name(self):
         for record in self:
             validate_name(record.name)

    @api.constrains('student_id')
    def _check_id(self):
        for record in self:
            existing_student=self.search([('student_id','=',record.student_id)],limit=1)
            if existing_student and existing_student != record:
                raise ValidationError("Student ID must be unique.")
    @api.constrains('dob')
    def _DateofBirth(self):
        for record in self : 
            if not record.dob:
                raise ValidationError('It is requird')
            today=datetime.today().date()
            age=today.year-record.dob.year- ((today.month, today.day) < (record.dob.month, record.dob.day))
            if age < 5:
                raise ValidationError('age should be greater than 5')
    @api.constrains('parent_name')
    def __checkname_(self):
        for record in self :
            validate_name(record.parent_name)
    @api.constrains('address')
    def __checkaddress(self):
        for record in self:  
         if not record.address or not record.address.strip():
            raise ValidationError("Address must not be empty or just whitespace.")

    @api.constrains('parent_contact')
    def __checkcontact(self):
        for record in self:
            # Ensure the contact is exactly 10 digits long
            if len(record.parent_contact) != 10:
                raise ValidationError('Parent Contact must be exactly 10 digits.')
            
            # Ensure the contact is numeric and doesn't contain alphabetic characters
            if not record.parent_contact.isdigit():
                raise ValidationError('Parent Contact must contain only numeric characters.')

            # Ensure the phone number matches a valid pattern (numbers, spaces, +, -, (, ))
            if record.parent_contact and not re.match(r'^[\d\+\-\(\) ]+$', record.parent_contact):
                raise ValidationError("Parent Contact must be a valid phone number, containing only numbers, spaces, and symbols like +, -, (, ).")
    @api.constrains('fee_due_ids')
    def _check_fee_due(self):
        for record in self:
            # Ensure the fee due records are consistent with the yearly fee
            total_fee_due = sum(fee_record.amount for fee_record in record.fee_due_ids)
            if total_fee_due > record.yearly_fee:
                raise ValidationError("Total Fee Due cannot exceed the Yearly Fee.")
    @api.constrains('yearly_fee')
    def __checkfees(self):
        for records in self:
            if records.yearly_fee <= 0 and records.yearly_fee == 0 :
                raise ValidationError('yearly_fee cannot nagitive and zero')
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


   
