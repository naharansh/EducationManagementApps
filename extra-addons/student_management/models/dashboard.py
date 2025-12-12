from odoo import models, fields, api

class EducationDashboard(models.Model):
    _name = 'education.dashboard'
    _description = 'Education Dashboard'
    _auto = False  # Virtual model, not stored in DB

    total_students = fields.Integer(string="Total Students")
    active_classes = fields.Integer(string="Total Active Classes")
    fees_pending_students = fields.Integer(string="Students With Fees Pending")
    total_outstanding = fields.Float(string="Total Outstanding Amount")
    todays_classes = fields.Integer(string="Today’s Classes")
    todays_attendance = fields.Integer(string="Months Attendance (%)")
    abesent = fields.Integer(string="Month's Absenties (%)")
    @api.model
    def init(self):
        """Define a SQL view for the dashboard metrics"""
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW education_dashboard AS (
                SELECT
                    1 as id,
                    (SELECT COUNT(*) FROM student_model) as total_students,
                    (SELECT COUNT(*) FROM batch_class WHERE start_date <= current_date 
   AND end_date >= current_date) as active_classes,
                  (SELECT COUNT(*) 
 FROM edu_fee_due 
 WHERE yearly_status = 'unpaid') AS fees_pending_students,
                    (SELECT COALESCE(SUM(balance_amount),0) FROM edu_fee_due WHERE paid_amount<>0) as total_outstanding,
                    (SELECT COUNT(*) FROM batch_class WHERE start_date = current_date) as todays_classes,
                    (SELECT COALESCE(SUM(present_days),0) FROM edu_monthly_attendence_line ) as todays_attendance,
                    (SELECT COALESCE(SUM(absent_days),0) FROM edu_monthly_attendence_line ) as  abesent
                            
            )
        """)