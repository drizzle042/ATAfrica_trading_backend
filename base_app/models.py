from django.db import models
from django.contrib.auth.hashers import make_password


class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.TextField(max_length=50)
    first_name = models.TextField()
    last_name = models.TextField()
    is_authenticated = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.last_name} {self.first_name}'

    def save(self, *args, **kwargs):
        self.first_name = str(self.first_name).strip().title()
        self.last_name = str(self.last_name).strip().title()
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    class Meta:
        db_table = 'user'


class Accounts(models.Model):
    user = models.ForeignKey(to='base_app.User', on_delete=models.CASCADE)
    server = models.CharField(max_length=30)
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    platform = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'accounts'
