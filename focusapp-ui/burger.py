import pytesseract
from PIL import Image
import pyautogui
import cv2
import numpy as np
import time
time.sleep(2)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Указываем путь к папке tessdata
tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'

# Координаты области для захвата текста заказа справа
right_box = (1000, 50, 600, 1200)
# Координаты области для поиска и клика по ингредиентам слева
left_box = (281, 331, 673, 798)

# Словарь с ингредиентами и соответствующими путями к их изображениям
ingredient_files = {
    "Котлета Куриная": "14.png",
    "Салат 1": "26.png",
    "Салями": "28.png",
    "Сыр": "29.png",
    "Авокадо": "1.png",
    "Креветки": "15.png",
    "Огурцы маринованные": "21.png",
    "Грибы": "10.png",
    "Бекон": "4.png",
    "Васаби": "7.png",
    "Горчица": "9.png",
    "Паприка": "22.png",
    "Салат 2": "27.png",
    "Барбекю": "3.png",
    "Перец Чили": "23.png",
    "Лук": "17.png",
    "Картошка Фри": "11.png",
    "Лосось": "16.png",
    "Котлета Говяжья": "13.png",
    "Ветчина": "8.png",
    "Огурцы": "20.png",
    "Майонез": "18.png",
    "Помидор": "24.png",
    "Булка Вверх": "5.png",
    "Ананас": "2.png",
    "Булка Низ": "6.png",
    "Руккола": "25.png",
    "Яичница": "30.png",
    "Маслины": "19.png",
    "Кетчуп": "12.png"
}

def capture_and_ocr(box):
    screenshot = pyautogui.screenshot(region=box)
    text = pytesseract.image_to_string(screenshot, lang='rus', config=tessdata_dir_config)
    return text

def capture_left_box(box):
    screenshot = pyautogui.screenshot(region=box)
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    return screenshot

def find_and_click_ingredient(ingredient_image_path, left_box_screenshot):
    ingredient_image = cv2.imread(ingredient_image_path, cv2.IMREAD_GRAYSCALE)
    if ingredient_image is None:
        print(f"Не удалось загрузить изображение: {ingredient_image_path}")
        return  # Пропускаем этот ингредиент, если изображение не найдено
    if ingredient_image.shape[0] > left_box_screenshot.shape[0] or ingredient_image.shape[1] > left_box_screenshot.shape[1]:
        print(f"Изображение-шаблон {ingredient_image_path} слишком велико для сопоставления.")
        return
    left_box_gray = cv2.cvtColor(left_box_screenshot, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(left_box_gray, ingredient_image, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val > 0.5:
        click_x = left_box[0] + max_loc[0] + ingredient_image.shape[1] // 2
        click_y = left_box[1] + max_loc[1] + ingredient_image.shape[0] // 2
        pyautogui.click(click_x, click_y)
def parse_and_find_ingredients(ocr_text, ingredient_files):
    lines = ocr_text.strip().split('\n')
    ingredients = []
    for line in lines:
        cleaned_line = line.replace('3.', 'З.').lstrip('0123456789. ')
        ingredient_name = cleaned_line.split('. ', 1)[-1] if '. ' in cleaned_line else cleaned_line
        if ingredient_name and not ingredient_name.startswith(':') and not ingredient_name.startswith('00'):
            file_name = ingredient_files.get(ingredient_name, "Файл не найден")
            ingredients.append((ingredient_name, file_name))
    return ingredients
while True:  # Начало бесконечного цикла
    # Получаем текст заказа с правой части экрана
    order_text = capture_and_ocr(right_box)
    # Обрабатываем текст и находим соответствующие изображения ингредиентов
    found_ingredient_images = parse_and_find_ingredients(order_text, ingredient_files)
    # Захватываем скриншот левой области
    left_box_screenshot = capture_left_box(left_box)
    # Ищем и кликаем по каждому ингредиенту на левой стороне экрана
    for ingredient, image_file in found_ingredient_images:
        if image_file != "Файл не найден":
            ingredient_image_path = f"ingredients/{image_file}"  # Путь к изображениям
            find_and_click_ingredient(ingredient_image_path, left_box_screenshot)
            time.sleep(1)
    # Выводим распознанный текст заказа в консоль
    print(order_text)
    time.sleep(5)
    pyautogui.click(x=1123, y=874)
    x, y = 969, 175
    expected_color = (241, 206, 64)
    actual_color = pyautogui.pixel(x, y)
    if actual_color != expected_color:
       print("Цвет на указанных координатах не соответствует ожидаемому. Завершение работы.")
       exit()