# Generated by Django 4.0 on 2021-12-29 06:22

from django.db import migrations, models
import django.db.models.deletion
import fleetmanager.model_helpers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pattern_key', models.CharField(max_length=50, null=True)),
                ('model_name', models.CharField(max_length=20, null=True)),
                ('attributes', models.JSONField(null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'rules',
            },
            bases=(models.Model, fleetmanager.model_helpers.BaseMethod),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('data_signature', models.CharField(max_length=80, null=True)),
                ('status', models.CharField(choices=[('created', 'Created'), ('complete', 'Complete'), ('canceled', 'Canceled')], max_length=15, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assigned_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_assigned_to', to='customer_management.customer')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_created_by', to='customer_management.customer')),
                ('rule', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='task_management.rule')),
            ],
            options={
                'db_table': 'tasks',
            },
            bases=(models.Model, fleetmanager.model_helpers.BaseMethod),
        ),
        migrations.AddIndex(
            model_name='rule',
            index=models.Index(fields=['pattern_key'], name='rules_pattern_59d06b_idx'),
        ),
        migrations.AddIndex(
            model_name='rule',
            index=models.Index(fields=['model_name'], name='rules_model_n_1eedf3_idx'),
        ),
        migrations.AddIndex(
            model_name='rule',
            index=models.Index(fields=['created_on'], name='rules_created_a0affe_idx'),
        ),
        migrations.AddIndex(
            model_name='rule',
            index=models.Index(fields=['updated_at'], name='rules_updated_c5117c_idx'),
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['name'], name='tasks_name_134490_idx'),
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['status'], name='tasks_status_031d4c_idx'),
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['data_signature'], name='tasks_data_si_0a88de_idx'),
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['created_by'], name='tasks_created_816ff3_idx'),
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['assigned_to'], name='tasks_assigne_00feb5_idx'),
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['created_on'], name='tasks_created_e2f654_idx'),
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['updated_at'], name='tasks_updated_57f1b1_idx'),
        ),
    ]
