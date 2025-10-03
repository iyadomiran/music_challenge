from django.urls import path  # URLパターンを定義するモジュールを読み込む
from . import views          # 同じアプリ内の views.py を読み込む

# このアプリ内のURLパターンを定義
urlpatterns = [
    path('', views.top_view, name='top'),                     # トップページ
    path('register/', views.register_view, name='register'),  # 新規登録ページ
    path('login/', views.login_view, name='login'),           # ログインページ
    path('guest/', views.guest_play_view, name='guest_play'), # ゲストプレイページ
    path('rules/', views.rules, name='rules'),               # ルールページ
    path('game/', views.compose_view, name='game'),          # ゲーム画面
    path('logout/', views.logout_view, name='logout_view'),  # ログアウト処理
    path('mypage/', views.mypage_view, name='mypage'),       # マイページ
    path('save_score/', views.save_score, name='save_score'),# スコア保存用API
]