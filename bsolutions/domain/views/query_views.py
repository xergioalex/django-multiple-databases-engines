from rest_framework.viewsets import ViewSet

from rest_framework.response import Response

from bsolutions.domain.models.purchase import Compra


class AllCompras(ViewSet):

    def list(self, request):
        db = request.GET.get('db', 'default')
        list(Compra.objects.all()[:100000])
        return Response({'db': db})
