from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from history.models import ReservartionHistory
from history.serializer import ReserveListSerialize
from reserva.permissions import IsBooker


class ReserveList(ListAPIView):
    queryset            = ReservartionHistory.objects.filter(is_cancled=False, is_paid=False)
    serializer_class    = ReserveListSerialize
    permission_classes  = [IsAuthenticated]

    def patch(self, request):
        is_paid = request.data.get('is_paid')
        item_pk = request.data.get('pk')
        lastest = ReservartionHistory.objects.filter(pk=item_pk).first()
        data = {
            'pk': item_pk,
            'booker': request.user.id,
            'is_paid': is_paid
        }
        instance = ReserveListSerialize(lastest, data=data, partial=True)
        if instance.is_valid():
            update_data = {
                'is_paid': is_paid,
                'booker': request.user.id
            }
            instance.update(lastest, update_data)
        return Response({'status': 'success'})

    
class BookerReserved(ListAPIView):

    serializer_class    = ReserveListSerialize
    permission_classes = [IsBooker]

    def get_queryset(self):
        user_pk = self.request.user.pk
        return ReservartionHistory.objects.filter(booker=user_pk)
        
