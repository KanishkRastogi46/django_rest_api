from django.db import models


# Create your models here
class Color(models.Model):
    color_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.color_name   


class Person(models.Model):
    color = models.ForeignKey(Color, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.age}"