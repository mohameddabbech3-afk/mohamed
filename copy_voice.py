import shutil
import os

src = r"C:\Users\Adem\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Local\Claude-3p\local-agent-mode-sessions\b1d93b46\00000000\e97e86d3\uploads\ElevenLabs_2026-11-23T21_49_13_Ahmed - Natural & Clear_pvc_s47_sim75_v4.mp3"
dst = r"C:\Users\Adem\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Local\Claude-3p\local-agent-mode-sessions\b1d93b46\00000000\e97e86d3\outputs\shorts\well-wishes\voice.mp3"

os.makedirs(os.path.dirname(dst), exist_ok=True)
shutil.copy2(src, dst)
print(f"Copied {os.path.getsize(dst)} bytes to {dst}")