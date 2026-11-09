from django.db import migrations

def create_unique_index(apps, schema_editor):
    if schema_editor.connection.vendor == 'mongodb':
        client = schema_editor.connection.connection
        db = client[schema_editor.connection.settings_dict['NAME']]
        db['auth_user'].create_index('email', unique=True, sparse=True)
    else:
        with schema_editor.connection.cursor() as cursor:
            cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS auth_user_email_unique ON auth_user (email);")

def drop_unique_index(apps, schema_editor):
    if schema_editor.connection.vendor == 'mongodb':
        client = schema_editor.connection.connection
        db = client[schema_editor.connection.settings_dict['NAME']]
        try:
            db['auth_user'].drop_index('email_1')
        except Exception:
            pass
    else:
        with schema_editor.connection.cursor() as cursor:
            cursor.execute("DROP INDEX IF EXISTS auth_user_email_unique;")

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_userprofile_failed_otp_attempts_and_more'),
    ]

    operations = [
        migrations.RunPython(create_unique_index, reverse_code=drop_unique_index),
    ]
