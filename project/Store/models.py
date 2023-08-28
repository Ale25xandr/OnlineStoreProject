import datetime

from django.db import models
from django.contrib.auth.models import User


class Ads(models.Model):
    category_title = [("Танки", 'Танки'), ("ДД", "ДД"), ("Квестгиверы", "Квестгиверы"), ("Хилы", "Хилы"),
                      ("Торговцы", "Торговцы"),
                      ("Гилдмастеры", "Гилдмастеры"), ("Кузнецы", "Кузнецы"), ("Кожевники", "Кожевники"),
                      ("Зельевары", "Зельевары"), ("Мастера заклинаний", "Мастера заклинаний")]
    Heading = models.CharField(max_length=255)
    Description = models.TextField()
    Content = models.TextField(null=True)
    Category = models.CharField(max_length=255, choices=category_title, default='1')
    Author = models.ForeignKey(User, on_delete=models.CASCADE)
    Date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Heading

    def res(self):
        return len(Response.objects.filter(ads=self.id))

    def r(self):
        if Response.objects.filter(ads=self.id) is not None:
            return True
        else:
            return False


class Response(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    Text = models.TextField()
    Accepted = models.BooleanField(default=False)
    ads = models.ForeignKey(Ads, on_delete=models.CASCADE, null=True, blank=True)
    Date = models.DateTimeField(auto_now_add=True)

    def a(self):
        return User.objects.get(username=self.author)


class Code(models.Model):
    code = models.IntegerField(unique=True, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_ok = models.BooleanField(default=False, blank=True)
