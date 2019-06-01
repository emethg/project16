from django.urls import include, path
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name="logout"),
    path('register/', views.register, name='register'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('reset_password/', PasswordResetView.as_view(template_name='accounts/password_reset_form.html'), name='password_reset'),
    path('reset_password/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password/confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password/complete', PasswordResetConfirmView.as_view(), name='password_reset_complete'),
    path('items_list/', views.view_items, name='list_items'),
    path('profile/click', views.activate_notification, name='activate_notification'),
    path('profile/list_activity', views.list_activity_log, name='list_activity_log'),
    path('profile/<name>', views.information, name='information'),
    path('todo/', views.todo, name='todo'),
    path('todo/add', views.addTodo, name='add'),
    path('todo/complete/<todo_id>', views.completeTodo, name="complete"),
    path('todo/deletecomplete', views.deleteCompleted, name="deletecomplete"),
    path('todo/deleteall', views.deleteCompleted, name="deleteall"),
    path('test/', views.test, name='test'),
    path('testp/', views.test_new, name='test'),
    path('dish/', views.dishes, name='dishes'),

]
