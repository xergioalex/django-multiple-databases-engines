# Generated by Django 2.0.9 on 2018-11-15 04:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Beacon',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('referencia', models.CharField(max_length=45)),
                ('modelo', models.CharField(max_length=45)),
                ('ubicacion', models.CharField(max_length=45)),
            ],
            options={
                'verbose_name_plural': 'beacons',
                'db_table': 'beacon',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=45)),
                ('correo', models.EmailField(max_length=45)),
                ('documento', models.CharField(max_length=20)),
                ('tipoDocumento', models.IntegerField(choices=[(1, 'Cédula de ciudadanía'), (2, 'Tarjeta de identidad'), (3, 'Pasaporte'), (4, 'Cédula de extranjería')])),
                ('genero', models.CharField(choices=[('F', 'Femenino'), ('M', 'Masculino')], max_length=1, null=True)),
                ('edad', models.PositiveIntegerField()),
                ('direccion', models.CharField(max_length=80, null=True)),
                ('telefono', models.CharField(max_length=20, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cliente',
            },
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('medioPago', models.IntegerField(choices=[(1, 'Efectivo'), (2, 'Tarjeta de debito'), (3, 'Tarjeta de credito')])),
                ('descuento', models.FloatField(default=0.0, null=True)),
                ('cliente', models.ForeignKey(db_column='idCliente', on_delete=django.db.models.deletion.CASCADE, to='domain.Cliente')),
            ],
            options={
                'verbose_name_plural': 'products',
                'db_table': 'compra',
            },
        ),
        migrations.CreateModel(
            name='CompraProducto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('descuento', models.FloatField(default=0.0, null=True)),
                ('compra', models.ForeignKey(db_column='idCompra', on_delete=django.db.models.deletion.CASCADE, to='domain.Compra')),
            ],
            options={
                'verbose_name_plural': 'products',
                'db_table': 'compra_producto',
            },
        ),
        migrations.CreateModel(
            name='Interaccion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('materializado', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(db_column='idCliente', on_delete=django.db.models.deletion.CASCADE, to='domain.Cliente')),
            ],
            options={
                'verbose_name_plural': 'beacons',
                'db_table': 'interaccion',
            },
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('mensaje', models.TextField()),
                ('beacon', models.ForeignKey(db_column='idBeacon', on_delete=django.db.models.deletion.CASCADE, to='domain.Beacon')),
            ],
            options={
                'verbose_name_plural': 'notifications',
                'db_table': 'notificacion',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=45)),
                ('referencia', models.CharField(max_length=45)),
                ('precio', models.FloatField()),
                ('costo', models.FloatField()),
            ],
            options={
                'verbose_name_plural': 'products',
                'db_table': 'producto',
            },
        ),
        migrations.CreateModel(
            name='TipoProducto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=45)),
            ],
            options={
                'verbose_name_plural': 'product_types',
                'db_table': 'tipo_producto',
            },
        ),
        migrations.AddField(
            model_name='producto',
            name='tipoProducto',
            field=models.ForeignKey(db_column='idTipoProducto', on_delete=django.db.models.deletion.CASCADE, to='domain.TipoProducto'),
        ),
        migrations.AddField(
            model_name='notificacion',
            name='producto',
            field=models.ForeignKey(db_column='idProducto', null=True, on_delete=django.db.models.deletion.CASCADE, to='domain.Producto'),
        ),
        migrations.AddField(
            model_name='interaccion',
            name='notificacion',
            field=models.ForeignKey(db_column='idNotificacion', on_delete=django.db.models.deletion.CASCADE, to='domain.Notificacion'),
        ),
        migrations.AddField(
            model_name='compraproducto',
            name='producto',
            field=models.ForeignKey(db_column='idProducto', on_delete=django.db.models.deletion.CASCADE, to='domain.Producto'),
        ),
    ]
