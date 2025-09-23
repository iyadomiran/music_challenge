from django.urls import path
from . import views

urlpatterns = [
    path('', views.top_view, name='top'),                     # トップページ
    path('register/', views.register_view, name='register'),  # 新規登録
    path('login/', views.login_view, name='login'),           # ログイン
    path('guest/', views.guest_play_view, name='guest_play'), # ゲストプレイ
    path('rules/', views.rules, name='rules'),               # ルールページ
    path('game/', views.compose_view, name='game'),          # ゲーム画面
    path('logout/', views.logout_view, name='logout_view'),  # ログアウト
    path('mypage/', views.mypage_view, name='mypage'),       # マイページ
    path('save_score/', views.save_score, name='save_score'),# スコア保存用API
]