from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DetailView, ListView, CreateView
from .models import Marker, Profile, MarkerImage
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignInForm, SignUpForm
from django.contrib.gis.geos import GEOSGeometry
import folium, geocoder
from django.contrib.gis.geos import Polygon
from .serializers import ImageListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
User = get_user_model()


class MarkerMapView(LoginRequiredMixin,TemplateView):
    template_name = "marker.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['marker_list'] = [   
            {
                'name':obj.name,
                'date':obj.date.date,
                'location':[obj.location[1], obj.location[0]],
            }
            for obj in Marker.objects.filter(user = self.request.user)
        ]
        return context



class SignUpView(CreateView):
    model = User
    template_name = 'form.html'
    form_class = SignUpForm
    
    def get_success_url(self):
        return reverse('gis_app:signin')


class SignInView(LoginView):
    template_name = 'form.html'
    form_class = SignInForm 
    success_url = reverse_lazy('gis_app:marker')
	


class LogOutView(LoginRequiredMixin,LogoutView):
    model = User
    
    def get_success_url(self):
        return reverse('gis_app:signin')


class ProfileView(LoginRequiredMixin,TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        
        profile = Profile.objects.filter(user = self.request.user).first()
            
        if profile is not None:
            context["information"] = {
                "title":profile.title,
                "home":list(reversed(profile.home)),
                "worker":list(reversed(profile.worker)),
                "line":[list(profile.home), list(profile.worker)],
                "length": profile.home.distance(profile.worker) * 100,
                "city":profile.city_point_list,
                "description":profile.description,
                "username":profile.user.username,
            }
        


        return context


class UserListView(ListView):
    queryset = Profile.objects.select_related('user').all()
    template_name = "users.html"
    context_object_name = "users"

class UserView(TemplateView): 
    template_name = 'profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        
        profile = Profile.objects.get(user__id = kwargs['pk'] )
            
        context["information"] = {
            "title":profile.title,
            "home":list(reversed(profile.home)),
            "worker":list(reversed(profile.worker)),
            "line":[list(profile.home), list(profile.worker)],
            "length": profile.home.distance(profile.worker) * 100,
            "city":profile.city_point_list,
            "description":profile.description,
            "username":profile.user.username,
        }

        return context


class Where(TemplateView):
    template_name = 'where.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        ip = self.request.META.get('REMOTE_ADDR')
        addr = self.request.GET.get('name', 'tehran')
        location = geocoder.osm(addr)        
        bbox = location.geojson['features'][0]['properties']['bbox']
        geoms = Polygon.from_bbox(bbox)
        
        map = folium.Map([19, -12], zoom_start=2)
        markers = Marker.objects.filter(location__within=geoms)

        for marker in markers:
            folium.Marker(
            list(reversed(marker.location)), 
            popup=f'<a href="https://google.com">Images</a>',
            tooltip=f'{list(reversed(marker.location))}-{marker.name}', 
            ).add_to(map)
        
        folium.Marker(
            [location.lat, location.lng], 
            tooltip=f'{location.wkt}-{location.country}-{location.city}', 
            popup=f'<a href="https://en.wikipedia.org/w/index.php?search={addr}&title=Special%3ASearch&fulltext=1&ns0=1">{addr}</a>',
            icon=folium.Icon(color='red')
        ).add_to(map)

        context['map'] = map._repr_html_()


        return context


class ListImageView(APIView):

    def get(self, *args, **kwargs):
        try:
            marker = Marker.objects.get(id = kwargs['pk'])
            images = MarkerImage.objects.filter(marker = marker)
            srz = ImageListSerializer(images)
            return Response(srz, status=200)

        except:
            return Response({'msg':'marker is not found'}, status=400)