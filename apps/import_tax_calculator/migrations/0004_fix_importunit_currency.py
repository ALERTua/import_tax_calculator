"""Fix ImportUnit.currency default and verbose_name broken by 0003."""

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("import_tax_calculator", "0003_alter_importunit_currency"),
    ]

    operations = [
        migrations.AlterField(
            model_name="importunit",
            name="currency",
            field=models.CharField(
                choices=[("EUR", "Euro"), ("USD", "US Dollar")],
                default="EUR",
                max_length=3,
                verbose_name="Currency",
            ),
        ),
    ]
