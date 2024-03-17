from django.db import models

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=250, null=False, blank=False)
    description = models.CharField(max_length=250, null=False, blank=False)
    is_completed = models.BooleanField(default=False)
    created_at  = models.DateField(auto_now_add=True)

def __str__(self):
    return self.title
