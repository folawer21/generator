from django.urls import path

from core import views

urlpatterns = [
    path('api/v1/get-questions', views.get_questions, name='question_list'),
    path('api/v1/get-characteristics', views.get_characteristics, name='characteristic_list'),
    path('api/v1/get-generatedTests', views.get_generated_tests, name='generated_test_list'),
    path('api/v1/get-generateTests', views.generate_test, name='generate_test'),
    path('api/v1/delete-combinedTest', views.delete_combined_test, name='delete_combined_test'),
    path('api/v1/get-combined-test', views.get_combined_test, name='get_combined_test'),
    path('api/v1/groups/', views.get_groups_with_students, name='get_groups_with_students'),
    path('api/v1/student/<int:student_id>/portrait/', views.get_psychological_portrait, name='get_psychological_portrait'),
    path('api/v1/submit_results_from_test', views.submit_results_from_test, name ='submit_results_from_test')
]