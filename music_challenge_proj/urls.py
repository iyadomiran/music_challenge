from django.contrib import admin  # /admin/ にアクセスするとDjango管理画面が表示される
from django.urls import path, include  # URLルーティング設定用
from django.views.generic import RedirectView  # URLを自動で別の場所に飛ばすときに使う

# URLパターン一覧
# アクセスされたURLごとにどの処理（ビュー）を呼ぶかを定義する
urlpatterns = [
    path('admin/', admin.site.urls),  # 管理画面専用URL
    path('', include('compose.urls')),  # ルートURLは compose アプリの URL を使用
    # include() によってアプリごとに URL を分けて管理できる
]


# 1. urlpatterns は 「URLごとの処理の対応表」
# 2. path() は 「このURLがリクエストされたらこの処理を実行する」
# 3. include() は 「別アプリのURL設定をまとめてここに追加する」
# 4. admin.site.urls は 「Django管理画面用のURL一覧」
# 5. RedirectView は 「将来、URLを別の場所に自動で飛ばすときに使う」