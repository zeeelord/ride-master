from django.urls import path

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from . import views


app_name = 'userprofile'


urlpatterns = [

    path('login_user', views.LoginView.as_view(), name='login'),
    path('register_user', views.UserCreateView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('user/', views.get_user, name="user_profile"),
    # path('user/update/', views.user_update, name="user_update"),
    # path('change_password_of_user', views.change_password, name='change_a_user_password'),
    # path('change_password_user', views.user_change_password, name='user_password'),

    # reset password
    # path(
    #     'reset_password/',
    #     auth_views.PasswordResetView.as_view(template_name='email-reset.html',
    #                                          success_url=reverse_lazy('userprofile:password_reset_done')),
    #     name='reset_password'),
    #
    # path(
    #     'reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='email-reset-sent.html'),
    #     name='password_reset_done'),
    #
    #
    # path(
    #     'reset/<uidb64>/<token>/',
    #     auth_views.PasswordResetConfirmView.as_view(template_name='email-reset-sent.html',
    #                                                 success_url=reverse_lazy('userprofile:password_reset_complete')),
    #     name='password_reset_confirm'),
    #
    #
    # path(
    #     'reset_password_complete/',
    #     auth_views.PasswordResetCompleteView.as_view(template_name='email-reset-done.html'),
    #     name='password_reset_complete'),
]
