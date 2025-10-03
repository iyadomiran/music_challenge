from django.shortcuts import render, redirect  # テンプレート表示・リダイレクト用
from django.contrib.auth.models import User   # Django標準のユーザーモデル
from django.contrib.auth import authenticate, login, logout  # 認証用関数
from django.contrib import messages             # 画面上の通知メッセージ用
from django.contrib.auth.decorators import login_required  # ログイン必須デコレーター
from django.http import JsonResponse            # JSONレスポンスを返すため
from .models import Score, SongPattern          # 自作モデル（スコア・曲パターン）
from django.utils import timezone               # 日付・時間操作用
import json                                     # JSON操作用

# トップページ表示
def top_view(request):
    # top.htmlを表示
    return render(request, 'compose/top.html')

# ゲストプレイ（ログインなしでルールページへ）
def guest_play_view(request):
    # セッションにゲストフラグをセット
    request.session['guest'] = True
    # ルールページへリダイレクト
    return redirect('rules')

# ルールページ表示
def rules(request):
    return render(request, 'compose/rules.html')

# ゲーム画面表示（DBから曲パターンを取得してテンプレートに渡す）
def compose_view(request):
    # DBから全曲パターンを取得
    patterns = SongPattern.objects.all()

    # 難易度別に辞書化
    song_patterns = {
        "beginner": [p.pattern for p in patterns.filter(level="beginner")],
        "intermediate": [p.pattern for p in patterns.filter(level="intermediate")],
        "advanced": [p.pattern for p in patterns.filter(level="advanced")],
    }

    # compose.htmlに渡す
    return render(request, 'compose/compose.html', {'song_patterns': song_patterns})

# ユーザー新規登録
def register_view(request):
    if request.method == 'POST':
        # フォームから値を取得
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # 入力チェック
        if not username or not password:
            messages.error(request, "ユーザー名とパスワードを入力してください。")
            return redirect('register')

        # ユーザー名の重複チェック
        if User.objects.filter(username=username).exists():
            messages.error(request, "そのユーザー名は既に使われています。")
            return redirect('register')

        # 新規ユーザー作成
        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "ユーザー登録が完了しました。ログインしてください。")
        return redirect('login')

    # GET時は登録フォームを表示
    return render(request, 'compose/register.html')

# ユーザーログイン
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # 認証
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # 認証成功
            login(request, user)
            return redirect('rules')
        else:
            # 認証失敗
            messages.error(request, "ユーザー名またはパスワードが間違っています。")
            return redirect('login')

    # GET時はログインフォームを表示
    return render(request, 'compose/login.html')

# ユーザーログアウト
def logout_view(request):
    # ログアウト処理
    logout(request)
    messages.success(request, "ログアウトしました。")
    return redirect('top')

# マイページ（ログインユーザー専用）
@login_required
def mypage_view(request):
    # 今日の日付を取得
    today = timezone.localdate()

    # ユーザーのスコアを日付順に取得
    scores_by_date = {}
    qs = Score.objects.filter(user=request.user).order_by('played_at')
    for s in qs:
        date_str = s.played_at.strftime('%Y-%m-%d')
        if date_str not in scores_by_date:
            scores_by_date[date_str] = []
        scores_by_date[date_str].append(s.score)

    # 今日のスコア
    today_str = today.strftime('%Y-%m-%d')
    today_scores = scores_by_date.get(today_str, [])

    # 今日の最新スコアと全期間の最高スコア
    latest_score = today_scores[-1] if today_scores else None
    best_score = max([score for scores in scores_by_date.values() for score in scores]) if scores_by_date else None

    # JSON形式に変換（グラフ描画用）
    scores_json = {}
    for date, scores in scores_by_date.items():
        scores_json[date] = {
            "labels": [f"挑戦{i+1}" for i, s in enumerate(scores)],
            "data": scores
        }

    # テンプレートに渡す
    context = {
        'username': request.user.username,
        'available_dates': list(scores_by_date.keys()),
        'scores_by_date_json': json.dumps(scores_json),
        'latest_score': latest_score,
        'best_score': best_score,
    }

    return render(request, 'compose/mypage.html', context)

# ゲーム終了時スコア保存
@login_required
def save_score(request):
    if request.method == 'POST':
        try:
            # フォームから送信されたスコアを取得
            score_value = int(request.POST.get('score', 0))
            # データベースに保存
            Score.objects.create(user=request.user, score=score_value)
            return JsonResponse({'status': 'ok'})
        except ValueError:
            return JsonResponse({'status': 'error', 'message': '無効なスコア'})

    # POST以外はエラー
    return JsonResponse({'status': 'error', 'message': 'POSTメソッドのみ許可'})