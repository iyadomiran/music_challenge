from django.shortcuts import render, redirect  # テンプレート表示やリダイレクト用
from django.contrib.auth.models import User   # ユーザーモデル
from django.contrib.auth import authenticate, login, logout  # 認証用関数
from django.contrib import messages             # 画面上の通知メッセージ用
from django.contrib.auth.decorators import login_required  # ログイン必須デコレーター
from django.http import JsonResponse            # JSONレスポンスを返すため
from .models import Score                       # 自作のScoreモデル
from django.utils import timezone               # 日付・時間操作用
import json                                     # JSON操作用

# トップページ
def top_view(request):
    # top.htmlを表示
    return render(request, 'compose/top.html')


# ゲストプレイ
def guest_play_view(request):
    # セッションに「ゲストフラグ」をセット
    request.session['guest'] = True
    # ルールページへリダイレクト
    return redirect('rules')


# ルールページ
def rules(request):
    # rules.htmlを表示
    return render(request, 'compose/rules.html')


# ゲーム画面（既存の compose.html を使用）
def compose_view(request):
    # ゲーム用の音パターン（必要に応じて変更可能）
    pattern = ["do", "re", "mi", "fa"]
    # compose.htmlにパターンを渡して表示
    return render(request, 'compose/compose.html', {'pattern': pattern})


# 新規登録
def register_view(request):
    if request.method == 'POST':
        # フォームからユーザー名とパスワードを取得
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # ユーザー名またはパスワードが空ならエラー
        if not username or not password:
            messages.error(request, "ユーザー名とパスワードを入力してください。")
            return redirect('register')

        # 既に存在するユーザー名ならエラー
        if User.objects.filter(username=username).exists():
            messages.error(request, "そのユーザー名は既に使われています。")
            return redirect('register')

        # 新規ユーザー作成
        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "ユーザー登録が完了しました。ログインしてください。")
        # 登録後はログインページへ
        return redirect('login')

    # GET時は登録ページを表示
    return render(request, 'compose/register.html')


# ログイン
def login_view(request):
    if request.method == 'POST':
        # フォームからユーザー名とパスワードを取得
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # ユーザー認証
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # 認証成功ならログイン処理
            login(request, user)
            # 成功時はルールページへリダイレクト
            return redirect('rules')
        else:
            # 認証失敗ならエラーメッセージ
            messages.error(request, "ユーザー名またはパスワードが間違っています。")
            return redirect('login')

    # GET時はログインページ表示
    return render(request, 'compose/login.html')


# ログアウト
def logout_view(request):
    # ログアウト処理
    logout(request)
    messages.success(request, "ログアウトしました。")
    # トップページへリダイレクト
    return redirect('top')


# ログインユーザー専用のマイページ（スコア履歴表示・日付選択対応）
@login_required
def mypage_view(request):
    # 今日の日付を取得
    today = timezone.localdate()

    # 日付ごとのスコアを辞書にまとめる
    scores_by_date = {}
    qs = Score.objects.filter(user=request.user).order_by('played_at')  # ユーザーのスコアを日付順に取得
    for s in qs:
        date_str = s.played_at.strftime('%Y-%m-%d')  # 日付だけ取り出す
        if date_str not in scores_by_date:
            scores_by_date[date_str] = []
        scores_by_date[date_str].append(s.score)  # 同じ日付のスコアをリストに追加

    # 今日のスコアを取得
    today_str = today.strftime('%Y-%m-%d')
    today_scores = scores_by_date.get(today_str, [])

    # 今日の最新スコアと全期間の最高スコア
    latest_score = today_scores[-1] if today_scores else None
    best_score = max([score for scores in scores_by_date.values() for score in scores]) if scores_by_date else None

    # グラフ表示用にJSON形式に変換
    scores_json = {}
    for date, scores in scores_by_date.items():
        scores_json[date] = {
            "labels": [f"挑戦{i+1}" for i, s in enumerate(scores)],  # 「挑戦1」「挑戦2」などのラベル
            "data": scores
        }

    # テンプレートに渡すコンテキスト
    context = {
        'username': request.user.username,
        'available_dates': list(scores_by_date.keys()),
        'scores_by_date_json': json.dumps(scores_json),
        'latest_score': latest_score,
        'best_score': best_score,
    }

    # mypage.htmlを表示
    return render(request, 'compose/mypage.html', context)


# ゲーム終了時にスコアを保存する
@login_required
def save_score(request):
    if request.method == 'POST':
        try:
            # フォームからスコアを取得して整数に変換
            score_value = int(request.POST.get('score', 0))
            # データベースにスコアを保存
            Score.objects.create(user=request.user, score=score_value)
            # 成功レスポンス
            return JsonResponse({'status': 'ok'})
        except ValueError:
            # 数値変換エラー時
            return JsonResponse({'status': 'error', 'message': '無効なスコア'})
    # POST以外のリクエストはエラー
    return JsonResponse({'status': 'error', 'message': 'POSTメソッドのみ許可'})