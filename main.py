import requests
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont

def read_api_key(filename="key.txt"):
    try:
        with open(filename, "r") as file:
            key = file.read().strip()
        return key
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None

def get_user_input(answer, taboo_words):
    # Display the instructions with the taboo words
    print(f"""
    --------------------------------------------------------
    Welcome to the Taboo YOLO Game!
    
    Objective:
    You need to describe an object or concept related to "{answer}".
    However, be careful! You are NOT allowed to use the following taboo words:
    
    {', '.join(taboo_words)}

    Instructions:
    Please describe the object or concept in a sentence WITHOUT using the taboo words.
    Your description should give enough clues for the image generator to create the correct image.

    Example:
    If the object is "pizza", a valid description might be: 
    "A round dish with cheese, sauce, and toppings baked in the oven."

    Now, go ahead and give it a try. What would you like to say to the image generator?

    --------------------------------------------------------

    Your description: 
    """)

    # Prompt user to input their description
    user_input = input()

    # Validate the input
    while any(word in user_input.lower() for word in [answer] + taboo_words):
        print("\nOops! Your description contains one or more taboo words.")
        print(f"Remember, you cannot use the target object '{answer}' or any of these taboo words: {', '.join(taboo_words)}.")
        print("\nPlease try again.")
        
        # Prompt the user again if the input was invalid
        user_input = input("Your description: ")
    
    return user_input

def generate_image(prompt, img_path):

    key = read_api_key()

    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/core",
        headers={
            "authorization": f"Bearer "+key,
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": prompt,
            "output_format": "png",
        },
    )

    if response.status_code == 200:
        with open("./"+img_path, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))

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

answer = "pizza"
taboo_words = ["italian", "napoli", "mediterranean", "mozzarella", "tomato"]
gen_img_name = "generated.png"
    
user_input = get_user_input(answer, taboo_words)

generate_image(user_input, gen_img_name)

found, img, draw = validate_image(answer, gen_img_name)

print_result(found, img, draw)
