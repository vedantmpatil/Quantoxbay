# Generated by Django 5.2.3 on 2025-06-13 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('category', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('file', models.FileField(upload_to='uploads/products/')),
                ('file_size', models.CharField(blank=True, max_length=20)),
                ('file_type', models.CharField(blank=True, max_length=50)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='uploads/thumbnails/')),
                ('preview_url', models.URLField(blank=True)),
                ('tags', models.CharField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
