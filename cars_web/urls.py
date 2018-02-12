from django.conf.urls import include, url
from django.contrib import admin
from .views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'cars_web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^get/models/$', GetModels.as_view(), name='models'),
    url(r'^get/results/$', RetrieveAutoTraderResults.as_view(), name='results'),
    url(r'^$', Homepage.as_view(), name='homepage')
]
