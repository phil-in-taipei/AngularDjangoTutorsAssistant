"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

"""
class AngularAppView(TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # this can be used to pass any customized data to frontend
        # for SPA configuration ie app name, color variables etc.
        # the encryption key in this prototype is insecure
        # so this approach was abandoned in favor of environment variables
        # on seperate frontend server with SSR
        context['encryption_config'] = {
            'frontend_encryption_key': settings.FRONTEND_ENCRYPTION_KEY
        }
        return context
"""


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authapp.urls')),
    path('api/accounting/', include('accounting.urls')),
    path('api/profiles/', include('user_profiles.urls')),
    path('api/recurring/', include('recurring_scheduling.urls')),    
    path('api/schools/', include('school.urls')),
    path('api/scheduling/', include('class_scheduling.urls')),
    path('api/accounts/', include('student_account.urls')),
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]
