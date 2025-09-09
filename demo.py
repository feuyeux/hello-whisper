#!/usr/bin/env python3
"""Hello Whisper 演示脚本 - 支持文件转录和实时录音转录"""
import sys
import os
import time
import whisper
import tempfile
import signal
try:
    import sounddevice as sd
    import numpy as np
    import scipy.io.wavfile as wavfile
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False


def record_audio():
    """录制音频并返回临时文件路径"""
    if not AUDIO_AVAILABLE:
        print("❌ 缺少录音依赖: pip install sounddevice numpy scipy")
        return None

    print("🎤 开始录音... (按 Ctrl+C 停止)")

    sample_rate = 16000
    audio_data = []
    recording = [True]  # 使用列表避免闭包问题

    def callback(indata, frames, time, status):
        if recording[0]:
            audio_data.append(indata.copy())

    def signal_handler(sig, frame):
        recording[0] = False

    signal.signal(signal.SIGINT, signal_handler)

    try:
        with sd.InputStream(samplerate=sample_rate, channels=1,
                            callback=callback, dtype='float32'):
            while recording[0]:
                time.sleep(0.1)
    except KeyboardInterrupt:
        pass

    print("\n🛑 录音结束")

    if not audio_data:
        print("❌ 没有录到音频")
        return None

    # 保存音频
    audio_array = np.concatenate(audio_data, axis=0)
    temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    audio_int16 = (audio_array * 32767).astype(np.int16)
    wavfile.write(temp_file.name, sample_rate, audio_int16)

    print(f"💾 音频已保存")
    return temp_file.name


def transcribe_audio(audio_file, show_language=False):
    """转录音频文件"""
    print("🎯 正在转录...")
    available_models = whisper.available_models()
    print(f"可用模型: {available_models}")
    # 可用模型: ['tiny.en', 'tiny', 'base.en', 'base',
    # 'small.en', 'small', 'medium.en', 'medium',
    # 'large-v1', 'large-v2', 'large-v3', 'large',
    # 'large-v3-turbo', 'turbo']
    model = whisper.load_model("turbo")
    result = model.transcribe(audio_file)

    print(f"\n文本: {result['text']}")

    if show_language:
        # 语言检测
        audio = whisper.load_audio(audio_file)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(
            audio, n_mels=model.dims.n_mels).to(model.device)
        _, probs = model.detect_language(mel)

        print("\n🌐 语言检测:")
        sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)
        for lang, prob in sorted_probs[:3]:
            print(f"  {lang}: {prob:.3f} ({prob*100:.1f}%)")


def show_usage():
    """显示使用说明"""
    print("Hello Whisper 演示脚本")
    print("用法:")
    print("  python demo.py <音频文件>     # 文件转录")
    print("  python demo.py <音频文件> -l  # 文件转录 + 语言检测")
    print("  python demo.py record        # 实时录音转录")
    print("  python demo.py record -l     # 实时录音 + 语言检测")


def main():
    if len(sys.argv) < 2:
        show_usage()
        return

    first_arg = sys.argv[1]
    show_language = '-l' in sys.argv or '-a' in sys.argv

    audio_file = None

    if first_arg == "record":
        print("🎙️ 实时录音模式")
        audio_file = record_audio()
        if not audio_file:
            return
    else:
        if not os.path.exists(first_arg):
            print(f"❌ 文件不存在: {first_arg}")
            return
        audio_file = first_arg

    try:
        transcribe_audio(audio_file, show_language)
        print("\n✅ 完成!")

        # 清理录音临时文件
        if first_arg == "record" and audio_file and os.path.exists(audio_file):
            os.unlink(audio_file)
            print("🗑️ 已清理临时文件")

    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == "__main__":
    main()
