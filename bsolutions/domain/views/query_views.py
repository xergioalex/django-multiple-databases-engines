import time
from django.db.models.aggregates import Count, Sum
from django.db.models.expressions import F
from django.db.models.functions.datetime import TruncMonth
from neomodel.match import QueryBuilder, NodeSet
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

from rest_framework.response import Response

from bsolutions.domain.documents.beacon_logs import BeaconLogsDocument
from bsolutions.domain.models.interaction import Interaccion
from bsolutions.domain.models.product import Producto
from bsolutions.domain.models.product_type import TipoProducto
from bsolutions.domain.models.profile import Cliente
from bsolutions.domain.models.purchase import Compra
from bsolutions.domain.neomodels.social_logs import BeaconNode, PersonaNode


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
        Producto.objects.using(db).filter(compraproducto__compra__cliente__in=Cliente.objects.using(db).all()[:int(limit)])
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
    def ventas_por_mes(self, request):
        db = request.GET.get('db', 'default')
        list(Compra.objects.using(db).annotate(
            month=TruncMonth('fecha')
        ).values('month').annotate(total=Count('id')).values('month', 'total'))
        return Response({})

    @action(methods=['GET'], detail=False)
    def interacciones_por_mes(self, request):
        db = request.GET.get('db', 'default')
        list(Interaccion.objects.using(db).annotate(
            month=TruncMonth('fecha')
        ).values('month').annotate(total=Count('id')).values('month', 'total'))

        return Response({})

    @action(methods=['GET'], detail=False)
    def ventas_por_rango_de_edad(self, request):
        db = request.GET.get('db', 'default')
        list(Cliente.objects.using(db).all().annotate(
            rango=F('edad') / 10
        ).values('rango').annotate(total=Count('compra')).values('rango', 'total'))
        return Response({})

    @action(methods=['GET'], detail=False)
    def ventas_por_genero(self, request):
        db = request.GET.get('db', 'default')
        list(Cliente.objects.using(db).all().values('genero').annotate(total=Count('compra')).values('genero', 'total'))
        return Response({})


class AllDocumentedMongoViews(ViewSet):

    @action(methods=['GET'], detail=False)
    def beacon_logs(self, request):
        limit = int(request.GET.get('limit', 100))
        query = BeaconLogsDocument.objects.all()[:limit]
        start_time = time.time()
        list(query)
        a = []
        for b in query[:10]:
            c = b.to_mongo().to_dict()
            c['_id'] = str(c['_id'])
            c['interaccion']['fecha'] =str(c['interaccion']['fecha'])
            a.append(c)
        return Response({'time': time.time() - start_time, 'query': query._query, 'parcial_result': a})

    @action(methods=['GET'], detail=False)
    def filtrar_beacons_por_bateria(self, request):
        limit = int(request.GET.get('limit', 1000))
        battery = int(request.GET.get('battery', 40))
        query = BeaconLogsDocument.objects.filter(payload__bateria__lte=battery)[:limit]
        start_time = time.time()
        list(query)
        a = []
        for b in query[:10]:
            c = b.to_mongo().to_dict()
            c['_id'] = str(c['_id'])
            c['interaccion']['fecha'] =str(c['interaccion']['fecha'])
            a.append(c)
        return Response({'time': time.time() - start_time, 'query': query._query, 'parcial_result': a})

    @action(methods=['GET'], detail=False)
    def numero_de_interacciones_por_mes(self, request):
        query = {'$group': {'_id': {'$substr': ['$interaccion.fecha', 5, 2]}, 'total': {'$sum': 1}}}
        queryDocumet = BeaconLogsDocument.objects.all().aggregate(query)
        start_time = time.time()
        list(query)
        return Response({'time': time.time() - start_time, 'query': query, 'parcial_result': list(queryDocumet)})


class AllNeo4jViews(ViewSet):

    @action(methods=['GET'], detail=False)
    def beacons(self, request):
        limit = int(request.GET.get('limit', 100))
        query = BeaconNode.nodes.filter()
        query_language = QueryBuilder(query).build_ast().build_query()
        start_time = time.time()
        list(query[:limit])

        return Response({
            'time': time.time() - start_time,
            'query': query_language
        })

    @action(methods=['GET'], detail=False)
    def persona(self, request):
        limit = int(request.GET.get('limit', 100))
        query = PersonaNode.nodes.filter()
        query_language = QueryBuilder(query).build_ast().build_query()
        start_time = time.time()
        list(query[:limit])

        return Response({
            'time': time.time() - start_time,
            'query': query_language
        })

    @action(methods=['GET'], detail=False)
    def personas_con_interacciones(self, request):
        limit = int(request.GET.get('limit', 100))
        query = PersonaNode.nodes.has(beacons=True)
        query_language = QueryBuilder(query).build_ast().build_query()
        start_time = time.time()
        list(query[:limit])

        return Response({
            'time': time.time() - start_time,
            'query': query_language
        })
