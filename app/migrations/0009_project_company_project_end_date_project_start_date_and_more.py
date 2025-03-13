# Generated by Django 5.1.4 on 2025-03-13 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0008_certification_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="company",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="project",
            name="end_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="project",
            name="start_date",
            field=models.DateField(default="2000-01-01"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="experience",
            name="end_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="formation",
            name="end_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
