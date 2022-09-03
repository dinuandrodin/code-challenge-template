from django.db import models


class WeatherData(models.Model):
    date = models.DateField()
    max_temp = models.DecimalField(max_digits=4, decimal_places=1)
    min_temp = models.DecimalField(max_digits=4, decimal_places=1)
    precipitation = models.DecimalField(max_digits=4, decimal_places=1)

    class Meta:
        unique_together = ['date', 'max_temp', 'min_temp', 'precipitation']


class Statistics(models.Model):
    year = models.PositiveSmallIntegerField()
    avg_max_temp = models.FloatField(null=True)
    avg_min_temp = models.FloatField(null=True)
    total_precipitation = models.FloatField(null=True)
