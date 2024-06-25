
import os
import logging
import re
from datetime import timedelta
def split_text_by_multiple_breaks(input_string,uv_breaks):
    # 使用正则表达式按 uv_break 分割字符串并保留 uv_break 和紧随其后的标点符号
    segments = re.split(r'(\[uv_break\]\s*[\u3000-\u303F\uFF00-\uFFEF\u0020-\u007E]*)', input_string)

    # segments = re.split(pattern, input_string)
    #
    # 将标点与前面的字符串连接
    result = []
    for i in range(0, len(segments) - 1, 2):
        combined_segment = segments[i] + segments[i + 1]
        result.append("[speed_5]"+combined_segment.strip())

    # 添加最后一个分割段（如果存在并且不为空）
    if len(segments) % 2 == 1 and segments[-1].strip():
        result.append("[speed_5]"+segments[-1].strip())

    return result
# TODO 替换语气词
def text_Replace_Tone(input_string,uv_breaks):
    # 替换 result 中每个段落中的 uv_break 为 ""
    symbol_pattern = re.compile(r'[\u3000-\u303F\uFF00-\uFFEF\u0020-\u007E]$')
    for uv_break in uv_breaks:
        input_string = input_string.replace(uv_break, '')
        if symbol_pattern.search(input_string):
            input_string = input_string[:-1]
    return input_string
# TODO 格式化字幕时间
def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int(td.microseconds / 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"
    # TODO SRT 字幕文件写入文件
def write_srt_file( srt_entries,filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for entry in srt_entries:
            f.write(f"{entry['index']}\n")
            f.write(f"{entry['start']} --> {entry['end']}\n")
            f.write(f"{entry['text']}\n\n")
def remove_suffix(text:str, suffix:str):
    # 如果字符串以后缀结尾，返回去除后缀的字符串，否则返回原字符串
    return text[:-len(suffix)] if text.endswith(suffix) else text