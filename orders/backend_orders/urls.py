from django.urls import path
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm

from rest_framework.routers import DefaultRouter

from .views import PartnerUpdate, RegisterAccount, LoginAccount, CategoryViewSet, ShopViewSet, ProductInfoViewSet, \
    BasketView, AccountDetails, ContactView, OrderView, PartnerState, PartnerOrders, ConfirmAccount

router = DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'product', ProductInfoViewSet, basename='products')
router.register(r'shops', ShopViewSet)

app_name = 'backend_my_diplom'
urlpatterns = [
    # Путь для обновления данных партнера.
    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    # Путь для получения статуса партнера.
    path('partner/state', PartnerState.as_view(), name='partner-state'),
    # Путь для получения заказов партнера.
    path('partner/orders', PartnerOrders.as_view(), name='partner-orders'),
    # Путь для регистрации нового пользователя.
    path('user/register', RegisterAccount.as_view(), name='user-register'),
    # Путь для подтверждения аккаунта пользователя.
    path('user/register/confirm', ConfirmAccount.as_view(), name='user-register-confirm'),
    # Путь для получения информации о пользователе.
    path('user/details', AccountDetails.as_view(), name='user-details'),
    # Путь для связи с администрацией сайта.
    path('user/contact', ContactView.as_view(), name='user-contact'),
    # Путь для авторизации пользователя.
    path('user/login', LoginAccount.as_view(), name='user-login'),
    # Путь для сброса пароля пользователя.
    path('user/password_reset', reset_password_request_token, name='password-reset'),
    # Путь для подтверждения сброса пароля пользователя.
    path('user/password_reset/confirm', reset_password_confirm, name='password-reset-confirm'),
    # Путь для получения списка категорий товаров.
    # path('categories', CategoryView.as_view(), name='categories'),
    # Путь для получения списка магазинов.
    # path('shops', ShopView.as_view(), name='shops'),
    # Путь для получения списка товаров.
    # path('products', ProductInfoView.as_view(), name='shops'),
    # Путь для работы с корзиной покупателя.
    path('basket', BasketView.as_view(), name='basket'),
    # Путь для создания нового заказа.
    path('order', OrderView.as_view(), name='order'),
]
