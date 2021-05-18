# Generated by Django 3.2.3 on 2021-05-18 06:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original', models.ImageField(upload_to='')),
                ('thumbnail_m', models.ImageField(upload_to='images/thumbnails/m')),
                ('thumbnail_s', models.ImageField(upload_to='images/thumbnails/s')),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('basic', 'Basic'), ('enterprise', 'Enterprise'), ('premium', 'Premium')], default='basic', max_length=16)),
                ('thumbnail_s_size', models.PositiveIntegerField()),
                ('thumbnail_m_size', models.PositiveIntegerField()),
                ('create_expire', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ManyToManyField(to='images.Image')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='images.plan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
