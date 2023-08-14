from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from storages.backends.ftp import FTPStorage

from author.models import User
from author.models.user_model import Designation

fs = FTPStorage()


class File(models.Model):
    file = models.FileField(storage=fs, upload_to="assets", help_text="Max size of file: 20MB.")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def clean_attachment(self):
        if self.file and self.file.size > 20 * 1024 * 1024:
            raise ValidationError('File too large. Size should not exceed 20 MB.')

    def __str__(self):
        return self.file.name


class Municipality(models.Model):
    name = models.CharField(max_length=250, unique=True, verbose_name="Municipality Name")
    priority = models.IntegerField(default=50,
                                   help_text="Set the priority any number, higher priority makes the content show first")

    def __str__(self):
        return self.name


class InstituteType(models.Model):
    name = models.CharField(max_length=250, unique=True, verbose_name="Institute Type")
    priority = models.IntegerField(default=50,
                                   help_text="Set the priority any number, higher priority makes the content show first")

    def __str__(self):
        return self.name


class Institute(models.Model):
    name = models.CharField(max_length=250, verbose_name="Institute Name")
    address = models.CharField(max_length=250, verbose_name="Address")
    municipality = models.ForeignKey(Municipality, null=True, blank=True, on_delete=models.CASCADE,
                                     verbose_name="Municipality")
    institute_type = models.ForeignKey(InstituteType, on_delete=models.CASCADE, verbose_name="Institute Type")
    priority = models.IntegerField(default=50,
                                   help_text="Set the priority any number, higher priority makes the content show first")

    def __str__(self):
        return self.name


# Model representing types of complainants (e.g., students, teachers, parents)
class ComplainantType(models.Model):
    name = models.CharField(max_length=250, verbose_name="Complainant Type")
    priority = models.IntegerField(default=50,
                                   help_text="Set the priority any number, higher priority makes the content show first")

    def __str__(self):
        return self.name


# Model representing classes or grade levels in an educational system
class Class(models.Model):
    name = models.CharField(max_length=250, verbose_name="Class Name")
    priority = models.IntegerField(default=50,
                                   help_text="Set the priority any number, higher priority makes the content show first")
    def __str__(self):
        return self.name


# Model representing subjects or topics of complaints
class Subject(models.Model):
    name = models.CharField(max_length=250, verbose_name="Subject")
    priority = models.IntegerField(default=50,
                                   help_text="Set the priority any number, higher priority makes the content show first")
    def __str__(self):
        return self.name


class ComplaintStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')
    UNDER_REVIEW = 'under_review', _('Under Review')
    IN_PROGRESS = 'in_progress', _('In Progress')
    ESCALATED = 'escalated', _('Escalated')
    ON_HOLD = 'on_hold', _('On Hold')
    RESOLVED = 'resolved', _('Resolved')
    PARTIALLY_RESOLVED = 'partially_resolved', _('Partially Resolved')
    REJECTED = 'rejected', _('Rejected')
    CLOSED = 'closed', _('Closed')
    ONGOING = 'ongoing', _('Ongoing')
    FEEDBACK_PROVIDED = 'feedback_provided', _('Feedback Provided')


class Complaint(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True, help_text="Enter the title of the complaint.")
    details = models.TextField(null=True, blank=True, help_text="Enter the details of the complaint.")
    complainant_name = models.CharField(max_length=250, null=True, blank=True,
                                        help_text="Enter the name of the complainant.")
    complainant_phone = models.CharField(max_length=14, null=True, blank=True,
                                         help_text="Enter the phone number of the complainant.")
    complainant_email = models.EmailField(null=True, blank=True,
                                          help_text="Enter the email address of the complainant.")

    student_name = models.CharField(max_length=250, null=True, blank=True,
                                    help_text="Enter the name of the student involved in the complaint.")
    student_roll = models.IntegerField(null=True, blank=True, help_text="Enter the roll number of the student.")
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, null=True, blank=True,
                                  help_text="Select the institute associated with the complaint.")
    complained_to = models.ForeignKey(Designation, on_delete=models.CASCADE, null=True, blank=True,
                                      help_text="Select the designation of the person the complaint is addressed to.")
    complainant_type = models.ForeignKey(ComplainantType, on_delete=models.CASCADE, null=True, blank=True,
                                         help_text="Select the type of complainant.")
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True,
                                      help_text="Select the class of the student involved.")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True,
                                help_text="Select the subject or topic of the complaint.")
    file = models.ForeignKey(File, null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ComplaintStatus.choices, default=ComplaintStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Feedback(models.Model):
    comments = models.TextField()
    complain = models.ForeignKey(Complaint, on_delete=models.CASCADE,
                                 help_text="Select the complaint for which feedback is given.")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                             help_text="Select the user providing the feedback.")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='replies',
                               help_text="Parent feedback in the reply chain.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback for {self.complain.title} by {self.user.username}"
