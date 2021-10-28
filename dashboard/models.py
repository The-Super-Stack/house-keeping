from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from .utils import generate_code
from django.utils.timezone import now

gender_choices = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('X', 'Unknown')
]


class WorkingStatus(models.Model):
    status = models.CharField(max_length=255, verbose_name='status bekerja sekarang : ')

    def __str__(self):
        return self.status


class WorkPlace(models.Model):
    buildings = models.CharField(max_length=255, verbose_name='Nama Gedung : ')
    tower_name = models.CharField(max_length=255, verbose_name='Nama Tower : ')
    ground_name = models.CharField(max_length=255, verbose_name='Nama Lantai : ')
    job_area = models.CharField(max_length=255, verbose_name='Zona Kerja : ')
    qr_code = models.TextField(verbose_name='unique code QR', default=generate_code())
    qr_img = models.FileField(verbose_name='QR Code Image', upload_to='qr/', blank=True, null=True)

    def __str__(self):
        return f"{self.buildings} -- {self.job_area}"

    def naming(self):
        return self.job_area

    def save(self, *args, **kwargs):
        code_img = qrcode.make(self.qr_code)
        canvas = Image.new('RGB', (600, 600), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(code_img)
        fname = f"qr_code_{self.qr_code}.png"
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_img.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)


class EmployeeManagement(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='emp_user', related_query_name='emp_user')
    nik = models.CharField(unique=True, verbose_name='NIK : ', max_length=255)
    is_employee = models.BooleanField(default=True)
    is_supervisor = models.BooleanField(default=False)
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default='', null=True)
    shift = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=255, verbose_name='nomor telepon : ')
    profile_img = models.FileField(upload_to='profile/')
    gender = models.CharField(max_length=10, choices=gender_choices, default='X')
    status = models.ForeignKey(WorkingStatus, on_delete=models.CASCADE)

    def __str__(self):
        if self.is_employee and self.is_supervisor:
            return f"{self.user} is supervisor "
        elif self.is_employee and not self.is_supervisor:
            return f"{self.user} just employee "


class AssignmentControl(models.Model):
    assignment = models.ForeignKey(WorkPlace, on_delete=models.CASCADE, blank=True, verbose_name='Tugas yang akan diberikan : ')
    access_permission = models.BooleanField(default=False)
    worker = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    estimated_time = models.IntegerField(default=0, verbose_name='Lama waktu pengerjaan : ')
    for_day = models.DateField(default=now(), verbose_name='Untuk dikerjakan pada tanggal : ')
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    on_progress = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    img_before = models.FileField(upload_to='assignment/before/', blank=True)
    img_after = models.FileField(upload_to='assignment/after/', blank=True)

    def __str__(self):
        if self.on_progress:
            return f"{self.assignment.naming()} is being cleaned by {self.worker.username} | wait for {self.estimated_time} minutes"
        elif self.is_done:
            return f"{self.assignment.naming()} has been cleaned {self.worker.username}"
        elif not self.is_done and not self.on_progress:
            return f"{self.assignment.naming()} will be cleaned {self.worker.username}"
