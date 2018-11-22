from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

from rest_framework.response import Response

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
        list(Cliente.objects.using(db).all()[:int(limit)].prefetch_related('compra_set__compraproducto_set'))
        return Response({})
