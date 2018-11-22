from rest_framework.viewsets import ViewSet

from rest_framework.response import Response

from bsolutions.domain.models.purchase import Compra


class AllCompras(ViewSet):

    def list(self, request):
        db = request.GET.get('db', 'default')
        list(Compra.objects.using(db).all()[:1000])
        return Response({'db': db})
