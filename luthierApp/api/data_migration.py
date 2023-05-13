from django.db import migrations
from functools import partial

dict_table_data = [
    {
        'model_name': 'PaymentMethod',
        'data': ['visa', 'mastercard']
    },
    {
        'model_name':
        'Status',
        'data': [
            'new',
            'luthier_agree_price',
            'customer_shipping',
            'customer_rejected',
            'luthier_job_in_progress',
            'luthier_shipping',
            'done',
            'request_more_info',
            'warn_solve_manually',
        ]
    },
    {
        'model_name':
        'Brand',
        'data': [
            'epiphone', 'gibson', 'furch', 'martin', 'gretsch', 'ibanez',
            'fender'
        ]
    },
    {
        'model_name': 'Category',
        'data': ['guitar', 'bass', 'violin']
    },
    {
        'model_name': 'UserRole',
        'data': ['customer', 'luthier']
    },
]


def populate_dict_table(
    apps,
    schema_editor,
    names,
    model_name,
    app_name,
):
    rows = []
    model = apps.get_model(app_name, model_name)
    for name in names:
        row_to_append = model(name=name)
        rows.append(row_to_append)

    model.objects.bulk_create(rows)


def create_superuser():
    ...


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            partial(populate_dict_table,
                    names=d['data'],
                    model_name=d['model_name'],
                    app_name='api')) for d in dict_table_data
    ]
    operations = []
