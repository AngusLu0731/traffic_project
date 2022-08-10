from .models import speedLot , towing , parking
from django import forms
import django_filters

class ParkingFilter(django_filters.FilterSet):
    
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder':'EX:錢櫃忠孝停車場'}))

    address = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder':'Ex:忠孝東路三段'}))

    class Meta:
        model = parking
        fields = ['name','address',]

class TowingFilter(django_filters.FilterSet):
    
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder':'Ex:土城逾放場'}))

    address = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder':'Ex:土城區青雲路113號'}))

    class Meta:
        model = parking
        fields = ['name','address',]

class SpeedLotFilter(django_filters.FilterSet):
    
    roadsection = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder':'Ex:忠孝東路三段'}))

    situation = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder':'測速情況'}))

    class Meta:
        model = parking
        fields = ['roadsection','situation',]