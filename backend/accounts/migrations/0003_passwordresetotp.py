from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordResetOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(db_index=True, max_length=254)),
                ('code_hash', models.CharField(max_length=128)),
                ('expires_at', models.DateTimeField()),
                ('attempts', models.PositiveSmallIntegerField(default=0)),
                ('used_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [
                    models.Index(fields=['email', 'created_at'], name='accounts_pa_email_3c70d1_idx'),
                    models.Index(fields=['expires_at'], name='accounts_pa_expires_0af7fd_idx'),
                ],
            },
        ),
    ]
