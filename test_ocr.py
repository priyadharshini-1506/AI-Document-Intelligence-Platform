from services.image_reader import read_image


image_path = r"C:\Users\priya\Downloads\WhatsApp Image 2026-07-10 at 20.26.46.jpeg"


text = read_image(image_path)


print("========== OCR OUTPUT ==========")
print(text)