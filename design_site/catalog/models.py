import django
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    fio = models.CharField(max_length=100)
    email =  models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class DesignCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Request(models.Model):
    objects = None
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        max_size = 2.0
        if filesize > max_size * 1024 * 1024:
            raise ValidationError("Максимальный размер файла 2 МБ")
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(DesignCategory, on_delete=models.CASCADE, verbose_name='Категория')
    REQUEST_STATUS = (
        ('new', 'Новая'),
        ('process', 'Принято в работу'),
        ('made', 'Выполнено'),
    )
    status = models.CharField(
        max_length=25,
        choices=REQUEST_STATUS,
        blank=True,
        verbose_name="Статус заявки",
        default='new')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    request_photo = models.ImageField(max_length=254, upload_to="media/", verbose_name="Фотография",
                                      help_text="Разрешается формата файла только jpg, jpeg, png, bmp",
                                      validators=[
                                          FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp']),
                                          validate_image])
    date = models.DateTimeField(default=django.utils.timezone.now)
    design_file = models.ImageField(upload_to='media/',
                                   validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png', 'bmp']),
                                               validate_image], blank=True)
    comment = models.TextField(blank=True)
    def __str__(self):
        return self.title


