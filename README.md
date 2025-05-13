## 🕹️ Taboo YOLO Game
Taboo YOLO Game is an interactive AI-powered word-guessing game where players must describe a hidden object without using taboo words, and an image generator + object detector decide if they win the round!

The game combines:

🎨 Image generation (via Stable Diffusion or DALL·E)

🧠 Object detection using YOLOv8

🧩 A fun twist on the classic Taboo game

## 🚀 How It Works
The player is given a target word (e.g., "pizza") and a list of taboo words (e.g., "Italian", "Napoli").

They must write a creative sentence to describe the target without using the forbidden terms.

The system uses a text-to-image model to generate an image based on that sentence.

Then, YOLOv8 scans the generated image to check if it contains the target object.

If YOLO finds the object — ✅ CORRECT!
If not — ❌ WRONG.

## 🧰 Tech Stack
Python

YOLOv8 (Ultralytics)

Stable Diffusion (via Hugging Face)

Pillow and Tkinter for GUI and image editing

OpenAI or Hugging Face APIs for image generation

## ✨ Features
Fun and educational image-based guessing game

Real-time object detection feedback

Taboo word filtering and validation

Simple and intuitive GUI

Easily extendable for more complex game logic

## 📦 Setup
Clone the repo

Install dependencies

Set your API keys (for image generation)

Run the game and start playing!

```bash
pip install -r requirements.txt
python main.py
```
## 💡 Example Prompt
Describe “pizza” without using: pizza, italian, napoli, table
→ “A round dish with melted cheese and crispy crust baked in an oven”

🧠 Your creativity decides if the AI sees it too!
