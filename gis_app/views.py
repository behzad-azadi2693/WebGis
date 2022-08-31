from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from .models import Marker, Profile
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignInForm, SignUpForm
from django.contrib.gis.geos import GEOSGeometry

# Create your views here.
User = get_user_model()


class MakerMapView(LoginRequiredMixin,TemplateView):
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


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        
        profile = Profile.objects.get(user = self.request.user)
            
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
        
        for point in profile.city:
            print(point)

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