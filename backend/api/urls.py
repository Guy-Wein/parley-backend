from django.urls import path
from . import views

urlpatterns = [
    path('transaction-class', views.ProcessorListMixin.as_view(), name="processor_list"),
    path('transaction-create', views.ProcessorCreateMixin.as_view(), name="processor_create"),
    path('transaction-advance', views.ProcessorCreateAdvance.as_view(), name="processor_advance")
]