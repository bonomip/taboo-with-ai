## 🎮 Taboo YOLO Game
Taboo YOLO is an interactive, AI-powered word-guessing game that fuses creativity, vision AI, and classic party game mechanics.

Your goal? Describe a secret word without using the forbidden "taboo" words — and let AI be the judge!

## 🧠 How It Works
You're given an answer word (e.g., pizza) and a list of taboo words (e.g., Italian, Napoli, mozzarella).

You must write a creative sentence to describe the object — without using any of the taboo words.

The system uses Cloudflare Workers AI or Stable Diffusion to generate an image from your sentence.

Then, YOLOv8 (You Only Look Once) scans the image to detect if your described object actually appears.

If YOLO detects the target object → ✅ You win the round!
If not → ❌ Try again next round.

## ⚙️ Tech Stack
- Image Generation	Stable Diffusion (Cloudflare Workers AI / Hugging Face)
- Object Detection	YOLOv8 via Ultralytics
- Taboo Word Filtering	Python NLP string processing
- Backend Code	Pure Python

## ✨ Features
🧩 Classic Taboo game logic
🎨 Real-time AI image generation
🔍 Smart object detection with YOLO
🚫 Taboo word validation (with plural, case-insensitive matching)
🖼️ Image feedback with detection overlay
🪄 Extendable for multiplayer or web version

## 📦 Setup Instructions
``` bash
 # Clone the repo
git clone https://github.com/yourname/taboo-with-ai.git
cd taboo-with-ai

# Create and activate virtual environment
python3 -m venv taboo
source taboo/bin/activate  # or taboo\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Set up API keys (for image generation)
echo 'ACCOUNT_ID = "6362fed1c93bcd019be986b093d3a5bb"
API_TOKEN = "5O9fRfD9o7UiLgVb8kq-rOD9mWzMgO9XfYqEYFcW"' > key.txt

# Run the game!
python main.py
```

## 💡 Example Round
```
🎯 ANSWER: pizza  
🚫 TABOO WORDS: italian, napoli, mediterranean, mozzarella, tomato  

🤖 Describe it:
→ "A round dish with cheese, sauce, and toppings baked in the oven."
```
If YOLO detects a pizza in the generated image → ✅ you score a point!

## 🔄 Game Flow
```
📌 Round 1:
- You get a word and taboo list
- Write your prompt
- AI generates image
- YOLO checks for match
- Score is updated
```

Play multiple rounds and challenge your creativity while competing against the AI!

## 🧩 Coming Soon
- Multiplayer mode (pass & play or networked)
- Leaderboards
- Image customization and filters
- Better semantic taboo filtering
