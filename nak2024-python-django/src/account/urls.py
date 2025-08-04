from django.urls import path, include
from .views import UserLoginView, UserLogoutView, BecomeSellerView, ToggleUserRoleView, StoreView
from .router import router

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('become-seller/', BecomeSellerView.as_view(), name='become-seller'),
    path('toggle-role/', ToggleUserRoleView.as_view(), name='toggle-role'),
    path('store/<int:seller_id>/', StoreView.as_view(), name='store'),
    path('', include(router.urls)),
]