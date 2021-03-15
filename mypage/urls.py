from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mypage', views.mypage, name='mypage'),
    path('mypage_process/<int:account_id>', views.mypage_process, name='mypage_process'),
    path('signup', views.signup, name='signup'),
    path('signup_process', views.signup_process, name='signup_process'),
    path('login', views.login, name='login'),
    path('login_process', views.login_process, name='login_process'),
    path('logout', views.logout, name='logout'),
    path('account_add', views.account_add, name='account_add'),
    path('account_add_proccess', views.account_add_proccess, name='account_add_proccess'),
    path('account_add_first', views.account_add_first, name='account_add_first'),
    path('account_add_first_proccess', views.account_add_first_proccess, name='account_add_first_proccess'),
    path('template_index', views.template_index, name='template_index'),
    path('template_index_process/<int:template_type_id>', views.template_index_process, name='template_index_process'),
    path('template_follow_add', views.template_follow_add, name='template_follow_add'),
    path('template_follow_add_proccess', views.template_follow_add_proccess, name='template_follow_add_proccess'),
    path('template_guest_add', views.template_guest_add, name='template_guest_add'),
    path('template_guest_add_proccess', views.template_guest_add_proccess, name='template_guest_add_proccess'),
    path('template_repeater_add', views.template_repeater_add, name='template_repeater_add'),
    path('template_repeater_add_proccess', views.template_repeater_add_proccess, name='template_repeater_add_proccess'),
    path('template_campaign_add', views.template_campaign_add, name='template_campaign_add'),
    path('template_campaign_add_proccess', views.template_campaign_add_proccess, name='template_campaign_add_proccess'),
    path('template_static_edit/<int:template_id>', views.template_static_edit, name='template_static_edit'),
    path('template_static_edit_proccess/<int:template_id>', views.template_static_edit_proccess, name='template_static_edit_proccess'),
    path('follower_show', views.follower_show, name='follower_show'),

]
