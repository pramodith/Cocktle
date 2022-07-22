from difflib import ndiff
from PIL import Image

def levenshtein_distance(str1, str2, ):
    counter = {"+": 0, "-": 0}
    distance = 0
    for edit_code, *_ in ndiff(str1, str2):
        if edit_code == " ":
            distance += max(counter.values())
            counter = {"+": 0, "-": 0}
        else:
            counter[edit_code] += 1
    distance += max(counter.values())
    return distance

def get_image(image_name):
    image = Image.open(f"../data/images/{image_name}.png")
    image = image.resize((300, 300))
    return image