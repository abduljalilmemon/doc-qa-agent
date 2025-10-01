import re

def split_sentence(text: str):
    if not text:
        return []
    text = re.sub(r'\s+', ' ', text).strip()
    parts = re.split(r'(?<=[.!?])\s+', text)
    merged = []
    buffer = ""
    for p in parts:
        if len(p) < 40:
            buffer = (buffer + " " + p).strip()
            continue
        if buffer:
            merged.append((buffer + " " + p).strip())
            buffer = ""
        else:
            merged.append(p.strip())
    if buffer:
        merged.append(buffer.strip())
    return [s for s in merged if s]
