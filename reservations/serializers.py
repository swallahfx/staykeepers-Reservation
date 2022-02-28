from rest_framework import serializers
from reservations.models import Listing, HotelRoomType, HotelRoom, BookingInfo, BlockedPeriod


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields =  ('__all__')
        
class BookingSerializer(serializers.ModelSerializer):
    listing = ListingSerializer()
    class Meta:
        model = BookingInfo
        fields = ('__all__')
        
        
class BlockedPeriodSerializer(serializers.ModelSerializer):    
    class Meta:
        model = BlockedPeriod
        fields = ['bookings', 'check_in', 'check_out']
        
class SearchSerializer(serializers.Serializer):   
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    max_price = serializers.DecimalField(max_digits=6, decimal_places=2)
        