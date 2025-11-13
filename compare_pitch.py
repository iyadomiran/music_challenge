import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# ===== ファイルパス設定 =====
# 問題音ファイル（例）
problem_path = "static/sounds/game2-1.mp3"
# 録音した音声ファイル（例）
recorded_path = "media/recorded_20251112030015.webm"

# ===== 問題音をロード =====
problem_y, problem_sr = librosa.load(problem_path)
problem_pitch, _ = librosa.piptrack(y=problem_y, sr=problem_sr)
problem_pitches = problem_pitch[np.nonzero(problem_pitch)]
problem_times = librosa.frames_to_time(np.arange(len(problem_pitches)), sr=problem_sr)

# ===== 録音音をロード =====
recorded_y, recorded_sr = librosa.load(recorded_path)
recorded_pitch, _ = librosa.piptrack(y=recorded_y, sr=recorded_sr)
recorded_pitches = recorded_pitch[np.nonzero(recorded_pitch)]
recorded_times = librosa.frames_to_time(np.arange(len(recorded_pitches)), sr=recorded_sr)

# ===== グラフ描画 =====
plt.figure(figsize=(12, 6))
plt.plot(problem_times, problem_pitches, label="問題音 (正解)", color='red', linewidth=2)
plt.plot(recorded_times, recorded_pitches, label="録音音 (あなたの声)", color='green', linewidth=2)
plt.title("ピッチ比較（赤＝問題音, 緑＝録音音）")
plt.xlabel("時間 [秒]")
plt.ylabel("周波数 [Hz]")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment  # webm→wav変換用

# ===== ファイルパス設定 =====
problem_path = "static/sounds/game2-1.mp3"
recorded_path = "media/recorded_20251112030015.webm"
recorded_wav_path = "media/recorded_20251112030015.wav"  # 変換後のWAV

# ===== 録音音を WAV に変換 =====
audio = AudioSegment.from_file(recorded_path)
audio.export(recorded_wav_path, format="wav")

# ===== 問題音をロード =====
problem_y, problem_sr = librosa.load(problem_path, sr=None)
problem_pitch, _ = librosa.piptrack(y=problem_y, sr=problem_sr)
problem_pitches = problem_pitch[np.nonzero(problem_pitch)]
problem_times = librosa.frames_to_time(np.arange(len(problem_pitches)), sr=problem_sr)

# ===== 録音音をロード =====
recorded_y, recorded_sr = librosa.load(recorded_wav_path, sr=None)
recorded_pitch, _ = librosa.piptrack(y=recorded_y, sr=recorded_sr)
recorded_pitches = recorded_pitch[np.nonzero(recorded_pitch)]
recorded_times = librosa.frames_to_time(np.arange(len(recorded_pitches)), sr=recorded_sr)

# ===== グラフ描画 =====
plt.figure(figsize=(12, 6))
plt.plot(problem_times, problem_pitches, label="問題音 (正解)", color='red', linewidth=2)
plt.plot(recorded_times, recorded_pitches, label="録音音 (あなたの声)", color='green', linewidth=2)
plt.title("ピッチ比較（赤＝問題音, 緑＝録音音）")
plt.xlabel("時間 [秒]")
plt.ylabel("周波数 [Hz]")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
