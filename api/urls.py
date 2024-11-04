from django.urls import path

from . import views
urlpatterns = [
    path('api/user/login', views.user_login),
    path('api/user/register', views.user_register),
    path('api/user/current', views.user_current),
    path('api/user/logout', views.user_logout),
    path('api/user/update', views.user_update),
    path('api/user/list', views.user_list),
    path('api/user/delete/<int:id>', views.user_delete),
    path('api/user/add', views.user_add),
    path('api/scenic/add', views.scenic_add),
    path('api/scenic/list', views.scenic_list),
    path('api/scenic/<int:id>', views.scenic_detail),
    path('api/scenic/delete/<int:id>', views.scenic_delete),
    path('api/scenic/update/<int:id>', views.scenic_update),
    path('api/strategy/add', views.strategy_add),
    path('api/strategy/list', views.strategy_list),
    path('api/strategy/delete/<int:id>', views.strategy_delete),
    path('api/strategy/update/<int:id>', views.strategy_update),
    path('api/strategy/<int:id>', views.strategy_update),
    path('api/reserve/add', views.reserve_add),
    path('api/reserve/get/all', views.reserve_get_all),
    path('api/reserve/<int:id>', views.reserve_detail)
]