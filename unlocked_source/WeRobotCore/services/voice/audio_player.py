# Decompiled from: audio_player.pyc
# Python 3.12 bytecode (mode: cfg)

"""
将 mp3 文件以阻塞方式播放到指定 sounddevice 输出设备。

主要使用场景：AI 语音回复 — 把豆包合成的 mp3 流向 VB-Cable Input，让微信
从 CABLE Output 录到这段音频。

实现注意：刻意避开 numpy 和 pydub。
  - numpy: PyInstaller frozen 下 numpy._core._multiarray_umath 首次加载报
    "cannot load module more than once per process"。
  - pydub: 内部 subprocess.Popen 调 ffmpeg 时不传 CREATE_NO_WINDOW，
    每次解码都会闪一个白色 ffmpeg 控制台窗口（实测）。

链路：ffmpeg subprocess (CREATE_NO_WINDOW) → raw 16-bit PCM bytes
     → sounddevice.RawOutputStream 喂播放。
全程无 numpy / 无 pydub / 无窗口闪烁。
"""

__doc__ = "\n将 mp3 文件以阻塞方式播放到指定 sounddevice 输出设备。\n\n主要使用场景：AI 语音回复 — 把豆包合成的 mp3 流向 VB-Cable Input，让微信\n从 CABLE Output 录到这段音频。\n\n实现注意：刻意避开 numpy 和 pydub。\n  - numpy: PyInstaller frozen 下 numpy._core._multiarray_umath 首次加载报\n    \"cannot load module more than once per process\"。\n  - pydub: 内部 subprocess.Popen 调 ffmpeg 时不传 CREATE_NO_WINDOW，\n    每次解码都会闪一个白色 ffmpeg 控制台窗口（实测）。\n\n链路：ffmpeg subprocess (CREATE_NO_WINDOW) → raw 16-bit PCM bytes\n     → sounddevice.RawOutputStream 喂播放。\n全程无 numpy / 无 pydub / 无窗口闪烁。\n"
from __future__ import annotations
import os
import subprocess
from typing import Optional
import sounddevice as sd
_DEFAULT_SR = 44100
_DEFAULT_CHANNELS = 2
_SAMPLE_WIDTH = 2
_CREATE_NO_WINDOW = 134217728
def _hidden_subprocess_kwargs():
    """返回 subprocess.run / Popen 在 Windows 上完全隐藏子进程窗口的参数集。
        creationflags + startupinfo 双重保险 — 二者任一生效都不会闪窗口。"""

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = 0
    return {"creationflags": _CREATE_NO_WINDOW, "startupinfo": startupinfo}
    return {}
def _decode_mp3_to_pcm_bytes(mp3_path, samplerate, channels):
    """
        用 ffmpeg subprocess 解码 mp3 → 16-bit little-endian raw PCM bytes。
        Windows 下 ffmpeg 子进程窗口完全隐藏（CREATE_NO_WINDOW + SW_HIDE）。
        """

    cmd = ["ffmpeg", "-loglevel", "error", "-i", mp3_path, "-f", "s16le", "-acodec", "pcm_s16le", "-ac", str(channels), "-ar", str(samplerate), "-"]
    proc = subprocess.run(*(cmd,), **{**{"capture_output": True}, **_hidden_subprocess_kwargs()})
    return proc.stdout
    raise RuntimeError("ffmpeg 输出为空")
    err = 300
    raise RuntimeError("ffmpeg decode 失败: ", f'{err}')
    raise FileNotFoundError("mp3 文件不存在: ", f'{mp3_path}')
def play_mp3_to_device(mp3_path, device_index, target_samplerate, pre_silence_sec, post_silence_sec):
    """
        把 mp3 文件解码后通过 sounddevice 播到指定输出设备。**阻塞**直到播放完成。

        参数：
          mp3_path           本地 mp3 文件路径
          device_index       sounddevice 输出索引（来自 audio_devices.find_cable_input_sd_index）
          target_samplerate  目前未使用（保持向后兼容；固定按 44100Hz 解码）
          pre_silence_sec    播放前预留的静音秒数（让 WeChat 录音 UI 有时间起来）
          post_silence_sec   播放后追加的静音秒数（避免末尾被截断）

        返回：实际播放的总秒数（含 pre / post silence）。
        抛出：FileNotFoundError / RuntimeError（解码失败 / 设备不可用）。
        """

    samplerate = _DEFAULT_SR
    channels = _DEFAULT_CHANNELS
    bytes_per_frame = _SAMPLE_WIDTH * channels
    pcm_bytes = _decode_mp3_to_pcm_bytes(mp3_path, samplerate, channels)
    pre_silence = b''
    post_silence = b''
    full_bytes = pre_silence + pcm_bytes + post_silence
    total_frames = len(full_bytes) // bytes_per_frame
    stream = sd.RawOutputStream(samplerate=samplerate, channels=channels, dtype="int16", device=device_index)
    stream.write(full_bytes)
    None(None, None)
    return total_frames / float(samplerate)
    post_silence = b'\x00' * int(samplerate * post_silence_sec) * bytes_per_frame
    pre_silence = b'\x00' * int(samplerate * pre_silence_sec) * bytes_per_frame
