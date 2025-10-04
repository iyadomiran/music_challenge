from pathlib import Path
import os

# ==============================
# 基本設定
# ==============================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# セキュリティ設定
# ==============================

# SECRET_KEY: 本番はRender環境変数から読み込む
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-placeholder-key-for-local-dev",  # ローカル開発用のダミーキー
)

# DEBUGモード: 環境変数で制御（RenderではFalse推奨）
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

# 許可するホスト（Renderドメインを含める）
ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1,music-challenge.onrender.com",
).split(",")

# ==============================
# アプリケーション定義
# ==============================
INSTALLED_APPS = [
    "django.contrib.admin",          # 管理画面
    "django.contrib.auth",           # 認証
    "django.contrib.contenttypes",   # コンテンツタイプ
    "django.contrib.sessions",       # セッション
    "django.contrib.messages",       # メッセージ
    "django.contrib.staticfiles",    # 静的ファイル
    "compose",                       # 自作アプリ
]

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
# データベース設定
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
TIME_ZONE = "Asia/Tokyo"  # ← UTCより日本時間の方が開発に便利
USE_I18N = True
USE_TZ = True

# ==============================
# 静的ファイル設定
# ==============================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoiseで圧縮・キャッシュ管理
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ==============================
# デフォルト主キー
# ==============================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==============================
# 本番用セキュリティ強化設定
# ==============================
if not DEBUG:
    # HTTPS強制
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # HSTS（HTTPS固定）
    SECURE_HSTS_SECONDS = 31536000  # 1年
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # リファラ制限
    SECURE_REFERRER_POLICY = "same-origin"