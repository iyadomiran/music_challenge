from django.db import models
from django.conf import settings

class Challenge(models.Model):
    """
    ゲームの1回分の記録（最小構成）
    - user: ログインユーザー（ゲストは None）
    - level: ゲームのレベル（'game2' など）
    - correct: 正解の音名（例: "do,re,mi,fa"）
    - user_answer: ユーザーが歌った音名（例: "do,re,mi,fa"）
    - created_at: 作成日時
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    level = models.CharField(max_length=32, blank=True)        # 'game2' など
    correct = models.CharField(max_length=255, blank=True)     # 正解音名
    user_answer = models.CharField(max_length=255, blank=True) # ユーザー音名
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_name = self.user.username if self.user else "Guest"
        return f"{user_name} - {self.level} - {self.created_at:%Y-%m-%d %H:%M:%S}"