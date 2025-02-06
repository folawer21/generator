# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from core.views import QuestionViewSet, AnswerViewSet, CharacteristicViewSet, GeneratedTestViewSet

# router = DefaultRouter()
# router.register(r'api/v1/get-questions', QuestionViewSet)
# router.register(r'api/v1/answers', AnswerViewSet)
# router.register(r'api/v1/get-characteristics', CharacteristicViewSet)
# router.register(r'api/v1/get-generatedTests', GeneratedTestViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]

from django.urls import path

from core import views

urlpatterns = [
    path('api/v1/get-questions', views.get_questions, name='question_list'),
    path('api/v1/get-characteristics', views.get_characteristics, name='characteristic_list'),
    path('api/v1/get-generatedTests', views.get_generated_tests, name='generated_test_list'),
    path('api/v1/get-generateTests', views.generate_test, name='generate_test'),
    path('api/v1/delete-combinedTest', views.delete_combined_test, name='delete_combined_test'),

]