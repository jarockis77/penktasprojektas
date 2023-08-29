from django.db import models

# Create your models here.

class Gamintojas(models.Model):
    pavadinimas = models.CharField('Pavadinimas', max_length=50)
    gaminimo_pradzia = models.IntegerField('Pradejo-gaminti')
    aprasymas = models.TextField('about', max_length=2000)

    def __str__(self):
        return self.pavadinimas

    class Meta:
        verbose_name_plural = 'Gamintojas'

class Modelis(models.Model):
    modelis = models.CharField('Modelis', max_length=50)
    metai_pasirode = models.IntegerField('Gaminimo-pradzia')
    aprasymas = models.TextField('Aprasymas', max_length=2000)
    gamintojasFK = models.ForeignKey('Gamintojas', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.modelis

    class Meta:
        verbose_name_plural = 'Modelis'
