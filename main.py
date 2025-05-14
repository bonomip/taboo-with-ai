import requests
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import base64
import random
import ast
import re

def read_credentials(filename="key.txt"):
    creds = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    creds[key.strip()] = value.strip().strip('"')
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    return creds

def load_taboo_file(filename="taboo.txt"):
    taboo_dict = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    key = key.strip().strip('"')
                    value = ast.literal_eval(value.strip())
                    taboo_dict[key] = value
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    return taboo_dict

def print_game_intro():
    print("""
    ========================================================
                      🎯 TABOO YOLO GAME 🎯
    ========================================================

    👋 Welcome to the Taboo YOLO Game!

    🧠 Objective:
        Describe a secret object or concept — but with a twist!
        You are given an ANSWER and a list of TABOO WORDS.
        Your challenge is to describe the object *without using* any taboo words.

    🚫 Taboo Words:
        These are words you CANNOT say in your description.
        Think creatively and give clues using alternative phrases!

    🖼️ How the Game Works:
        1. You will describe the answer (without taboo words).
        2. Your description will be passed to an image generator (like Stable Diffusion).
        3. YOLO (You Only Look Once) object detection will analyze the generated image.
        4. The AI tries to guess your original answer — based on what it *sees*.

    ✅ Example:
        ANSWER: "pizza"  
        TABOO WORDS: ["italian", "napoli", "mediterranean", "mozzarella", "tomato"]

        ✔ Valid Description:
            "A round dish with cheese, sauce, and toppings baked in the oven."

    🕹️ Your Turn:
        Get ready to describe without saying too much!
        Impress the AI with your creativity.

    ========================================================
    """)

def normalize(word):
    # Lowercase, remove punctuation, and strip simple plural
    word = re.sub(r'[^\w\s]', '', word.lower())  # Remove punctuation
    if word.endswith('s') and len(word) > 3:
        word = word[:-1]  # crude plural stripping
    return word

def get_user_input(answer, taboo_words):
    normalized_taboo_set = set(normalize(w) for w in [answer] + taboo_words)

    while True:
        user_input = input("👉 Your description: ")
        
        # Normalize and split user input
        words = [normalize(w) for w in user_input.split()]

        if any(w in normalized_taboo_set for w in words):
            print("\n🚫 Oops! Your description contains a taboo word or the answer itself.")
            print(f"❗ You cannot use '{answer}' or any of these taboo words: {', '.join(taboo_words)}.")
            print("🔁 Please try again.\n")
        else:
            return user_input

def generate_image(prompt, img_path):

    creds = read_credentials()

    ACCOUNT_ID = creds["ACCOUNT_ID"]
    API_TOKEN = creds["API_TOKEN"]

    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell"

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "seed": 5  # Optional, or randomize if you want
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        image_base64 = response.json()["result"]["image"]
        with open(img_path, "wb") as f:
            f.write(base64.b64decode(image_base64))
    else:
        raise Exception(str(response.status_code))

def validate_image(answer, img_path):
    # Load model and run detection
    model = YOLO("yolov8n.pt")
    results = model(img_path)

    # Open image for drawing
    img = Image.open(img_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Define what object we're looking for
    target_label = answer
    found = False

    for result in results:
        names = model.names  # class index to name
        boxes = result.boxes

        for box in boxes:
            cls_id = int(box.cls[0].item())  # class ID
            label = names[cls_id]

            if label == target_label:
                found = True
                # Get coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                
                # Draw bounding box
                draw.rectangle([(x1, y1), (x2, y2)], outline="green", width=6)
    return found, img, draw

def print_result(found, img, draw):
    # Load font
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", size=60)
    except:
        font = ImageFont.load_default()

    # Add "CORRECT" or "WRONG" at the bottom
    text = "CORRECT!" if found else "WRONG!"
    color = "green" if found else "red"

    # Get text size and position
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    image_width, image_height = img.size
    x = (image_width - text_width) // 2
    y = image_height - text_height - 50

    # Draw white outline by drawing text at offset positions
    outline_color = "white"
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color)

    # Draw green fill on top
    draw.text((x, y), text, fill=color, font=font)

    # Save and show result
    img.save("result.png")
    img.show()

def play_taboo_yolo_game(taboo_data, rounds=5):
    score = 0
    used_answers = set()  # To track answers that have already been used

    print("\n🔁 Starting the Taboo YOLO Challenge – 5 Rounds!\n")

    for i in range(1, rounds + 1):
        print(f"\n================== Round {i} ==================\n")

        # 1. Randomly select answer and taboo words
        available_answers = list(set(taboo_data.keys()) - used_answers)  # Remove already used answers
        answer = random.choice(available_answers)
        used_answers.add(answer)
        taboo_words = taboo_data[answer]

        # 2. Show the player their target
        print(f"🎯 Your target word is: **{answer.upper()}**")
        print(f"🚫 Taboo words: {', '.join(taboo_words)}")
        print("💬 Describe it without using any taboo words!\n")

        # 3. Get player input
        user_input = input("👉 Your description: ")

        # 4. Generate image from user input
        gen_img_name = f"generated_round_{i}.png"
        generate_image(user_input, gen_img_name)

        # 5. Use YOLO to detect if answer is in the generated image
        found, img, draw = validate_image(answer, gen_img_name)

        # 6. Display results and update score
        print_result(found, img, draw)

        if found:
            print("✅ Success! The AI guessed it.")
            score += 1
        else:
            print("❌ Missed! The AI didn’t recognize it.")

    # Final score summary
    print("\n=============================================")
    print(f"🏁 Game Over! You scored {score} out of {rounds}.")
    print("=============================================\n")

### Main function ###

# Load the dictionary
taboo_data = load_taboo_file()

print_game_intro()

play_taboo_yolo_game(taboo_data)