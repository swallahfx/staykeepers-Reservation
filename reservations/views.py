import re
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import authentication, permissions
from reservations.models import Listing, HotelRoomType, HotelRoom, BookingInfo,BlockedPeriod
from .serializers import BlockedPeriodSerializer, BookingSerializer, SearchSerializer
from django.utils.timezone import datetime


class Booking(APIView):
    serializer_class = BlockedPeriodSerializer
    permission_classes= (permissions.AllowAny,)
    queryset = BlockedPeriod.objects.all()
    
    def get(self, request, *args, **kwargs):
        all_apartments = BookingSerializer(BookingInfo.objects.all(), 
            many=True
            ).data
        return Response(dict(all_apartments=all_apartments))
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print()
            check_in = serializer.data.get('check_in')
            check_out = serializer.data.get('check_out')
            bookings = serializer.data.get('bookings')
            print(serializer.data)
            checker = BlockedPeriod.objects.filter(bookings=bookings, booked=True)
            if checker.exists():                
                return Response(dict(messages='seleted room is not avaliable'))
            else:
                blocked = BlockedPeriod.objects.create(
                    check_in=check_in,
                    check_out=check_out,
                    bookings=bookings,
                    booked=True
                )
                response = {
                    'messages': f'{bookings} has been booked successfully from {check_in} to {check_out}',
                    'data':BookingSerializer(blocked).data,
                }
                return Response(response)
        return Response({'message': "an error occured"})
        
 
class SearchBooking(APIView): 
    serializer_class = SearchSerializer
    permission_classes= (permissions.AllowAny,)
    queryset = BlockedPeriod.objects.all()
    
    def get(self, request, *args, **kwargs):
        check_in=request.query_params.get('check_in')
        max_price=request.query_params.get('max_price')
    
        queryset = BlockedPeriod.objects.filter(
            Q(bookings__price__lte=max_price)|
            Q(check_out__lte=check_in)
        )
        
        if queryset.exists(): 
            # print(BlockedPeriod.bookings.get_queryset()[:3].values) 
            # print(BookingInfo.price)             
            ex = BookingInfo.objects.filter(price__lte=max_price).exclude(id__in=queryset.values_list('bookings_id', flat=True))
            trap = []
            for i in ex:
                if i.listing:                    
                    trap.append({
                        'listing_type': i.listing.listing_type,
                        'title':i.listing.title,
                        'country':i.listing.country,
                        'city':i.listing.city,
                        'price':i.price
                    })
                    
            return Response({
                    # 'message': "search result",
                    'items' : trap
                    })
        return Response({'message': "an error occured"})
       