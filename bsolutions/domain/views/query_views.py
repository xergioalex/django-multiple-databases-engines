from rest_framework.viewsets import ViewSet

from rest_framework.response import Response

from bsolutions.domain.models.purchase import Compra


class AllCompras(ViewSet):

    def list(self, request):
        Compra.objects.all().count()
        return Response({})
