from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Score
from django.utils import timezone
import json

# トップページ
def top_view(request):
    return render(request, 'compose/top.html')


# ゲストプレイ
def guest_play_view(request):
    request.session['guest'] = True
    return redirect('rules')


# ルールページ
def rules(request):
    return render(request, 'compose/rules.html')


# ゲーム画面（既存の compose.html を使用）
def compose_view(request):
    pattern = ["do", "re", "mi", "fa"]  # 必要に応じて変更
    return render(request, 'compose/compose.html', {'pattern': pattern})


# 新規登録
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, "ユーザー名とパスワードを入力してください。")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "そのユーザー名は既に使われています。")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "ユーザー登録が完了しました。ログインしてください。")
        return redirect('login')

    return render(request, 'compose/register.html')


# ログイン
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('rules')  # ログイン成功後はルールページへ
        else:
            messages.error(request, "ユーザー名またはパスワードが間違っています。")
            return redirect('login')

    return render(request, 'compose/login.html')


# ログアウト
def logout_view(request):
    logout(request)
    messages.success(request, "ログアウトしました。")
    return redirect('top')


# マイページ（スコア履歴表示・日付選択対応）
@login_required
def mypage_view(request):
    """
    ログインユーザー専用のマイページ
    Scoreテーブルからユーザーのスコア履歴を取得し、
    Chart.js で日付ごとに表示できるようJSON化してテンプレートに渡す。
    """
    # 今日の日付
    today = timezone.localdate()

    # 日付ごとのスコアを辞書にまとめる
    scores_by_date = {}
    qs = Score.objects.filter(user=request.user).order_by('played_at')
    for s in qs:
        date_str = s.played_at.strftime('%Y-%m-%d')
        if date_str not in scores_by_date:
            scores_by_date[date_str] = []
        scores_by_date[date_str].append(s.score)

    # 今日のスコアも確保
    today_str = today.strftime('%Y-%m-%d')
    today_scores = scores_by_date.get(today_str, [])

    # 最新スコアと最高スコア
    latest_score = today_scores[-1] if today_scores else None
    best_score = max([score for scores in scores_by_date.values() for score in scores]) if scores_by_date else None

    # JSON化
    scores_json = {}
    for date, scores in scores_by_date.items():
        scores_json[date] = {
            "labels": [f"挑戦{i+1}" for i, s in enumerate(scores)],
            "data": scores
        }

    context = {
        'username': request.user.username,
        'available_dates': list(scores_by_date.keys()),
        'scores_by_date_json': json.dumps(scores_json),
        'latest_score': latest_score,
        'best_score': best_score,
    }

    return render(request, 'compose/mypage.html', context)


# ゲーム終了時にスコアを保存する
@login_required
def save_score(request):
    if request.method == 'POST':
        try:
            score_value = int(request.POST.get('score', 0))
            Score.objects.create(user=request.user, score=score_value)
            return JsonResponse({'status': 'ok'})
        except ValueError:
            return JsonResponse({'status': 'error', 'message': '無効なスコア'})
    return JsonResponse({'status': 'error', 'message': 'POSTメソッドのみ許可'})