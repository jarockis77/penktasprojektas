from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.urls import reverse

from datetime import date
import uuid
from PIL import Image


# Create your models here.

class Gamintojas(models.Model):
    pavadinimas = models.CharField('Pavadinimas', max_length=50)
    gaminimo_pradzia = models.IntegerField('Pradejo-gaminti')
    aprasymas = HTMLField()

    class Meta:
        verbose_name = 'Gamintojas'
        verbose_name_plural = 'Gamintojai'
        ordering = ['pavadinimas']

    def __str__(self):
        return f"{self.pavadinimas} - {self.gaminimo_pradzia}"

    def display_modeliai(self):
        return ',  '.join(modelis.modelis for modelis in self.modeliai.all()[:3])

    display_modeliai.short_description = "Modeliai"

    def get_absolute_url(self):
        return reverse('gamintojas-vienas-url', args=[str(self.id)])


class Modelis(models.Model):
    modelis = models.CharField('Modelis', max_length=50)
    metai_pasirode = models.IntegerField('Gaminimo-pradzia')
    modelis_aprasymas = HTMLField()
    gamintojas = models.ForeignKey('Gamintojas', on_delete=models.SET_NULL, null=True, related_name='modeliai')
    likutis = models.ManyToManyField('Likutis', help_text="Isrinkite likucio bukle")
    cover = models.ImageField('Virselis', upload_to='covers', null=True, blank=True)

    class Meta:
        verbose_name = 'Modelis'
        verbose_name_plural = 'Modeliai'

    def __str__(self):
        return f"{self.modelis}  --  {self.metai_pasirode}"

    def display_likutis(self):
        return ',  '.join(likutis.name for likutis in self.likutis.all()[:3])

    display_likutis.short_description = "Likutis"

    def get_absolute_url(self):
        return reverse('modelis-vienas-url', args=[str(self.id)])


class Likutis(models.Model):
    name = models.CharField('Pavadinimas', max_length=20, help_text="sukurkite likucio info")

    class Meta:
        verbose_name = 'Likutis'
        verbose_name_plural = 'Likuciai'

    def __str__(self):
        return self.name


class ModelisInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    modelis = models.ForeignKey('Modelis', on_delete=models.CASCADE, related_name='modelisinstance_set')
    planuojama_gauti = models.DateField('Turesime pardavime', null=True, blank=True)

    LIKUCIU_STATUS = (
        ('t', 'Turime sandelyje'),
        ('a', 'Atkeliauja'),
        ('n', 'Neturime'),
        ('r', 'Rezervuota')
    )

    status = models.CharField(
        max_length=1,
        choices=LIKUCIU_STATUS,
        blank=True,
        default='a',
        help_text='Moto statusas'
    )

    klientas = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.planuojama_gauti and date.today() > self.planuojama_gauti:
            return True
        else:
            return False

    class Meta:
        ordering = ['planuojama_gauti']

    def __str__(self):
        # return f"{self.id} -- {self.modelis.modelis} -- {self.modelis.gamintojas}"
        return f"{self.id}"


class ModelisReview(models.Model):
    content = models.TextField('Atsiliepimas', max_length=2000)
    date_created = models.DateTimeField(auto_now_add=True)
    modelis = models.ForeignKey(Modelis, on_delete=models.CASCADE, related_name='modelisreview_set', blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.content


class Profilis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    nuotrauka = models.ImageField(default='no-image.png', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.nuotrauka.path)
        if (img.height > 300) or (img.width > 300):
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)

    class Meta:
        verbose_name = 'Profilis'
        verbose_name_plural = 'Profiliai'
