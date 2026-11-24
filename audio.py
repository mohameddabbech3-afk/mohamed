"""Synthesized music bed + SFX for the well wishes short, mixed under voice.mp3."""
import numpy as np, subprocess, wave

SR = 48000

# Load voice to get duration
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", "voice.mp3", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
voice = np.frombuffer(raw, np.float32).copy()
DUR = len(voice) / SR
N = int(DUR * SR)
rng = np.random.default_rng(7)
t_all = np.arange(N) / SR

def env(n, a=0.005, r=0.2, sus=None):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / r)
    return e

def lp(x, k):
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)): acc += k * (x[i] - acc); y[i] = acc
    return y

def lp_fast(x, cutoff):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (f / cutoff) ** 4); return np.fft.irfft(X, len(x)).astype(np.float32)

def hp_fast(x, cutoff):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 - 1 / (1 + (f / cutoff) ** 4); return np.fft.irfft(X, len(x)).astype(np.float32)

def place(buf, sig, t0, gain=1.0):
    i = int(t0 * SR); j = min(N, i + len(sig))
    if i < N and j > i: buf[i:j] += sig[: j - i] * gain

midi = lambda m: 440 * 2 ** ((m - 69) / 12)

# ---------------- music ----------------
music = np.zeros(N, np.float32)
BPM = 72; beat = 60 / BPM
# Gentle, mystical progression - major with suspended chords
prog = [(60, [60, 64, 67]), (65, [65, 69, 72]), (67, [67, 71, 74]), (62, [62, 65, 69])]  # C F G Dm
def pluck(f, dur=0.5, bright=0.3):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum((bright ** k) * np.sin(2 * np.pi * f * (k + 1) * t) / (k + 1) for k in range(5))
    return (s * env(n, 0.01, dur * 0.4)).astype(np.float32)
def pad(fs, dur):
    n = int(dur * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for f in fs:
        ph = 2 * np.pi * f * t + 0.002 * np.sin(2 * np.pi * 0.5 * t)
        s += sum(np.sin((k + 1) * ph) / (k + 1) ** 1.5 for k in range(6))
    a = np.minimum(1, t / 0.5) * np.minimum(1, (dur - t) / 1.0).clip(0)
    return lp_fast((s * a).astype(np.float32), 800) / len(fs)
def chime(f, dur=1.2):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 1.5)
    s += 0.5 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 2)
    s += 0.25 * np.sin(2 * np.pi * f * 3 * t) * np.exp(-t * 3)
    return (s * 0.3).astype(np.float32)

# Music plays through most of the video, fades at reveal
MUSIC_END = DUR - 2.0
bar = 0; tt = 0.0
while tt < MUSIC_END:
    root, ch = prog[bar % 4]
    place(music, pad([midi(m) for m in ch], beat * 4 * 0.95), tt, 0.06)
    # Gentle pluck on downbeats
    for b in range(4):
        tb = tt + b * beat
        if tb >= MUSIC_END: break
        place(music, pluck(midi(root - 12), 0.6, 0.25), tb, 0.2)
        place(music, pluck(midi(ch[b % 3] + 12), 0.4, 0.4), tb + beat * 0.5, 0.08)
    # Occasional chime
    if bar % 2 == 0:
        place(music, chime(midi(root + 12), 2.0), tt + beat, 0.15)
    bar += 1; tt += beat * 4
# Fade out
i0 = int((MUSIC_END - 2.0) * SR); music[i0:] *= np.linspace(1, 0, N - i0) ** 4
# Soft drone for last 2 seconds
dn = int((DUR - MUSIC_END) * SR); td = np.arange(dn) / SR
drone = (np.sin(2 * np.pi * 65.4 * td) + 0.3 * np.sin(2 * np.pi * 98.0 * td)) * np.minimum(1, td / 1.5)
drone = lp_fast(drone.astype(np.float32), 400)
place(music, drone, MUSIC_END, 0.04)

# ---------------- sfx ----------------
sfx = np.zeros(N, np.float32)
def noise(d): return rng.standard_normal(int(d * SR)).astype(np.float32)
def plink(f0=800, d=0.8):
    n = int(d * SR); t = np.arange(n) / SR
    f = f0 * np.exp(-t * 3)
    ph = np.cumsum(f) / SR * 2 * np.pi
    s = np.sin(ph) * np.exp(-t * 4) * 0.5
    # Water resonance
    s += np.sin(2 * np.pi * 180 * t) * np.exp(-t * 8) * 0.2
    return s.astype(np.float32)
def water_ripple(d=1.0):
    n = int(d * SR); t = np.arange(n) / SR
    s = lp_fast(noise(d), 600) * np.exp(-t * 2) * 0.3
    return s.astype(np.float32)
def glow_chime(f=1200, d=1.5):
    n = int(d * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 1.2)
    s += 0.5 * np.sin(2 * np.pi * f * 1.5 * t) * np.exp(-t * 1.5)
    s += 0.25 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 2)
    return (s * 0.25).astype(np.float32)
def shimmer(d=2.0):
    n = int(d * SR); t = np.arange(n) / SR
    s = hp_fast(lp_fast(noise(d), 4000), 2000) * np.exp(-t * 0.5) * 0.15
    # Add subtle metallic tones
    for freq in [800, 1200, 1600, 2400]:
        s += np.sin(2 * np.pi * freq * t) * np.exp(-t * 0.8) * 0.03
    return s.astype(np.float32)
def warm_pad_chord(d=3.0):
    n = int(d * SR); t = np.arange(n) / SR
    # Major chord for happy ending
    s = sum(np.sin(2 * np.pi * midi(m) * t) * np.exp(-t * 0.3) for m in [60, 64, 67, 72])
    return (s * 0.1).astype(np.float32)
def whoosh(d=0.6):
    n = int(d * SR); t = np.arange(n) / SR
    return (lp_fast(noise(d), 1500) * np.sin(np.pi * t / d) ** 2 * 0.3).astype(np.float32)

F = lambda f: f / 30

# Shot 0: hook - ambient village, coin drop
place(sfx, water_ripple(3.0), F(5), 0.2)
place(sfx, plink(880, 1.2), F(15), 0.6)
place(sfx, glow_chime(1000, 1.5), F(20), 0.4)

# Shot 1: merchant - coin drop
place(sfx, plink(820, 1.2), F(100), 0.6)
place(sfx, glow_chime(950, 1.5), F(105), 0.4)
place(sfx, whoosh(0.4), F(180), 0.25)

# Shot 2: farmer - coin drop
place(sfx, plink(850, 1.2), F(220), 0.6)
place(sfx, glow_chime(1050, 1.5), F(225), 0.4)
place(sfx, whoosh(0.4), F(300), 0.25)

# Shot 3: bride - coin drop
place(sfx, plink(900, 1.2), F(340), 0.6)
place(sfx, glow_chime(1100, 1.5), F(345), 0.4)
place(sfx, whoosh(0.4), F(420), 0.25)

# Shot 4: elder - coin drop
place(sfx, plink(800, 1.2), F(460), 0.6)
place(sfx, glow_chime(900, 1.5), F(465), 0.4)

# Shot 5: reveal - camera plunges into well, magical glow
place(sfx, whoosh(1.0), F(575), 0.5)
place(sfx, shimmer(4.0), F(585), 0.6)
# Chord progression as each reflection appears
for i, freq in enumerate([800, 900, 1000, 1100]):
    place(sfx, glow_chime(freq, 2.0), F(590 + i * 25), 0.5)

# Shot 6: payoff - village happy, well glowing
place(sfx, warm_pad_chord(5.0), F(695), 0.4)
place(sfx, shimmer(6.0), F(700), 0.3)
# Rising sparkles
for i in range(8):
    place(sfx, glow_chime(1200 + i * 100, 1.5), F(710 + i * 10), 0.3)
# Final gentle chime
place(sfx, chime(midi(72), 3.0), F(780), 0.4)

# Save stems
def write_wav(path, sig):
    pcm = (np.clip(sig, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

write_wav("music.wav", music)
write_wav("sfx.wav", sfx)
print(f"ok music={music.max():.3f} sfx={sfx.max():.3f} dur={DUR:.2f}s")