from django.urls import path

from accounts.views import SignupView, SigninView, CreateAdminView

# from accounts.views import SignupView, SigninView

# from .views import RegisterView, CustomTokenObtainPairView

urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),
    # # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('signin/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', SignupView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('create-admin/', CreateAdminView.as_view(), name='create_admin'),
]
