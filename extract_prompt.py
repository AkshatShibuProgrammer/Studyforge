import json

log_file = r'C:\Users\Aksha\.gemini\antigravity\brain\34ca128d-e077-4e14-b881-df4642c4ba75\.system_generated\logs\transcript_full.jsonl'
user_msgs = []

try:
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get('type') == 'USER_INPUT':
                    user_msgs.append(data.get('content'))
            except Exception as e:
                pass
except Exception as e:
    print(f"Error opening file: {e}")

if user_msgs:
    with open('prompt10.txt', 'w', encoding='utf-8') as out:
        out.write(user_msgs[-1])
    print(f"Extracted prompt 10! Size: {len(user_msgs[-1])} bytes")
else:
    print("No user messages found.")
