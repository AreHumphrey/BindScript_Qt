import pyautogui
import time

# Начальное нажатие и удерживание левой кнопки мыши
time.sleep(5)
initial_click_position = (644, 469)
pyautogui.moveTo(initial_click_position)
pyautogui.mouseDown()

# Функция для перемещения мыши с уже зажатой левой кнопкой (удалим mouseDown и mouseUp)
def move_mouse_drag(start_pos, end_pos):
    pyautogui.moveTo(start_pos)
    pyautogui.mouseDown()  # Зажимаем левую кнопку мыши
    pyautogui.moveTo(end_pos, duration=0.13)  # Перемещаем курсор мыши

# Начальные координаты для основной части скрипта
start_x = 600
start_y = 289
end_x = 1301
end_y = 289

# Конечные координаты
final_x_start = 600
final_y_start = 787
final_x_end = 1301
final_y_end = 787

# Количество повторений для каждого шага
repeats = 2

# Цикл для генерации и выполнения движений мыши
while start_y < final_y_start:
    for _ in range(repeats):
        move_mouse_drag((start_x, start_y), (end_x, end_y))
    start_y += 10
    end_y += 10

for _ in range(repeats):
    move_mouse_drag((final_x_end, final_y_end), (final_x_start, final_y_start))

