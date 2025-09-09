#!/usr/bin/env python3
"""
Hello Whisper 安装脚本
仅负责创建虚拟环境和安装依赖
"""
import os
import sys
import subprocess


def run_command(cmd, description):
    """运行命令"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        print(f"✅ {description}完成")
        return True
    except Exception as e:
        print(f"❌ {description}失败: {e}")
        return False


def install_whisper():
    """安装 Whisper 环境"""
    print("🎤 Hello Whisper 安装")
    print("=" * 30)

    # 检查 Python 版本
    if sys.version_info < (3, 8):
        print("❌ 需要 Python 3.8+")
        return False

    print(f"🐍 Python {sys.version_info.major}.{sys.version_info.minor}")

    # 创建虚拟环境
    if not os.path.exists("whisper-env"):
        if not run_command("python -m venv whisper-env", "创建虚拟环境"):
            return False

    # 安装依赖
    pip_path = "whisper-env/bin/pip" if os.name != 'nt' else "whisper-env\\Scripts\\pip"

    if not run_command(f"{pip_path} install --upgrade pip", "升级 pip"):
        return False

    if not run_command(f"{pip_path} install -U openai-whisper", "安装 Whisper"):
        return False

    # 安装录音功能依赖
    if not run_command(f"{pip_path} install sounddevice numpy scipy", "安装录音功能依赖"):
        return False

    return True


def main():
    if install_whisper():
        print("\n🎉 安装完成!")
        print("激活环境: source whisper-env/bin/activate")
        print("文件转录: python demo.py audio.mp3")
        print("实时录音: python demo.py record")


if __name__ == "__main__":
    main()
