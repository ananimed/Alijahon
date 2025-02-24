# Generated by Django 5.0.7 on 2024-08-12 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0008_stream_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deliver_price', models.FloatField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='stream',
            name='status',
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('new', 'New'), ('preparing', 'Preparing for Dispatch'), ('shipping', 'Shipping'), ('delivered', 'Delivered'), ('no_answer', 'No Answer'), ('cancelled', 'Cancelled'), ('archived', 'Archived')], default='new', max_length=20),
        ),
    ]
