from rest_framework.viewsets import ViewSet

from rest_framework.response import Response

from bsolutions.domain.models.purchase import Compra


class AllCompras(ViewSet):

    def list(self, request):
        db = request.GET.get('db', 'default')
        limit = request.GET.get('limit', 100)
        list(Compra.objects.using(db).all()[:int(limit)])
        return Response({'db': db})
