from django.urls import path
from users import views as users_view


urlpatterns = [
    path('register/', users_view.Register.as_view(), name="signUp"),
    path('login/', users_view.Login.as_view(), name="login"),
    path('logout/', users_view.Logout.as_view(), name="logout"),
    path('dashboard/', users_view.Dashboard.as_view(), name="dashboard"),
]
