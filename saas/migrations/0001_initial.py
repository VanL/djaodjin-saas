# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-10-18 13:50
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('title', models.CharField(max_length=150, unique=True)),
                ('modified', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='BalanceLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.SlugField()),
                ('title', models.CharField(max_length=255)),
                ('selector', models.CharField(max_length=255)),
                ('rank', models.IntegerField()),
                ('moved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='date/time at which the item was added to the cart.')),
                ('recorded', models.BooleanField(default=False, help_text='whever the item has been checked out or not.')),
                ('nb_periods', models.PositiveIntegerField(default=0)),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('claim_code', models.SlugField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Charge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('amount', models.PositiveIntegerField(default=0, help_text='Amount in cents')),
                ('unit', models.CharField(default='usd', max_length=3)),
                ('description', models.TextField(null=True)),
                ('last4', models.PositiveSmallIntegerField()),
                ('exp_date', models.DateField()),
                ('processor_key', models.SlugField(unique=True)),
                ('state', models.PositiveSmallIntegerField(choices=[(3, 'disputed'), (1, 'done'), (2, 'failed'), (0, 'created')], default=0)),
                ('extra', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChargeItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('charge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='charge_items', to='saas.Charge')),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('code', models.SlugField()),
                ('description', models.TextField(blank=True, null=True)),
                ('percent', models.PositiveSmallIntegerField(default=0, help_text='Percentage discounted', validators=[django.core.validators.MaxValueValidator(100)])),
                ('ends_at', models.DateTimeField(blank=True, null=True)),
                ('nb_attempts', models.IntegerField(blank=True, help_text='Number of times the coupon can be used', null=True)),
                ('extra', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(help_text='Unique identifier shown in the URL bar.', unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_bulk_buyer', models.BooleanField(default=False, help_text='Enable GroupBuy (<a href="/docs/#group-billing" target="_blank">what is it?</a>)')),
                ('is_provider', models.BooleanField(default=False, help_text='Can fulfill the provider side of a subscription.')),
                ('full_name', models.CharField(blank=True, max_length=60, verbose_name='full name')),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=50)),
                ('street_address', models.CharField(max_length=150)),
                ('locality', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=50)),
                ('postal_code', models.CharField(max_length=50)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('billing_start', models.DateField(auto_now_add=True, null=True)),
                ('funds_balance', models.PositiveIntegerField(default=0, help_text='Funds escrowed in cents')),
                ('processor_card_key', models.CharField(blank=True, max_length=20, null=True)),
                ('processor_deposit_key', models.CharField(blank=True, help_text='Used to deposit funds to the organization bank account', max_length=60, null=True)),
                ('processor_priv_key', models.CharField(blank=True, max_length=60, null=True)),
                ('processor_pub_key', models.CharField(blank=True, max_length=60, null=True)),
                ('processor_refresh_token', models.CharField(blank=True, max_length=60, null=True)),
                ('extra', models.TextField(null=True)),
                ('processor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='processes', to='saas.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('title', models.CharField(max_length=50, null=True)),
                ('description', models.TextField()),
                ('is_active', models.BooleanField(default=False)),
                ('is_not_priced', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('discontinued_at', models.DateTimeField(blank=True, null=True)),
                ('unit', models.CharField(default='usd', max_length=3)),
                ('setup_amount', models.PositiveIntegerField(default=0, help_text='One-time charge amount (in cents).')),
                ('period_amount', models.PositiveIntegerField(default=0, help_text='Recurring amount per period (in cents).')),
                ('transaction_fee', models.PositiveIntegerField(default=0, help_text='Fee per transaction (in per 10000).')),
                ('interval', models.PositiveSmallIntegerField(choices=[(1, 'HOURLY'), (2, 'DAILY'), (3, 'WEEKLY'), (4, 'MONTHLY'), (5, 'YEARLY')], default=5)),
                ('period_length', models.PositiveSmallIntegerField(default=1, help_text='Natural number of months/years/etc. before the plan ends')),
                ('unlock_event', models.CharField(blank=True, help_text='Payment required to access full service', max_length=128, null=True)),
                ('advance_discount', models.PositiveIntegerField(default=333, help_text='incr discount for payment of multiple periods (in %%).', validators=[django.core.validators.MaxValueValidator(10000)])),
                ('length', models.PositiveSmallIntegerField(blank=True, help_text='Number of intervals the plan before the plan ends.', null=True)),
                ('auto_renew', models.BooleanField(default=True)),
                ('extra', models.TextField(null=True)),
                ('next_plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='saas.Plan')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plans', to='saas.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('request_key', models.CharField(blank=True, max_length=40, null=True)),
                ('grant_key', models.CharField(blank=True, max_length=40, null=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saas.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='RoleDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=20)),
                ('slug', models.SlugField(help_text='Unique identifier shown in the URL bar.')),
                ('extra', models.TextField(null=True)),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='role_descriptions', to='saas.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_signed', models.DateTimeField(auto_now_add=True)),
                ('agreement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saas.Agreement')),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='signatures', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auto_renew', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ends_at', models.DateTimeField()),
                ('description', models.TextField(blank=True, null=True)),
                ('extra', models.TextField(null=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saas.Organization')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saas.Plan')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('orig_account', models.CharField(default='unknown', max_length=255)),
                ('orig_amount', models.PositiveIntegerField(default=0, help_text='amount withdrawn from origin in origin units')),
                ('orig_unit', models.CharField(default='usd', help_text='Measure of units on origin account', max_length=3)),
                ('dest_account', models.CharField(default='unknown', max_length=255)),
                ('dest_amount', models.PositiveIntegerField(default=0, help_text='amount deposited into destination in destination units')),
                ('dest_unit', models.CharField(default='usd', help_text='Measure of units on destination account', max_length=3)),
                ('descr', models.TextField(default='N/A')),
                ('event_id', models.SlugField(help_text='Event at the origin of this transaction (ex. job, charge, etc.)', null=True)),
                ('dest_organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming', to='saas.Organization')),
                ('orig_organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing', to='saas.Organization')),
            ],
        ),
        migrations.AddField(
            model_name='role',
            name='role_description',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='saas.RoleDescription'),
        ),
        migrations.AddField(
            model_name='role',
            name='user',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='organization',
            name='subscriptions',
            field=models.ManyToManyField(related_name='subscribes', through='saas.Subscription', to='saas.Plan'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saas.Organization'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='saas.Plan'),
        ),
        migrations.AddField(
            model_name='chargeitem',
            name='invoiced',
            field=models.ForeignKey(help_text='transaction invoiced through this charge', on_delete=django.db.models.deletion.CASCADE, related_name='invoiced_item', to='saas.Transaction'),
        ),
        migrations.AddField(
            model_name='chargeitem',
            name='invoiced_distribute',
            field=models.ForeignKey(help_text='transaction recording the distribution from processor to provider.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoiced_distribute', to='saas.Transaction'),
        ),
        migrations.AddField(
            model_name='chargeitem',
            name='invoiced_fee',
            field=models.ForeignKey(help_text='fee transaction to process the transaction invoiced through this charge', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoiced_fee_item', to='saas.Transaction'),
        ),
        migrations.AddField(
            model_name='charge',
            name='customer',
            field=models.ForeignKey(help_text='organization charged', on_delete=django.db.models.deletion.CASCADE, to='saas.Organization'),
        ),
        migrations.AddField(
            model_name='charge',
            name='processor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='charges', to='saas.Organization'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='coupon',
            field=models.ForeignKey(blank=True, help_text='coupon to apply to the plan.', null=True, on_delete=django.db.models.deletion.CASCADE, to='saas.Coupon'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='plan',
            field=models.ForeignKey(help_text='item added to the cart.', null=True, on_delete=django.db.models.deletion.CASCADE, to='saas.Plan'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='user',
            field=models.ForeignKey(db_column='user_id', help_text='user who added the item to the cart. ``None`` means the item could be claimed.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='balanceline',
            unique_together=set([('report', 'rank', 'moved')]),
        ),
        migrations.AlterUniqueTogether(
            name='signature',
            unique_together=set([('agreement', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='roledescription',
            unique_together=set([('organization', 'slug')]),
        ),
        migrations.AlterUniqueTogether(
            name='role',
            unique_together=set([('organization', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='plan',
            unique_together=set([('slug', 'organization')]),
        ),
        migrations.AlterUniqueTogether(
            name='coupon',
            unique_together=set([('organization', 'code')]),
        ),
        migrations.AlterUniqueTogether(
            name='chargeitem',
            unique_together=set([('charge', 'invoiced')]),
        ),
    ]
