from django.urls import path
from tax_calculator.views import tax_calculator

app_name = 'tax_calculator'
urlpatterns = [
   path('', tax_calculator, name='calculate-tax'),
]
