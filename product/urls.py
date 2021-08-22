
from django.urls import path

app_name='product'
from .views import product_create_view, register_view, product_detail_view, user_view, login_user, logout_user,product_update_view, product_delete_view, like_post

urlpatterns = [
        path('create/', product_create_view, name='product-create'),
        path('register/', register_view, name='register-user'),
        path('login/', login_user, name='login-user'),
        path('logout/', logout_user, name='logout-user'),
        path('<int:pk>/', product_detail_view, name='product-detail'),
        path('user/', user_view, name='user-view'),
        path('update/<int:pk>/', product_update_view, name='product-update'),
        path('delete/<int:pk>/', product_delete_view, name='product-delete'),
        path('like/', like_post, name='like-post'),


        # path('comment/', product_comment_view, name='product-comment'),



]
