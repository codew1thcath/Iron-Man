import cv2
import mediapipe as mp
import numpy as np
import ctypes
import pygame
import os
import tkinter as tk
from tkinter import filedialog

# --- Init pygame music player ---
pygame.mixer.init()

# --- Pick music file ---
root = tk.Tk()
root.withdraw()
music_path = filedialog.askopenfilename(
    title="Select a Music File",
    filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")]
)

if music_path:
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)  # loop forever
    song_name = os.path.basename(music_path)
else:
    song_name = "No music loaded"

# --- Volume keys ---
VK_VOLUME_UP = 0xAF
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_MUTE = 0xAD

# --- Gesture state ---
current_vol_pct = [50]
is_muted = [False]
is_paused = [False]
prev_fist = [False]
prev_peace = [False]

def count_fingers(lm_list):
    """Count how many fingers are up"""
    fingers = []
    # Thumb
    fingers.append(1 if lm_list[4][1] < lm_list[3][1] else 0)
    # 4 fingers (index to pinky)
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    for tip, pip in zip(tips, pips):
        fingers.append(1 if lm_list[tip][2] < lm_list[pip][2] else 0)
    return fingers

def set_volume_direct(target_percent, current_percent=[50]):
    diff = int((target_percent - current_percent[0]) / 2)
    key = VK_VOLUME_UP if diff > 0 else VK_VOLUME_DOWN
    for _ in range(abs(diff)):
        ctypes.windll.user32.keybd_event(key, 0, 0, 0)
        ctypes.windll.user32.keybd_event(key, 0, 2, 0)
    current_percent[0] = target_percent

def draw_hud(img, vol_pct, song_name, is_paused, is_muted, gesture_label):
    h, w, _ = img.shape

    # Semi-transparent overlay top bar
    overlay = img.copy()
    cv2.rectangle(overlay, (0, 0), (w, 70), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, img, 0.5, 0, img)

    # Song name
    display_name = song_name[:45] + "..." if len(song_name) > 45 else song_name
    cv2.putText(img, f"♪ {display_name}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 180), 2)

    # Status
    status = "⏸ PAUSED" if is_paused else ("🔇 MUTED" if is_muted else "▶ PLAYING")
    cv2.putText(img, status, (10, 58),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 200, 255), 2)

    # Volume bar (right side)
    bar_top = 100
    bar_bot = 400
    bar_x = w - 60
    filled = int(np.interp(vol_pct, [0, 100], [bar_bot, bar_top]))
    cv2.rectangle(img, (bar_x, bar_top), (bar_x + 35, bar_bot), (50, 50, 50), -1)
    color = (0, 100, 255) if is_muted else (0, 255, 180)
    cv2.rectangle(img, (bar_x, filled), (bar_x + 35, bar_bot), color, -1)
    cv2.rectangle(img, (bar_x, bar_top), (bar_x + 35, bar_bot), (255, 255, 255), 2)
    cv2.putText(img, f"{vol_pct}%", (bar_x - 5, bar_bot + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    cv2.putText(img, "VOL", (bar_x, bar_top - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Gesture label bottom
    if gesture_label:
        cv2.putText(img, gesture_label, (10, h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    # Controls guide
    guide = ["[GESTURES]",
             "Pinch: Volume",
             "Fist: Play/Pause",
             "Peace V: Mute",
             "Q: Quit"]
    for i, line in enumerate(guide):
        cv2.putText(img, line, (10, 110 + i * 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (200, 200, 200) if i > 0 else (0, 255, 255), 1)

# --- Setup ---
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
gesture_label = [""]

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)  # Mirror view
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # Draw hand
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS,
                mp_draw.DrawingSpec(color=(0,255,180), thickness=2, circle_radius=4),
                mp_draw.DrawingSpec(color=(0,180,255), thickness=2))

            lm_list = []
            h, w, c = img.shape
            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))

            if lm_list:
                fingers = count_fingers(lm_list)
                total_fingers = sum(fingers)

                # ✊ FIST = Play / Pause
                if total_fingers == 0:
                    if not prev_fist[0]:
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.pause()
                            is_paused[0] = True
                        else:
                            pygame.mixer.music.unpause()
                            is_paused[0] = False
                        gesture_label[0] = "✊ Play / Pause"
                    prev_fist[0] = True
                else:
                    prev_fist[0] = False

                # ✌ PEACE SIGN = Mute toggle
                if fingers == [0, 1, 1, 0, 0]:
                    if not prev_peace[0]:
                        is_muted[0] = not is_muted[0]
                        ctypes.windll.user32.keybd_event(VK_VOLUME_MUTE, 0, 0, 0)
                        ctypes.windll.user32.keybd_event(VK_VOLUME_MUTE, 0, 2, 0)
                        gesture_label[0] = "✌ Mute Toggle"
                    prev_peace[0] = True
                else:
                    prev_peace[0] = False

                # 🤏 PINCH (thumb + index) = Volume control
                if fingers[1] == 1 and total_fingers <= 2:
                    x1, y1 = lm_list[4][1], lm_list[4][2]
                    x2, y2 = lm_list[8][1], lm_list[8][2]

                    cv2.circle(img, (x1, y1), 12, (255, 100, 0), cv2.FILLED)
                    cv2.circle(img, (x2, y2), 12, (255, 100, 0), cv2.FILLED)
                    cv2.line(img, (x1, y1), (x2, y2), (255, 100, 0), 3)

                    length = np.hypot(x2 - x1, y2 - y1)
                    vol_pct = int(np.interp(length, [30, 200], [0, 100]))

                    if abs(vol_pct - current_vol_pct[0]) > 3:
                        set_volume_direct(vol_pct, current_vol_pct)
                        pygame.mixer.music.set_volume(vol_pct / 100)

                    gesture_label[0] = f"🤏 Volume: {vol_pct}%"

    draw_hud(img, current_vol_pct[0], song_name,
             is_paused[0], is_muted[0], gesture_label[0])

    cv2.imshow("Iron Man Music Controller", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()