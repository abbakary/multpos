# Generated migration to add WhatsApp field to Customer model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_alter_customer_customer_type_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='whatsapp',
            field=models.CharField(blank=True, help_text='WhatsApp number (if different from phone)', max_length=20, null=True),
        ),
    ]