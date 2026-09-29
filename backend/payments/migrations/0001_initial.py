from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_code', models.CharField(choices=[('starter', 'Starter'), ('professional', 'Professional')], max_length=30)),
                ('amount', models.PositiveIntegerField(help_text='Amount in paise.')),
                ('currency', models.CharField(default='INR', max_length=3)),
                ('razorpay_order_id', models.CharField(max_length=80, unique=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=80)),
                ('razorpay_signature', models.CharField(blank=True, max_length=255)),
                ('status', models.CharField(choices=[('created', 'Created'), ('verified', 'Verified'), ('failed', 'Failed'), ('refunded', 'Refunded')], default='created', max_length=20)),
                ('provider_status', models.CharField(blank=True, max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [
                    models.Index(fields=['user', 'status'], name='payments_pa_user_id_8e6ea4_idx'),
                    models.Index(fields=['created_at'], name='payments_pa_created_4c1a7d_idx'),
                ],
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_code', models.CharField(choices=[('free', 'Free'), ('starter', 'Starter'), ('professional', 'Professional'), ('business', 'Business')], default='free', max_length=30)),
                ('status', models.CharField(choices=[('active', 'Active'), ('expired', 'Expired'), ('cancelled', 'Cancelled')], default='active', max_length=20)),
                ('starts_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('ends_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('source_payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscriptions', to='payments.payment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [
                    models.Index(fields=['user', 'status'], name='payments_su_user_id_5d3a4b_idx'),
                    models.Index(fields=['plan_code'], name='payments_su_plan_co_4cc4a9_idx'),
                ],
            },
        ),
    ]
