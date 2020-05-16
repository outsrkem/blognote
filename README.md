# 蜗牛笔记博客开发学习

### https://www.bilibili.com/video/BV1U64y1u77k/?p=15

### 启动命令
```python
python3 main.py
gunicorn -w 4 -b 0.0.0.0:5000   --access-logfile ./log main:app –preload
```