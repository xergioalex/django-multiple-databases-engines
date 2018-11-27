from django.db.models.aggregates import Count, Sum
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

from rest_framework.response import Response

from bsolutions.domain.models.cassandra_models import BeaconLogs
from bsolutions.domain.models.interaction import Interaccion
from bsolutions.domain.models.product import Producto
from bsolutions.domain.models.product_type import TipoProducto
from bsolutions.domain.models.profile import Cliente
from bsolutions.domain.models.purchase import Compra


class AllCompras(ViewSet):

    def list(self, request):
        db = request.GET.get('db', 'default')
        limit = request.GET.get('limit', 100)
        list(Compra.objects.using(db).all()[:int(limit)])
        return Response({'db': db})

    @action(methods=['GET'], detail=False)
    def get_ventas_de_un_usuario(self, request):
        db = request.GET.get('db', 'default')
        limit = request.GET.get('limit', 100)
        Cliente.objects.filter(interaccion__materializado=True)
        list(Producto.objects.using(db).filter(compraproducto__compra__cliente__in=Cliente.objects.using(db).all()[:int(limit)]))
        return Response({})

    @action(methods=['GET'], detail=False)
    def numero_de_ventas_por_producto(self, request):
        db = request.GET.get('db', 'default')
        limit = int(request.GET.get('limit', 100))
        list(Producto.objects.using(db).all()[:limit].annotate(total_ventas=Sum('compraproducto__cantidad')))
        return Response({})

    @action(methods=['GET'], detail=False)
    def numero_notificaciones_por_producto(self, request):
        db = request.GET.get('db', 'default')
        limit = int(request.GET.get('limit', 100))
        list(Producto.objects.using(db).all()[:limit].annotate(total_ventas=Count('notificacion')))
        return Response({})

    @action(methods=['GET'], detail=False)
    def interacciones_materializadas(self, request):
        db = request.GET.get('db', 'default')
        limit = int(request.GET.get('limit', 100))
        query = Interaccion.objects.using(db).filter(materializado=True)[:limit]
        query.count()
        list(query)
        return Response({})

    @action(methods=['GET'], detail=False)
    def numero_interacciones_por_clientes(self, request):
        db = request.GET.get('db', 'default')
        limit = int(request.GET.get('limit', 100))
        list(Cliente.objects.using(db).all()[:limit].annotate(total_interacciones=Count('interaccion')))
        return Response({})

    @action(methods=['GET'], detail=False)
    def ventas_por_tipo_de_producto(self, request):
        db = request.GET.get('db', 'default')
        limit = int(request.GET.get('limit', 100))
        list(TipoProducto.objects.using(db).all()[:limit].annotate(total_tipo_producto=Sum('producto__compraproducto__cantidad')))
        return Response({})

    @action(methods=['GET'], detail=False)
    def ventas_por_trimestre(self, request):
        db = request.GET.get('db', 'default')
        limit = int(request.GET.get('limit', 100))
        list(BeaconLogs.objects.all().limit(int(limit)))
        return Response({})

    @action(methods=['GET'], detail=False)
    def interacciones_por_trimestre(self, request):
        db = request.GET.get('db', 'default')
        limit = int(request.GET.get('limit', 100))
        list(BeaconLogs.objects.all().limit(int(limit)))
        return Response({})
    @action(methods=['GET'], detail=False)
    def ventas_por_rango_de_edad(self, request):
        db = request.GET.get('db', 'default')
        limit = int(request.GET.get('limit', 100))
        list(BeaconLogs.objects.all().limit(int(limit)))
        return Response({})

    @action(methods=['GET'], detail=False)
    def ventas_por_genero(self, request):
        db = request.GET.get('db', 'default')
        limit = int(request.GET.get('limit', 100))
        list(BeaconLogs.objects.all().limit(int(limit)))
        return Response({})
