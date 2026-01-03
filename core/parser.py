import chardet
import re

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def parse_srt(file_path):
    encoding = detect_encoding(file_path)
    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
        content = f.read()

    blocks = re.split(r'\n\s*\n', content.strip())
    subs = []
    for block in blocks:
        lines = block.split('\n')
        if len(lines) >= 3:
            idx = lines[0]
            timestamp = lines[1]
            text = '\n'.join(lines[2:])
            subs.append({'idx': idx, 'time': timestamp, 'text': text})
    return subs

def write_srt(file_path, subs):
    with open(file_path, 'w', encoding='utf-8') as f:
        for sub in subs:
            f.write(f"{sub['idx']}\n{sub['time']}\n{sub['text']}\n\n")

def parse_vtt(file_path):
    encoding = detect_encoding(file_path)
    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
        lines = f.readlines()
    
    subs = []
    current_time = None
    current_text = []
    
    start_idx = 0
    if lines[0].startswith("WEBVTT"):
        start_idx = 1
        
    i = start_idx
    while i < len(lines):
        line = lines[i].strip()
        if "-->" in line:
            current_time = line
            i += 1
            current_text = []
            while i < len(lines) and lines[i].strip() != "":
                current_text.append(lines[i].strip())
                i += 1
            subs.append({'idx': '', 'time': current_time, 'text': '\n'.join(current_text)})
        i += 1
    return subs

def write_vtt(file_path, subs):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("WEBVTT\n\n")
        for sub in subs:
            f.write(f"{sub['time']}\n{sub['text']}\n\n")

def get_parser(format_type):
    if format_type == '.srt':
        return parse_srt, write_srt
    elif format_type == '.vtt':
        return parse_vtt, write_vtt
    else:
        return None, None
