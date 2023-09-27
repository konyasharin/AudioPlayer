"""
Малышев Николай КИ22-17/2Б

В данном модуле созданы все методы для работы с аудиоплеером.

Также здесь создан GUI самого плеера и есть методы
для работы с JSON-файлом, который сохраняет в себе все
плейлисты после выхода из программы, а также он хранит в
себе название последнего плейлиста, который был запущен

Ещё здесь реализована работа с потоками через threading,
что необходимо для правильной работы музыки и GUI.
"""
import os
import json
import shutil  # работа с копированием файлов
import threading
from threading import Thread  # Для использования потоков
# (для работы GUI и программы нужны отдельные потоки)
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import pygame
from PIL import Image, ImageTk  # Изменение размеров картинок
from Composition import Composition
from PlayList import PlayList
from LinkedListItem import LinkedListItem


def play_music():
    """
    Данный метод проигрывает текущую композицию на отдельном потоке,
    дожидаясь либо переключения трека пользователем либо конца композиции,
    после чего будет играть следующая композиция
    """
    buttons[1] = create_btn_with_image("images/pause.png",
                                       75, 0, 1, "pause", pause_music)
    global_variables["thread_flag"] = True
    pygame.mixer.music.load(playlist.current_track.track.path)
    pygame.mixer.music.play()
    while ((pygame.mixer.music.get_busy() or global_variables["is_pause"])
           and global_variables["thread_flag"]):
        pygame.time.Clock().tick(5)
    if global_variables["thread_flag"]:
        # Если это происходит на втором потоке,
        # который и так работает отдельно от GUI
        next_highlight()
        if len(playlist) > 1:
            playlist.current_track = playlist.current_track.next
        play_music()


def stop():
    """
    Данный метод полностью останавливает музыку(не пауза)
    """
    pygame.mixer.music.unload()
    reload_thread()
    buttons[1] = (
        create_btn_with_image("images/play.png", 75, 0, 1, "play",
                              lambda:
                              global_variables["play_with_threading"].start()
                              )
    )


def play_on_click():
    """
    Данный метод запускает композицию, на которую нажал пользователь
    """
    if list_box.size() == 0:
        print("Плейлист пустой!")
        return
    for item in playlist:
        if (item.track.path ==
                os.path.join(current_dir,
                             "music", list_box.get(list_box.curselection()))):
            playlist.current_track = item
    reload_thread()
    global_variables["play_with_threading"].start()


def next_highlight():
    """
    Данный метод перемещает выделение на следующую композицию
    """
    for curselection in list_box.curselection():
        if (playlist.current_track.track.path ==
                os.path.join(current_dir,
                             "music", list_box.get(curselection))):
            list_box.selection_clear(0, tk.END)
            if curselection + 1 >= len(playlist):
                list_box.select_set(0)
            else:
                list_box.select_set(curselection + 1)


def prev_highlight():
    """
    Данный метод перемещает выделение на предыдущую композицию
    """
    for curselection in list_box.curselection():
        if (playlist.current_track.track.path ==
                os.path.join(current_dir,
                             "music", list_box.get(curselection))):
            list_box.selection_clear(0, tk.END)
            if curselection - 1 < 0:
                list_box.select_set(len(playlist) - 1)
            else:
                list_box.select_set(curselection - 1)


def next_music():
    """
    Данный метод переключает музыку на следующую композицию
    после того, как пользователь нажа на кнопку 'далее'
    """
    next_highlight()
    if len(playlist) > 1:
        playlist.current_track = playlist.current_track.next
    reload_thread()
    global_variables["play_with_threading"].start()


def prev_music():
    """
    Данный метод переключает музыку на предыдущую композицию
    после того, как пользователь нажа на кнопку 'назад'
    """
    prev_highlight()
    if len(playlist) > 1:
        playlist.current_track = playlist.current_track.prev
    reload_thread()
    global_variables["play_with_threading"].start()


def create_btn_with_image(path, size, row, column, name, func):
    """
    Данный метод создает кнопки вутри frame(белое окно в аудиоплеере)
    :param path: путь до картинки кнопки на ПК
    :param size: размер картинки
    :param row: строка в grid сетке
    :param column: колонка в grid сетке
    :param name: имя кнопки внутри словаря
    :param func: функция, которая вызывается по нажатию кнопки
    :return: кнопка в формате tkinter
    """
    img = Image.open(path)
    resized = img.resize((size, size))
    new_img = ImageTk.PhotoImage(resized)
    images[name] = new_img
    btn = tk.Button(frame, image=images[name], borderwidth=0, command=func)
    btn.grid(row=row, column=column, padx=8)
    return btn


def pause_music():
    """
    Данный метод ставит музыку на паузу
    """
    global_variables["is_pause"] = True
    pygame.mixer.music.pause()
    buttons[1] = create_btn_with_image("images/play.png",
                                       75, 0, 1, "play", unpause_music)


def unpause_music():
    """
    Данный метод возобновляет музыку с паузы
    """
    global_variables["is_pause"] = False
    pygame.mixer.music.unpause()
    buttons[1] = create_btn_with_image("images/pause.png",
                                       75, 0, 1, "pause", pause_music)


def reload_thread():
    """
    Данный метод перезапускает второй поток(на котором играет музыка)
    """
    # выводим в консоль количество потоков(их должно быть не больше двух)
    print(f"Число активных потоков в данный момент:"
          f" {threading.active_count()}")
    if threading.active_count() == 2:
        global_variables["thread_flag"] = False
        global_variables["play_with_threading"].join()
        global_variables["play_with_threading"] = (
            Thread(target=play_music, daemon=True))


def add_music():
    """
    Данный метод добавляет новую музыку в плейлист
    и перезаписывает JSON
    """
    file_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.mp3 *.wav")])
    if file_path:
        output_path = os.path.join(current_dir,
                                   "music", os.path.basename(file_path))
        if not os.path.exists(output_path):
            shutil.copy(file_path, output_path)
        if not (os.path.basename(file_path) in
                global_variables["current_playlist"]["songs"]):
            playlist.append(LinkedListItem(Composition(output_path)))
            (global_variables["current_playlist"]["songs"].
             append(os.path.basename(file_path)))
            rewrite_json()
            rewrite_listbox()
            rewrite_playlist()
            stop()
            if len(playlist) >= 1:
                lock_play_buttons("normal")
        else:
            print("Данная песня уже есть в плейлисте")


def delete_music():
    """
    Данный метод привязывает удаление музыки к нажатию по музыке
    """
    stop()
    lock_play_buttons("disabled")
    menu.entryconfig("Меню", state="disabled")
    list_box.delete(0, tk.END)
    for j in range(0, len(playlist)):
        list_box.insert(tk.END,
                        global_variables["current_playlist"]["songs"][j])
    if list_box.size() > 0:
        list_box.bind("<<ListboxSelect>>", lambda e: delete_on_click())
    else:
        menu.entryconfig("Меню", state="normal")
        list_box.bind("<<ListboxSelect>>", lambda event: play_on_click())


def delete_on_click():
    """
    Данный метод удаляет песню по клику на нее
    """
    file_path = list_box.get(list_box.curselection())
    output_path = os.path.join(current_dir, "music", file_path)
    playlist.remove(LinkedListItem(Composition(output_path)))
    global_variables["current_playlist"]["songs"].remove(file_path)
    rewrite_json()
    rewrite_listbox()
    rewrite_playlist()
    list_box.bind("<<ListboxSelect>>", lambda event: play_on_click())
    if len(playlist) >= 1:
        lock_play_buttons("normal")
    menu.entryconfig("Меню", state="normal")
    flag = False
    # Удаление песни из папки если она не используется в плейлистах
    for check_playlist in playlists:
        if file_path in check_playlist["songs"]:
            flag = True
            break
    if not flag:
        os.remove(output_path)


def lock_play_buttons(state):
    """
    Данный метод блокирует или разблокировывает кнопки для нажатий
    :param state: состояние кнопки - отключена или включена
    """
    for btn in buttons:
        btn.config(state=state)


def rewrite_json():
    """
    Данный метод переписывает JSON файл
    """
    with open(os.path.join(current_dir, "music", "playLists.json"),
              "w", encoding="utf-8") as file:
        data = {"playlists": playlists,
                "current_playlist": global_variables["current_playlist_name"]}
        json.dump(data, file, indent=4)


def create_playlist():
    """
    Данный метод создает новый плейлист
    """
    playlist_name = simpledialog.askstring(
        "Введите данные", "Введите название для нового плейлиста")
    if playlist_name:
        playlists.append({"name": playlist_name, "songs": []})
        rewrite_json()


def choose_playlist():
    """
    Данный метод выводит список плейлистов и привязывает нажатие по одному
    из плейлистов к открытию этого плейлиста
    """
    stop()
    lock_play_buttons("disabled")
    menu.entryconfig("Меню", state="disabled")
    list_box.delete(0, tk.END)
    for check_playlist in playlists:
        list_box.insert(tk.END, check_playlist["name"])
    list_box.bind("<<ListboxSelect>>", lambda e: on_select_playlist())


def on_select_playlist():
    """
    Данный метод открывает плейлист по которому было произведено нажатие
    """
    global_variables["current_playlist_name"] = \
        list_box.get(list_box.curselection())
    for check_playlist in playlists:
        if check_playlist["name"] == global_variables["current_playlist_name"]:
            global_variables["current_playlist"] = check_playlist
            break
    rewrite_json()
    rewrite_listbox()
    rewrite_playlist()
    list_box.bind("<<ListboxSelect>>", lambda e: play_on_click())
    menu.entryconfig("Меню", state="normal")
    if len(playlist) < 1:
        lock_play_buttons("disabled")
    else:
        lock_play_buttons("normal")


def delete_playlist():
    """
    Данный метод удаляет текущий плейлист
    """
    if len(playlists) > 1:
        playlists.remove(global_variables["current_playlist"])
        rewrite_json()
        choose_playlist()
    else:
        print("Вы не можете удалить все плейлисты,"
              " сначала создайте другой плейлист,"
              " а потом можете удалить этот")


def instruction_edit_order():
    """
    Данный метод выводит надпись с инструкцией и привязывает метод
    edit_order_music к нажатию по треку
    """
    exit_command()
    stop()
    lock_play_buttons("disabled")
    list_box.bind("<<ListboxSelect>>", lambda e: edit_order_music())
    tk.Label(frame1, text="Выберите элемент").grid(row=0, column=0, padx=95)


def edit_order_music():
    """
    Данный метод убирает инструкцию и показывает кнопки для перемещения
    треков вверх и вниз, а также кнопку для прекращения перемещения
    """
    for widget in frame1.winfo_children():
        if isinstance(widget, tk.Label):
            widget.destroy()
            break
    if list_box.size() > 0:
        tk.Button(frame1, text="Опустить вниз",
                  command=music_down).grid(row=2, column=0, padx=35)
        tk.Button(frame1, text="Прекратить изменение пордка песен",
                  command=exit_command).grid(row=1, column=0, padx=35)
        tk.Button(frame1, text="Поднять вверх",
                  command=music_up).grid(row=0, column=0, padx=35)
        list_box.bind("<<ListboxSelect>>", lambda e: edit_order_music())
    else:
        list_box.bind("<<ListboxSelect>>", lambda e: play_on_click())


def exit_command():
    """
    Данный метод выходит из команд(разблокировка кнопок)
    """
    for widget in frame1.winfo_children():
        widget.destroy()
    lock_play_buttons("normal")
    list_box.selection_clear(0, tk.END)
    list_box.select_set(0)
    list_box.bind("<<ListboxSelect>>", lambda e: play_on_click())


def music_up():
    """
    Данный метод поднимает музыку наверх в списке
    """
    chased_elem = os.path.join(current_dir,
                               "music", list_box.get(list_box.curselection()))
    if (playlist[0].track.path != chased_elem
            and playlist[1].track.path != chased_elem):
        for j, check_track in enumerate(playlist):
            if check_track.track.path == chased_elem:
                playlist.remove(LinkedListItem(Composition(chased_elem)))
                playlist.insert(j - 2,
                                LinkedListItem(Composition(chased_elem)))
                (global_variables["current_playlist"]["songs"].
                 remove(os.path.basename(chased_elem)))
                (global_variables["current_playlist"]["songs"].
                 insert(j - 1, os.path.basename(chased_elem)))
                rewrite_json()
                rewrite_listbox()
                playlist.current_track = playlist[0]
                list_box.selection_clear(0, tk.END)
                list_box.select_set(j - 1)
                break
    # Нельзя сделать insert после -1 элемента
    elif playlist[1] == LinkedListItem(Composition(chased_elem)):
        playlist.remove(LinkedListItem(Composition(chased_elem)))
        playlist.append_left(LinkedListItem(Composition(chased_elem)))
        (global_variables["current_playlist"]["songs"].
         remove(os.path.basename(chased_elem)))
        (global_variables["current_playlist"]["songs"].
         insert(0, os.path.basename(chased_elem)))
        list_box.selection_clear(0, tk.END)
        list_box.select_set(0)
    else:
        print("Данный трек находится на самом верху, "
              "вы его не можете поднять больше!")


def music_down():
    """
    Данный метод опускает музыку вниз в списке
    """
    chased_elem = os.path.join(current_dir,
                               "music", list_box.get(list_box.curselection()))
    if playlist[len(playlist) - 1].track.path != chased_elem:
        for j, check_track in enumerate(playlist):
            if check_track.track.path == chased_elem:
                playlist.remove(LinkedListItem(Composition(chased_elem)))
                playlist.insert(j, LinkedListItem(Composition(chased_elem)))
                (global_variables["current_playlist"]["songs"].
                 remove(os.path.basename(chased_elem)))
                (global_variables["current_playlist"]["songs"].
                 insert(j + 1, os.path.basename(chased_elem)))
                rewrite_json()
                rewrite_listbox()
                playlist.current_track = playlist[0]
                list_box.selection_clear(0, tk.END)
                list_box.select_set(j + 1)
                break
    else:
        print("Данный трек находится в самом низу, "
              "вы его не можете опустить больше!")


def rewrite_listbox():
    """
    Данный метод перезаписывает песни в списке в аудиоплеере
    """
    list_box.delete(0, tk.END)
    for j in range(0, len(global_variables["current_playlist"]["songs"])):
        list_box.insert(tk.END,
                        global_variables["current_playlist"]["songs"][j])


def rewrite_playlist():
    """
    Данный метод перезаписывает текущий плейлист
    + изменение текущего трека на нулевой
    """
    global playlist
    playlist = PlayList()
    for music in global_variables["current_playlist"]["songs"]:
        playlist.append(LinkedListItem(
            Composition(os.path.join(current_dir, "music", music))))
    if len(playlist) != 0:
        playlist.current_track = playlist[0]
    list_box.select_set(0)


if __name__ == "__main__":
    images = {}  # Сборщик мусора без хранения картинок их удалял
    global_variables = {"thread_flag": False, "is_pause": False,
                        "play_with_threading":
                            Thread(target=play_music, daemon=True),
                        "current_playlist": {"name": "", "songs": []},
                        "current_playlist_name": ""}
    pygame.mixer.init()
    playlist = PlayList()
    buttons = []

    # Создание главного окна
    root = tk.Tk()
    root['bg'] = '#000000'
    root.geometry('350x400')
    root.title("Аудиолеер")
    root.resizable(width=False, height=False)

    frame = tk.Frame(root)
    frame.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.2)
    frame1 = tk.Frame(root, bg="black")
    frame1.place(relx=0.1, rely=0.45, relwidth=0.8, relheight=0.2)

    # Создание кнопок
    buttons.append(create_btn_with_image("images/back.png",
                                         75, 0, 0, "back", prev_music))
    buttons.append(
        create_btn_with_image(
            "images/play.png", 75, 0, 1, "play",
            lambda: global_variables["play_with_threading"].start()
        )
    )
    buttons.append(create_btn_with_image("images/next.png",
                                         75, 0, 2, "next", next_music))

    menu = tk.Menu(root)
    root.config(menu=menu)
    open_menu = tk.Menu(menu)
    menu.add_cascade(label="Меню", menu=open_menu)
    open_menu.add_command(label="Добавить песню",
                          command=add_music)
    open_menu.add_command(label="Удалить песню",
                          command=delete_music)
    open_menu.add_command(label="Создать плейлист",
                          command=create_playlist)
    open_menu.add_command(label="Удалить данный плейлист",
                          command=delete_playlist)
    open_menu.add_command(label="Выбрать другой плейлист",
                          command=choose_playlist)
    open_menu.add_command(label="Изменить порядок песен",
                          command=lambda: instruction_edit_order())

    list_box = tk.Listbox(root, width=47, height=10,
                          selectbackground="gray", selectforeground="white",
                          selectmode=tk.SINGLE)
    list_box.pack()

    # Получение текущей директории
    current_dir = os.getcwd()

    with open(os.path.join(current_dir, "music", "playLists.json"),
              "r", encoding="utf-8") as json_file:
        dictionary = json.load(json_file)
        global_variables[("current_playlist"
                          "_name")] = dictionary["current_playlist"]
        playlists = dictionary["playlists"]
        for playlist_check in playlists:
            if playlist_check["name"] == global_variables[("current_playlist"
                                                           "_name")]:
                global_variables["current_playlist"] = playlist_check
                break
    rewrite_listbox()
    rewrite_playlist()
    list_box.bind("<<ListboxSelect>>", lambda event: play_on_click())
    if len(playlist) < 1:
        lock_play_buttons("disabled")

    root.mainloop()
