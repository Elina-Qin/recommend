from django.urls import path
from .views import (
    calculate_recommendation_1, calculate_recommendation_2, calculate_recommendation_3,
    get_latest_recommendation_1, get_latest_recommendation_2, get_latest_recommendation_3
)

# 接口URL配置
urlpatterns = [
    # 3个上传接口：对应3个上传按钮
    path(route='calculate/1/', view=calculate_recommendation_1, name='calculate_recommendation_1'),
    path(route='calculate/2/', view=calculate_recommendation_2, name='calculate_recommendation_2'),
    path(route='calculate/3/', view=calculate_recommendation_3, name='calculate_recommendation_3'),

    # 3个查看接口：对应3个查看按钮
    path(route='latest-recommendation/1/', view=get_latest_recommendation_1, name='get_latest_recommendation_1'),
    path(route='latest-recommendation/2/', view=get_latest_recommendation_2, name='get_latest_recommendation_2'),
    path(route='latest-recommendation/3/', view=get_latest_recommendation_3, name='get_latest_recommendation_3'),
]