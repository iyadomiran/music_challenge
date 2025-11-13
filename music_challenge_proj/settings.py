from pathlib import Path
import os

# ==============================
# 基本設定
# ==============================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# セキュリティ設定
# ==============================

# SECRET_KEY: 本番は環境変数から読み込む
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-placeholder-key-for-local-dev",  # ローカル開発用
)

# DEBUGモード: 環境変数で制御
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

# 許可するホスト（カンマ区切り）
ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1,music-challenge.onrender.com",
).split(",")

# ==============================
# アプリケーション定義
# ==============================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "compose",  # 自作アプリ
]

# ==============================
# ミドルウェア
# ==============================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # 静的ファイル配信
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "music_challenge_proj.urls"

# ==============================
# テンプレート設定
# ==============================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # プロジェクト共通テンプレート
        "APP_DIRS": True,                  # 各アプリのtemplatesも探索
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "music_challenge_proj.wsgi.application"

# ==============================
# データベース設定（SQLite）
# ==============================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ==============================
# パスワード検証
# ==============================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ==============================
# 国際化
# ==============================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Tokyo"
USE_I18N = True
USE_TZ = True

# ==============================
# 静的ファイル設定
# ==============================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # 開発時に参照する静的ファイル
STATIC_ROOT = BASE_DIR / "staticfiles"    # collectstatic 実行時の出力先
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ==============================
# メディアファイル設定（録音データや生成画像）
# ==============================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ==============================
# デフォルト主キー
# ==============================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==============================
# 本番用セキュリティ強化設定
# ==============================
if not DEBUG:
    # HTTPS 強制
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # HSTS（HTTP Strict Transport Security）
    SECURE_HSTS_SECONDS = 31536000  # 1年
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # リファラ制限
    SECURE_REFERRER_POLICY = "same-origin"

# ==============================
# ローカル開発用メモ
# ==============================
# MEDIA_ROOT 以下に保存された録音や解析画像は
# 開発サーバーでは `python manage.py runserver` で /media/ にアクセス可能
# 本番では nginx や WhiteNoise などで配信設定が必要