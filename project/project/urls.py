"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from museos import views
from project import settings
from django.contrib.auth.views import login, logout
from django.views.static import serve
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$',views.principal, name = 'barra'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout', logout, {'next_page': '/'}),
    url(r'^login', login),
    #url(r'^museos/(\d+)', views.museo_id, name='museo_id'),
    url(r'^museos', views.museos_all, name='museos_all'),
    url(r'^css$', views.css),
    ##url(r'^static/(?P<path>.*)$', serve, {'document_root':settings.STATIC_URL }),
    ##url(r'^(static/(?P<path>.*)$', serve, {'document_root':'templates/businessxhtml'}),
    url(r'^style.css$', serve, {'document_root':'templates/businessxhtml' }),
    #url(r'^about', views.autoria_html, name='HTML'),
    url(r'^(\w+)/xml', views.user_xml, name='XML_user'),
    url(r'^(.+)', views.usuario, name='pag_personal'),
]
