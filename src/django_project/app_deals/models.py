from django.db import models


class Deals(models.Model):
    date = models.DateTimeField('Date')
    customer = models.CharField('Customer', max_length=32)
    gem = models.CharField('Gem', max_length=64)
    quantity = models.PositiveIntegerField('Quantity')
    total = models.DecimalField('Total', max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.customer}, {self.quantity}, {self.gem}'

    class Meta:
        verbose_name = 'Deal'
        verbose_name_plural = 'Deals'


