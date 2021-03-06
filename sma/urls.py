#! /usr/bin/env python2.7
"""{{ project_name }} URL Configuration

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
from sma.home.views import HomeView, RegisterView, CreateCardView, MainView, BuyItemView

admin.autodiscover()

urlpatterns = [
    # Homepage
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^register$', RegisterView.as_view(), name='register'),
    url(r'^create_card$', CreateCardView.as_view(), name='create_card'),
    url(r'^buy_item$', BuyItemView.as_view(), name='buy_item'),
    url(r'^main$', MainView.as_view(),name='main'),
    #url(r'^admin/', include(admin.site.urls)),
]
