import json

with open(r"C:\Users\Aksha\.gemini\antigravity\brain\34ca128d-e077-4e14-b881-df4642c4ba75\.system_generated\logs\transcript_full.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        if data.get("type") == "USER_INPUT" and "check this example ?" in data.get("content", ""):
            with open("match.txt", "w", encoding="utf-8") as out:
                out.write(data["content"])
            break
