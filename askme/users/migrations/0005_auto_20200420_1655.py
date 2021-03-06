# Generated by Django 3.0.4 on 2020-04-20 13:55

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='temp', max_length=50, unique=True, validators=[users.validators.UsernameValidator()], verbose_name='Username for profile page'),
            preserve_default=False,
        ),
    ]
