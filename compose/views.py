from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.db.models import F
from datetime import timedelta, date, datetime
import json
import logging
import os
import base64
from django.conf import settings
from django.utils import timezone

from .forms import RegisterForm
from .models import Challenge

# ログ出力用 logger
logger = logging.getLogger(__name__)

# ----------------- 既存ビュー -----------------
def top(request):
    return render(request, 'compose/top.html')

def rules(request):
    return render(request, 'compose/rules.html')

@ensure_csrf_cookie
def game(request):
    return render(request, 'compose/compose.html')

def game2(request):
    return render(request, 'compose/game2.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if not username or not password:
            messages.error(request, 'ユーザー名とパスワードを入力してください。')
            return render(request, 'compose/login.html')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('rules')
        else:
            messages.error(request, 'ユーザー名またはパスワードが間違っています。')
            return render(request, 'compose/login.html')
    else:
        return render(request, 'compose/login.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('top')
    return redirect('top')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username, password=password)
            messages.success(request, '登録しました。ログインしてください。')
            return redirect('login')
        else:
            for e in form.errors.values():
                messages.error(request, e)
            return render(request, 'compose/register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'compose/register.html', {'form': form})

def guest_play(request):
    request.session['is_guest'] = True
    return redirect('rules')

def mypage(request):
    if not request.user.is_authenticated:
        messages.error(request, 'ログインが必要です。')
        return redirect('login')
    today = timezone.localdate()
    challenges = Challenge.objects.filter(user=request.user, created_at__date=today).order_by('created_at')[:50]
    total = challenges.count()
    correct_count = sum(1 for c in challenges if c.correct and c.user_answer and c.correct == c.user_answer)
    correct_rate = int((correct_count / total) * 100) if total > 0 else 0

    all_challenges_qs = Challenge.objects.filter(user=request.user)
    dates = set()
    for ch in all_challenges_qs:
        try:
            local_dt = timezone.localtime(ch.created_at)
            dates.add(local_dt.date())
        except Exception:
            try:
                dates.add(ch.created_at.date())
            except Exception:
                logger.warning("Failed to convert created_at to date for Challenge id=%s", getattr(ch, 'id', 'unknown'))

    consecutive_days = 0
    d = timezone.localdate()
    while d in dates:
        consecutive_days += 1
        d = d - timedelta(days=1)

    if total == 0:
        weak_notes = []
    else:
        wrongs = Challenge.objects.filter(user=request.user).exclude(correct=F('user_answer'))
        weak_notes = list(wrongs.values_list('correct', flat=True).distinct()[:10])

    days_count = 7
    today_local = timezone.localdate()
    week_start = today_local - timedelta(days=today_local.weekday())
    week_end = week_start + timedelta(days=days_count - 1)

    past_range_qs = Challenge.objects.filter(
        user=request.user,
        created_at__date__range=(week_start, week_end)
    ).order_by('created_at')

    mapping = {}
    for ch in past_range_qs:
        try:
            d_local = timezone.localtime(ch.created_at).date()
        except Exception:
            d_local = ch.created_at.date()
        mapping.setdefault(d_local, []).append(ch)

    past_days_grouped = []
    for i in range(days_count):
        d_iter = week_start + timedelta(days=i)
        items = mapping.get(d_iter, [])
        past_days_grouped.append({
            'date': d_iter,
            'items': items
        })

    context = {
        'challenges': challenges,
        'correct_count': correct_count,
        'correct_rate': correct_rate,
        'consecutive_days': consecutive_days,
        'weak_notes': weak_notes,
        'past_week_grouped': past_days_grouped,
    }
    return render(request, 'compose/mypage.html', context)

@require_POST
def save_challenge(request):
    logger.info("save_challenge called, user=%s, body=%s", request.user if request.user.is_authenticated else "Anonymous", request.body)
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except Exception as e:
        logger.exception("invalid json in save_challenge")
        return HttpResponseBadRequest('invalid json')

    level = payload.get('level', '')[:64]
    correct = payload.get('correct', '')[:255]
    user_answer = payload.get('user_answer', '')[:255]

    if not correct:
        logger.warning("save_challenge missing 'correct'")
        return HttpResponseBadRequest('missing correct')
    if user_answer is None:
        logger.warning("save_challenge missing 'user_answer'")
        return HttpResponseBadRequest('missing user_answer')

    user = request.user if request.user.is_authenticated else None

    ch = Challenge.objects.create(
        user=user,
        level=level,
        correct=correct,
        user_answer=user_answer
    )

    logger.info("Challenge created id=%s user=%s level=%s correct=%s user_answer=%s", ch.id, user.username if user else 'None', level, correct, user_answer)
    return JsonResponse({'status': 'ok', 'id': ch.id})

@csrf_exempt
def upload_audio(request):
    """
    MediaRecorder で録音した音声をサーバーに保存
    """
    if request.method == 'POST':
        audio_data = request.POST.get('audio')
        if audio_data:
            try:
                header, audio_base64 = audio_data.split(',', 1)
                audio_bytes = base64.b64decode(audio_base64)
            except Exception as e:
                logger.exception("Failed to decode audio base64")
                return JsonResponse({'status': 'ng', 'error': 'invalid audio data'})

            filename = f"recorded_{datetime.now().strftime('%Y%m%d%H%M%S')}.webm"
            save_path = os.path.join(settings.MEDIA_ROOT, filename)
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(audio_bytes)
            return JsonResponse({'status': 'ok', 'filename': filename})
    return JsonResponse({'status': 'ng'})

# ----------------- 新規追加ビュー: ピッチ解析 -----------------
import librosa
import matplotlib.pyplot as plt
import numpy as np

def analyze_pitch(request):
    """
    POSTで送信された音声ファイルを解析し、ピッチ折れ線グラフを生成して表示
    """
    if request.method == "POST" and request.FILES.get("audio"):
        audio_file = request.FILES["audio"]
        save_path = os.path.join(settings.MEDIA_ROOT, audio_file.name)
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        with open(save_path, "wb") as f:
            for chunk in audio_file.chunks():
                f.write(chunk)

        # ===== librosa でピッチ解析 =====
        y, sr = librosa.load(save_path)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = [pitches[:, i].max() for i in range(pitches.shape[1])]

        # ===== matplotlib でグラフ生成 =====
        plt.figure(figsize=(12, 4))
        plt.plot(pitch_values, color='green', linewidth=2)
        plt.title("録音ピッチ解析")
        plt.xlabel("時間フレーム")
        plt.ylabel("周波数 [Hz]")
        plt.tight_layout()

        graph_path = os.path.join(settings.MEDIA_ROOT, "pitch_graph.png")
        plt.savefig(graph_path)
        plt.close()

        return render(request, "compose/game2_result.html", {"graph_url": f"/media/pitch_graph.png"})

    return render(request, "compose/game2_upload.html")