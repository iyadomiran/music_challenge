from django.contrib import admin  # 管理画面用のモジュールを読み込む
from .models import Score         # 同じアプリ内の Score モデルを読み込む

admin.site.register(Score)
# 管理画面に Score モデルを登録する
# これにより、Django 管理画面から Score を追加・編集・削除できるようになる