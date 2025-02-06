from django.urls import path

from core import views

urlpatterns = [
    path('api/v1/get-questions', views.get_questions, name='question_list'),
    path('api/v1/get-characteristics', views.get_characteristics, name='characteristic_list'),
    path('api/v1/get-generatedTests', views.get_generated_tests, name='generated_test_list'),
    path('api/v1/get-generateTests', views.generate_test, name='generate_test'),
    path('api/v1/delete-combinedTest', views.delete_combined_test, name='delete_combined_test'),
    path('api/v1/get-combined-test', views.get_combined_test, name='get_combined_test')
]