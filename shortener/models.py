from django.conf import settings
from django.db import models
from .utils import create_shortcode
# Create your models here.
from .validators import validate_url

SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 15)

class KirrURLManager(models.Manager):
    def all(self, *args, **kwargs):
        qs = super(KirrURLManager, self).all(*args, **kwargs)
        qs = qs.filter(active=True)
        return qs

    def refresh_shortcodes(self, items=None):
        qs = KirrURL.objects.filter(id__gte=1) # equal to all (without our filter)
        if items is not None and isinstance(items, int):
            qs = qs.order_by('id')[:items]
        new_codes = 0
        for q in qs:
            q.shortcode = create_shortcode(q)
            q.save()
            new_codes += 1
        return "New codes made: {i}".format(i=new_codes)

class KirrURL(models.Model):
    url = models.CharField(max_length=220, validators=[validate_url,])
    shortcode = models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = KirrURLManager()


    def save(self, *args, **kargs):
        if self.shortcode is None or self.shortcode == "":
            self.shortcode = create_shortcode(self) 
        super(KirrURL, self).save(*args, **kargs)

    def __str__(self):
        return str([self.url, self.shortcode])

    def get_short_url(self):
        return "http://127.0.0.1:8000/{shortcode}".format(shortcode=self.shortcode)