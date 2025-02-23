from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
# Create your models here.

class Task(models.Model):
    task = models.TextField()
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    priority = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    deadline = models.DateField()
    memo = models.TextField(null=True)
    comp_flg = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task

    def get_absolute_url(self):
        return reverse("task:index")