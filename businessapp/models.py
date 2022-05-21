from django.db import models
from django.utils.translation import gettext_lazy as _
from auth_user.models import User
# Create your models here.


class Projects(models.Model):
    BUSINESS_TYPE = (
        ("STARTUP", "Start up"),
        ("FRANCHISE", "Franchise"),
        ("READY BUSINESSES", "Ready businesses")
    )
    title = models.CharField(_('title project'), max_length=250,)
    image = models.ImageField(_('image project'), upload_to='projects', null=True, blank=True)
    definition = models.TextField(_("definition project"), blank=True, null=True)
    cost_investments = models.FloatField(_("investments project"))
    is_active = models.BooleanField(default=False, blank=True, null=True)
    age_business = models.FloatField(_('age business'), blank=True, null=True)
    number_employees = models.IntegerField(_("the number of employees"), default=1)
    organizational_type = models.CharField(_('Organizational and legal form'), max_length=250, default='OOO',
                                           help_text='its legal status and business goals arising from this')
    business_type = models.CharField(choices=BUSINESS_TYPE, default=BUSINESS_TYPE[0][0], max_length=250)
    is_delete = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)

    def __str__(self):
        return f'{self.title}  {self.business_type}'

    class Meta:
        ordering = ['id']
