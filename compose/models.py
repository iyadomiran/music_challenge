from django.db import models
from django.contrib.auth.models import User

class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ← Userと紐付け
    score = models.IntegerField()                             # ← 得点
    played_at = models.DateTimeField(auto_now_add=True)        # ← プレイ日時

    def __str__(self):
        return f"{self.user.username} - {self.score} ({self.played_at})"