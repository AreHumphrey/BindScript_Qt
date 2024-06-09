import pyautogui
import time
import numpy as np

# Задержка перед началом работы скрипта
time.sleep(2)

# Координаты области видимости, где ожидается наличие элементов
x1, y1, x2, y2 = 362, 486, 1558, 789

# Координаты мусорок
trash_bins = [(1507, 849), (1319, 849), (1125, 849), (940, 849), (745, 849), (554, 849), (363, 849)]

def find_element(area):
    """Поиск элемента, отличающегося по цвету."""
    screenshot = pyautogui.screenshot(region=(area[0], area[1], area[2] - area[0], area[3] - area[1]))
    for x in range(0, screenshot.width, 10):
        for y in range(0, screenshot.height, 10):
            if screenshot.getpixel((x, y)) != (234, 234, 234):
                return x + area[0], y + area[1]
    return None

def images_are_different(image1, image2):
    """Сравнение двух изображений."""
    image1_array = np.array(image1)
    image2_array = np.array(image2)
    return not np.array_equal(image1_array, image2_array)

def screenshot_equals(bin_position):
    """Проверка идентичности скриншотов до и после отпускания кнопки мыши."""
    pyautogui.moveTo(*bin_position)
    before_drop_screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    pyautogui.mouseUp()
    after_drop_screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    return images_are_different(before_drop_screenshot, after_drop_screenshot)

def check_color_match(x, y, expected_color):
    """Проверка цвета пикселя на соответствие ожидаемому."""
    return pyautogui.screenshot().getpixel((x, y)) == expected_color

def try_to_grab_and_drag(initial_position, move_attempts):
    for dx, dy in move_attempts:
        current_position = (initial_position[0] + dx, initial_position[1] + dy)
        pyautogui.moveTo(*current_position)
        pyautogui.mouseDown()
        pyautogui.moveRel(10, 0)
        before_grab_screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
        pyautogui.moveRel(90, 50)
        after_grab_screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

        if images_are_different(before_grab_screenshot, after_grab_screenshot):
            for bin_position in trash_bins:
                if screenshot_equals(bin_position):
                    print(f"Элемент не переместился в мусорку {bin_position}. Перемещаем в следующую.")
                    pyautogui.mouseDown()
                else:
                    print(f"Элемент переместился в мусорку {bin_position}. Поиск нового элемента.")
                    return True
            print("Элемент перетащен ко всем мусоркам.")
            return True
        else:
            print("Не удалось схватить элемент, пытаемся снова.")
            pyautogui.mouseUp()

    print("Не удалось схватить элемент после всех попыток.")
    return False

while True:
    if not check_color_match(1082, 357, (139, 196, 68)):
        print("Указанный цвет на координатах (1082, 357) пропал. Завершение работы.")
        break

    element_position = find_element((x1, y1, x2, y2))
    if element_position is None:
        print("Элементы для перетаскивания закончились.")
        break

    move_attempts = [(0, 0), (30, 0), (0, 30), (0, -30), (30, 30), (30, -30)]
    if not try_to_grab_and_drag(element_position, move_attempts):
        break
