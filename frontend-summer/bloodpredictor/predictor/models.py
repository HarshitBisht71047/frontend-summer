from django.db import models

class BloodReport(models.Model):
    report_pdf = models.FileField(upload_to='reports/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report uploaded on {self.uploaded_at}"
