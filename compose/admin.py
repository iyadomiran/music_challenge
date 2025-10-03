from django.contrib import admin  # 管理画面用のモジュールを読み込む
from .models import Score, SongPattern  # 同じアプリ内の Score と SongPattern モデルを読み込む

# Score モデルを管理画面に登録
# これにより、Django 管理画面から Score を追加・編集・削除できるようになる
admin.site.register(Score)

# SongPattern モデルを管理画面に登録
# これにより、Django 管理画面から正解曲パターンを追加・編集・削除できるようになる
admin.site.register(SongPattern)