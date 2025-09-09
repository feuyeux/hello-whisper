# Hello Whisper

```bash
# 1. 安装
python install.py

# 2. 激活环境
source whisper-env/bin/activate

# 3. 运行演示
python demo.py audio.mp3 -a       # 文件转录
python demo.py record -a          # 实时录音转录
```

注意：录音功能依赖已自动安装（sounddevice, numpy, scipy）

## 功能说明

### 文件转录

- 支持多种音频格式：mp3, wav, flac, m4a 等
- 基础转录：`python demo.py audio.mp3`
- 语言检测：`python demo.py audio.mp3 -l`
- 模型对比：`python demo.py audio.mp3 -c`
- 全部功能：`python demo.py audio.mp3 -a`

### 实时录音转录

- 实时录音并转录：`python demo.py record`
- 录音 + 语言检测：`python demo.py record -l`
- 录音 + 全部功能：`python demo.py record -a`
- 录音时按 Ctrl+C 停止

## 模型说明

| 模型   | 大小  | 内存  | 速度 | 用途     |
| ------ | ----- | ----- | ---- | -------- |
| tiny   | 39M   | ~1GB  | 最快 | 快速测试 |
| base   | 74M   | ~1GB  | 快   | 日常使用 |
| turbo  | 809M  | ~6GB  | 推荐 | 最佳平衡 |
| medium | 769M  | ~5GB  | 慢   | 翻译功能 |
| large  | 1550M | ~10GB | 最慢 | 最高精度 |

## 参考

- [OpenAI Whisper](https://github.com/openai/whisper)
- [论文](https://arxiv.org/abs/2212.04356)
