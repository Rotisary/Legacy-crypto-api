from django.urls import path
from users.api.views import (
    registration_view,
    user_detail_view,
    profile_view,
    update_profile_view,
    update_user_detail_view,
    delete_user_view,
    ObtainAuthTokenView,
    ChangePasswordApiView,
    add_wallet,
    wallet_view,
    delete_wallet_view,
    send_fund,
    fund_detail,
    FundHistory
)

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', ObtainAuthTokenView.as_view(), name='login'),
    path('details/<str:username>/', user_detail_view, name='user-detail'),
    path('profile/<str:username>/', profile_view, name='profile-detail'),
    path('profile/<str:username>/update/', update_profile_view, name='doctor-profile-update'),
    path('details/<str:username>/update/', update_user_detail_view, name='patient-profile-update'),
    path('<str:username>/delete/', delete_user_view, name='delete-user'),
    path('change-password/', ChangePasswordApiView.as_view(), name='change-password'),
    path('add-wallet/', add_wallet, name='add-wallet'),
    path('wallet/<str:username>/', wallet_view, name='wallet-detail'),
    path('wallet/<str:username>/delete/', delete_wallet_view, name='delete-wallet'),
    path('send-fund/<str:username>/', send_fund, name='send-fund'),
    path('fund/<int:pk>/', fund_detail, name='fund-detail'),
    path('funds/history/', FundHistory.as_view(), name='funds-list')
]
