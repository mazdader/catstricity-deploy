# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views
#from django.contrib import admin

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^run/(?P<server>.*)/$', views.runAnsible, name='run_ansible'),
    url(r'^results/(?P<server>.*)/$', views.viewResults, name='view_results'),

]