import sys
import json
import datetime
import ollama


def extract_events(chat_text):
    today = datetime.date.today().strftime("%A, %Y-%m-%d")
    prompt = f"""Today is {today}.
    Extract every event, deadline or meeting from this group chat.
    Reply ONLY with JSON in exactly this form:
    {{"events": [{{"title": "...", "date": "YYYY-MM-DD", "time": "HH:MM", "location": "..."}}]}}
    Use "" for anything unknown. Convert words like "tomorrow" or "friday" into real dates.

    CHAT:
    {chat_text}"""

    reply = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}],
        format="json",
    )

    content = reply.message.content


    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        print(f"ERROR: Model returned invalid JSON:\n{content}")
        return []

    if "events" not in data:
        print(f"ERROR: JSON missing 'events' key. Got:\n{data}")
        return []

    return data["events"]


def write_ics(events, filename="events.ics"):
    now = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//ChatChaos//EN"]
    for i, e in enumerate(events):
        if not e.get("date"):
            continue
        d = e["date"].replace("-", "")
        t = (e.get("time") or "09:00").replace(":", "") + "00"
        lines += [
            "BEGIN:VEVENT",
            f"UID:chatchaos-{i}-{now}",
            f"DTSTAMP:{now}",
            f"SUMMARY:{e.get('title', 'Event')}",
            f"DTSTART:{d}T{t}",
            f"LOCATION:{e.get('location', '')}",
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    with open(filename, "w", encoding="utf-8", newline="") as f:
        f.write("\r\n".join(lines) + "\r\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <chat.txt>")
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as f:
        chat = f.read()
    events = extract_events(chat)
    if events:
        print(f"Found {len(events)} event(s):")
        for e in events:
            print(f"  • {e.get('title', '?')} — {e.get('date', '?')} {e.get('time', '?')}")
        write_ics(events)
        print("Saved events.ics ✓")
    else:
        print("No events found.")
