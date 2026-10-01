# Chat to Calendar

Using this locally running app, turn your messy college group chat into calendar events using an open-weight AI model that runs entirely on your own laptop. Just paste in your chat and get back an .ics file you can import into Google Calendar, Apple Calendar or Outlook.

# How it works?
- No API key, no account and no internet connection required to run this model once downloaded
- Your chats never leave your machine so your data is safe
- Model used : llama3.2 (open-weight), run locally with Ollama
- Output format: JSON

# Installation and Setup
1. Install Ollama  
2. Download the model  
   ```ollama pull llama3.2```
3. Install the python library  
```pip install ollama```
4. Clone this repo  
```https://github.com/Mahi-Chandra/chat-to-calendar.git```
5. Run using  
```python app.py sample_chat.txt```

This prints the important events it found and saves events.ics
Open that file or import it into your calendar app!

---
Built at the Hacktober 2026 hack day.
