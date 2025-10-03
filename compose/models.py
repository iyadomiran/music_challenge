from django.db import models                      # Djangoでデータベースのモデルを作るために必要
from django.contrib.auth.models import User       # Django標準のユーザー情報（ログイン情報）を使う

# ゲームのスコアを記録するモデル
class Score(models.Model):
    # このスコアがどのユーザーのものかを記録
    # User が削除されたら、そのユーザーのスコアも自動で削除される
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ← どのユーザーのスコアか

    # ユーザーがゲームで獲得した点数
    score = models.IntegerField()                             # ← 得点

    # スコアが記録された日時
    # auto_now_add=True にすると、データ作成時に自動で現在日時を入れてくれる
    played_at = models.DateTimeField(auto_now_add=True)        # ← プレイ日時

    # 管理画面やターミナルで見たときにわかりやすく表示する文字列
    # 例: "tanaka - 150 (2025-10-03 22:00:00)"
    def __str__(self):
        return f"{self.user.username} - {self.score} ({self.played_at})"
    
    # ゲームの正解曲パターンを保存するモデル
class SongPattern(models.Model):
    # 難易度を表すフィールド（初級・中級・上級）
    LEVEL_CHOICES = [
        ("beginner", "初級"),
        ("intermediate", "中級"),
        ("advanced", "上級"),
    ]
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)  # ← 難易度

    # 正解の音列パターンを JSON 形式で保存
    # 例: ["do", "re", "mi"] のように配列で保存
    pattern = models.JSONField()  # ← 正解曲パターン

    # 管理画面やターミナルでわかりやすく表示する文字列
    # 例: "beginner - ['do', 're', 'mi']"
    def __str__(self):
        return f"{self.level} - {self.pattern}"