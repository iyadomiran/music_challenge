from django.urls import path
from . import views

# app_name intentionally omitted so template {% url 'register' %} etc. resolve as global names

urlpatterns = [
    path('', views.top, name='top'),
    path('rules/', views.rules, name='rules'),

    # ゲームページ
    path('game/', views.game, name='game'),
    path('game2/', views.game2, name='game2'),

    # ユーザー認証
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.register, name='register'),

    # ゲストプレイ
    path('guest/', views.guest_play, name='guest_play'),

    # チャレンジ保存
    path('save_challenge/', views.save_challenge, name='save_challenge'),

    # マイページ
    path('mypage/', views.mypage, name='mypage'),

    # 録音アップロード
    path('upload_audio/', views.upload_audio, name='upload_audio'),

    # 新規：ピッチ解析（サーバー側で画像生成）
    path('analyze_pitch/', views.analyze_pitch, name='analyze_pitch'),
]