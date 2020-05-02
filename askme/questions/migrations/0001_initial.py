# Generated by Django 3.0.4 on 2020-04-26 20:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answered_on', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Date & time the answer was created')),
                ('content', models.CharField(max_length=1024, verbose_name='The answer')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=512, verbose_name='The question')),
                ('asked_on', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Date & time the question was created')),
                ('hidden', models.BooleanField(blank=True, default=False, verbose_name="Hide question from user's profile page")),
                ('asked_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions_posted', to=settings.AUTH_USER_MODEL)),
                ('asked_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions_received', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='questions.Answer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_answers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='questions.Question'),
        ),
        migrations.AddConstraint(
            model_name='like',
            constraint=models.UniqueConstraint(fields=('answer', 'user'), name='user_liked'),
        ),
    ]