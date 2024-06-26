# Generated by Django 5.0.3 on 2024-05-30 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliation_app', '0001_initial'),
        ('profile_app', '0002_profile_affiliations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='affiliations',
            field=models.ManyToManyField(blank=True, related_name='affiliations', to='affiliation_app.affiliation'),
        ),
    ]
