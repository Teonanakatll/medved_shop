from django.db import models

class Subscriber(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=128)

    def __str__(self):
        # Вывод имени и емейла
        return "Пользователь %s %s" % (self.name, self.email)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
