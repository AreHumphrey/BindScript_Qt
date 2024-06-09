import pyautogui
import time

time.sleep(5)

start_position = (621, 657)
end_position = (717, 551)

pyautogui.mouseDown(button='left', x=start_position[0], y=start_position[1])

pyautogui.moveTo(end_position[0], start_position[1])

pyautogui.moveTo(end_position[0], end_position[1])
pyautogui.mouseUp()

pyautogui.mouseDown(button='left', x=end_position[0], y=end_position[1])


start_x = 670
start_y = 240
end_x = 1240
end_y = 240

final_x_start = 670
final_y_start = 720
final_x_end = 1240
final_y_end = 720

repeats = 2

def move_mouse_drag(start_pos, end_pos):
    pyautogui.moveTo(start_pos)
    pyautogui.mouseDown()
    pyautogui.moveTo(end_pos, duration=0.1)


while start_y < final_y_start:
    for _ in range(repeats):
        move_mouse_drag((start_x, start_y), (end_x, end_y))
    start_y += 9
    end_y += 9


for _ in range(repeats):
    move_mouse_drag((final_x_end, final_y_end), (final_x_start, final_y_start))
