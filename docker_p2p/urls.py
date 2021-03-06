"""docker_p2p URL Configuration

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
from p2p import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^api/v1/filelist$', views.filelist_api),
    url(r'^api/v1/download_file$', views.download_file),
    url(r'^api/v1/search_neighbor$', views.search_neighbor),
    url(r'^search_results$', views.search_results),
    url(r'^search_page$', views.search_page),
    url(r'^local_files$', views.local_files),
    url(r'^api/v1/sync$', views.sync_files),
    url(r'^upload$', views.upload_page),
    url(r'^api/v1/upload$', views.upload_file),
    url(r'^test$', views.test_page),
    url(r'^api/v1/download_tcp$', views.download_file_tcp),
    url(r'^api/v1/test$', views.test_api),
    url(r'^api/v1/split$', views.download_split_tcp),

]
