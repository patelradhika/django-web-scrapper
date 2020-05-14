from django.db import models

# Create your models here.
class Search(models.Model):

    __tablename__ = 'searches'
    
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.search

    def as_dict(self):
        return {'search': self.search}

    class Meta:
        verbose_name_plural = 'Searches'