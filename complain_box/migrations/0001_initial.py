# Generated by Django 4.1.3 on 2023-08-13 13:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import storages.backends.ftp


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Class Name')),
            ],
        ),
        migrations.CreateModel(
            name='ComplainantType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Complainant Type')),
            ],
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter the title of the complaint.', max_length=250)),
                ('details', models.TextField(help_text='Enter the details of the complaint.')),
                ('complainant_name', models.CharField(help_text='Enter the name of the complainant.', max_length=250)),
                ('complainant_phone', models.CharField(help_text='Enter the phone number of the complainant.', max_length=14)),
                ('complainant_email', models.EmailField(help_text='Enter the email address of the complainant.', max_length=254)),
                ('student_name', models.CharField(help_text='Enter the name of the student involved in the complaint.', max_length=250)),
                ('student_roll', models.IntegerField(help_text='Enter the roll number of the student.')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('under_review', 'Under Review'), ('in_progress', 'In Progress'), ('escalated', 'Escalated'), ('on_hold', 'On Hold'), ('resolved', 'Resolved'), ('partially_resolved', 'Partially Resolved'), ('rejected', 'Rejected'), ('closed', 'Closed'), ('ongoing', 'Ongoing'), ('feedback_provided', 'Feedback Provided')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('complainant_type', models.ForeignKey(help_text='Select the type of complainant.', on_delete=django.db.models.deletion.CASCADE, to='complain_box.complainanttype')),
                ('complained_to', models.ForeignKey(help_text='Select the designation of the person the complaint is addressed to.', on_delete=django.db.models.deletion.CASCADE, to='author.designation')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(help_text='Max size of file: 20MB.', storage=storages.backends.ftp.FTPStorage(), upload_to='assets')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='InstituteType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True, verbose_name='Institute Type')),
            ],
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True, verbose_name='Municipality Name')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Subject')),
            ],
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Zone Name')),
                ('municipal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='complain_box.municipality', verbose_name='Municipality')),
            ],
        ),
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Institute Name')),
                ('address', models.CharField(max_length=250, verbose_name='Address')),
                ('institute_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='complain_box.institutetype', verbose_name='Institute Type')),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='complain_box.zone', verbose_name='Zone')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('complain', models.ForeignKey(help_text='Select the complaint for which feedback is given.', on_delete=django.db.models.deletion.CASCADE, to='complain_box.complaint')),
                ('parent', models.ForeignKey(blank=True, help_text='Parent feedback in the reply chain.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='complain_box.feedback')),
                ('user', models.ForeignKey(blank=True, help_text='Select the user providing the feedback.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='complaint',
            name='file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='complain_box.file'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='institute',
            field=models.ForeignKey(help_text='Select the institute associated with the complaint.', on_delete=django.db.models.deletion.CASCADE, to='complain_box.institute'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='student_class',
            field=models.ForeignKey(help_text='Select the class of the student involved.', on_delete=django.db.models.deletion.CASCADE, to='complain_box.class'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='subject',
            field=models.ForeignKey(help_text='Select the subject or topic of the complaint.', on_delete=django.db.models.deletion.CASCADE, to='complain_box.subject'),
        ),
    ]