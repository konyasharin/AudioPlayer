import shutil  # работа с копированием файлов
import threading
import tkinter as tk
import pygame
from PIL import Image, ImageTk  # Изменение размеров картинок
from tkinter import filedialog
from Composition import Composition
from PlayList import PlayList
from LinkedListItem import LinkedListItem
import os
from threading import Thread  # Для использования потоков(для работы GUI и программы нужны отдельные потоки)
import json
from tkinter import simpledialog


def play_music():
    buttons[1] = create_btn_with_image("images/pause.png", 75, 0, 1, "pause", pause_music)
    global thread_flag
    thread_flag = True
    pygame.mixer.music.load(playlist.current_track.track.path)
    pygame.mixer.music.play()
    while (pygame.mixer.music.get_busy() or is_pause) and thread_flag:
        pygame.time.Clock().tick(5)
    if thread_flag:  # Если это происходит на втором потоке, который и так работает отдельно от GUI
        next_highlight()
        if len(playlist) > 1:
            playlist.current_track = playlist.current_track.next
        play_music()


def stop():
    pygame.mixer.music.unload()
    reload_thread()
    buttons[1] = create_btn_with_image("images/play.png", 75, 0, 1, "play",
                                       lambda: play_with_threading.start())


def play_on_click():
    if list_box.size() == 0:
        print("Плейлист пустой!")
        return
    for item in playlist:
        if item.track.path == os.path.join(current_dir, "music", list_box.get(list_box.curselection())):
            playlist.current_track = item
    reload_thread()
    play_with_threading.start()


def next_highlight():
    for curselection in list_box.curselection():
        if playlist.current_track.track.path == os.path.join(current_dir, "music", list_box.get(curselection)):
            list_box.selection_clear(0, tk.END)
            if curselection + 1 >= len(playlist):
                list_box.select_set(0)
            else:
                list_box.select_set(curselection + 1)


def prev_highlight():
    for curselection in list_box.curselection():
        if playlist.current_track.track.path == os.path.join(current_dir, "music", list_box.get(curselection)):
            list_box.selection_clear(0, tk.END)
            if curselection - 1 < 0:
                list_box.select_set(len(playlist) - 1)
            else:
                list_box.select_set(curselection - 1)


def next_music():
    next_highlight()
    if len(playlist) > 1:
        playlist.current_track = playlist.current_track.next
    reload_thread()
    play_with_threading.start()


def prev_music():
    prev_highlight()
    if len(playlist) > 1:
        playlist.current_track = playlist.current_track.prev
    reload_thread()
    play_with_threading.start()


def create_btn_with_image(path, size, row, column, name, func):
    img = Image.open(path)
    resized = img.resize((size, size))
    new_img = ImageTk.PhotoImage(resized)
    images[name] = new_img
    btn = tk.Button(frame, image=images[name], borderwidth=0, command=func)
    btn.grid(row=row, column=column, padx=8)
    return btn


def pause_music():
    global is_pause
    is_pause = True
    pygame.mixer.music.pause()
    buttons[1] = create_btn_with_image("images/play.png", 75, 0, 1, "play", unpause_music)


def unpause_music():
    global is_pause
    is_pause = False
    pygame.mixer.music.unpause()
    buttons[1] = create_btn_with_image("images/pause.png", 75, 0, 1, "pause", pause_music)


def reload_thread():
    global thread_flag
    global play_with_threading
    print(threading.active_count())  # выводим в консоль количество потоков
    if threading.active_count() == 2:
        thread_flag = False
        play_with_threading.join()
        play_with_threading = Thread(target=play_music, daemon=True)


def add_music():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    if file_path:
        output_path = os.path.join(current_dir, "music", os.path.basename(file_path))
        try:
            if not os.path.exists(output_path):
                shutil.copy(file_path, output_path)
            if not os.path.basename(file_path) in current_playlist["songs"]:
                playlist.append(LinkedListItem(Composition(output_path)))
                current_playlist["songs"].append(os.path.basename(file_path))
                rewrite_json()
                rewrite_listbox()
                rewrite_playlist()
                stop()
                if len(playlist) >= 1:
                    lock_play_buttons("normal")
            else:
                print("Данная песня уже есть в плейлисте")
        except Exception as e:
            print("Произошла ошибка при добавлении музыки")
            print(e)


def delete_music():
    stop()
    lock_play_buttons("disabled")
    menu.entryconfig("Меню", state="disabled")
    list_box.delete(0, tk.END)
    for j in range(0, len(playlist)):
        list_box.insert(tk.END, current_playlist["songs"][j])
    if list_box.size() > 0:
        list_box.bind("<<ListboxSelect>>", lambda e: delete_on_click())
    else:
        menu.entryconfig("Меню", state="normal")
        list_box.bind("<<ListboxSelect>>", lambda event: play_on_click())


def delete_on_click():
    file_path = list_box.get(list_box.curselection())
    output_path = os.path.join(current_dir, "music", file_path)
    try:
        playlist.remove(LinkedListItem(Composition(output_path)))
        current_playlist["songs"].remove(file_path)
        rewrite_json()
        rewrite_listbox()
        rewrite_playlist()
        list_box.bind("<<ListboxSelect>>", lambda event: play_on_click())
        if len(playlist) >= 1:
            lock_play_buttons("normal")
        menu.entryconfig("Меню", state="normal")
        flag = False
        for j in range(0, len(playlists)):  # Удаление песни из папки если она не используется в плейлистах
            if file_path in playlists[j]["songs"]:
                flag = True
                break
        if not flag:
            os.remove(output_path)
    except Exception as e:
        print(e)
        print("Произошла ошибка при удалении музыки")


def lock_play_buttons(state):
    for btn in buttons:
        btn.config(state=state)


def rewrite_json():
    with open(os.path.join(current_dir, "music", "playLists.json"), "w") as json_file:
        data = {"playlists": playlists, "current_playlist": current_playlist_name}
        json.dump(data, json_file, indent=4)


def create_playlist():
    playlist_name = simpledialog.askstring("Введите данные", "Введите название для нового плейлиста")
    if playlist_name:
        playlists.append({"name": playlist_name, "songs": []})
        rewrite_json()


def choose_playlist():
    stop()
    lock_play_buttons("disabled")
    menu.entryconfig("Меню", state="disabled")
    list_box.delete(0, tk.END)
    for j in range(0, len(playlists)):
        list_box.insert(tk.END, playlists[j]["name"])
    list_box.bind("<<ListboxSelect>>", lambda e: on_select_playlist())


def on_select_playlist():
    global current_playlist_name
    global current_playlist
    current_playlist_name = list_box.get(list_box.curselection())
    for j in range(0, len(playlists)):
        if playlists[j]["name"] == current_playlist_name:
            current_playlist = playlists[j]
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
    if len(playlists) > 1:
        playlists.remove(current_playlist)
        rewrite_json()
        choose_playlist()
    else:
        print("Вы не можете удалить все плейлисты, сначала создайте другой плейлист, а потом можете удалить этот")


def instruction_edit_order():
    exit_command()
    list_box.bind("<<ListboxSelect>>", lambda e: edit_order_music())
    tk.Label(frame1, text="Выберите элемент").grid(row=0, column=0, padx=95)


def edit_order_music():
    for widget in frame1.winfo_children():
        if isinstance(widget, tk.Label):
            widget.destroy()
            break
    if list_box.size() > 0:
        tk.Button(frame1, text="Опустить вниз", command=music_down).grid(row=2, column=0, padx=35)
        tk.Button(frame1, text="Прекратить изменение пордка песен", command=exit_command).grid(row=1, column=0, padx=35)
        tk.Button(frame1, text="Поднять вверх", command=music_up).grid(row=0, column=0, padx=35)
        stop()
        lock_play_buttons("disabled")
        list_box.bind("<<ListboxSelect>>", lambda e: edit_order_music())
    else:
        list_box.bind("<<ListboxSelect>>", lambda e: play_on_click())


def exit_command():
    for widget in frame1.winfo_children():
        widget.destroy()
    lock_play_buttons("normal")
    list_box.bind("<<ListboxSelect>>", lambda e: play_on_click())


def music_up():
    chased_elem = os.path.join(current_dir, "music", list_box.get(list_box.curselection()))
    if playlist[0].track.path != chased_elem and playlist[1].track.path != chased_elem:
        for j in range(0, len(playlist)):
            if playlist[j].track.path == chased_elem:
                playlist.remove(LinkedListItem(Composition(chased_elem)))
                playlist.insert(j - 2, LinkedListItem(Composition(chased_elem)))
                current_playlist["songs"].remove(os.path.basename(chased_elem))
                current_playlist["songs"].insert(j - 1, os.path.basename(chased_elem))
                rewrite_json()
                rewrite_listbox()
                rewrite_playlist()
                list_box.selection_clear(0, tk.END)
                list_box.select_set(j - 1)
                break
    elif playlist[1] == LinkedListItem(Composition(chased_elem)):  # Нельзя сделать insert после -1 элемента
        playlist.remove(LinkedListItem(Composition(chased_elem)))
        playlist.append_left(LinkedListItem(Composition(chased_elem)))
        current_playlist["songs"].remove(os.path.basename(chased_elem))
        current_playlist["songs"].insert(0, os.path.basename(chased_elem))
        rewrite_json()
        rewrite_listbox()
        list_box.selection_clear(0, tk.END)
        list_box.select_set(0)
    else:
        print("Данный трек находится на самом верху, вы его не можете поднять больше!")


def music_down():
    chased_elem = os.path.join(current_dir, "music", list_box.get(list_box.curselection()))
    if playlist[len(playlist) - 1].track.path != chased_elem:
        for j in range(0, len(playlist)):
            if playlist[j].track.path == chased_elem:
                playlist.remove(LinkedListItem(Composition(chased_elem)))
                playlist.insert(j, LinkedListItem(Composition(chased_elem)))
                current_playlist["songs"].remove(os.path.basename(chased_elem))
                current_playlist["songs"].insert(j + 1, os.path.basename(chased_elem))
                rewrite_json()
                rewrite_listbox()
                list_box.selection_clear(0, tk.END)
                list_box.select_set(j + 1)
                break
    else:
        print("Данный трек находится в самом низу, вы его не можете опустить больше!")


def rewrite_listbox():
    list_box.delete(0, tk.END)
    for j in range(0, len(current_playlist["songs"])):
        list_box.insert(tk.END, current_playlist["songs"][j])


def rewrite_playlist():
    global playlist
    playlist = PlayList()
    for music in current_playlist["songs"]:
        playlist.append(LinkedListItem(Composition(os.path.join(current_dir, "music", music))))
    if len(playlist) != 0:
        playlist.current_track = playlist[0]
    list_box.select_set(0)


if __name__ == "__main__":
    images = {}  # Сборщик мусора без хранения картинок их удалял
    thread_flag = False  # Флаг для завершения работы потокаов
    pygame.mixer.init()
    is_pause = False
    play_with_threading = Thread(target=play_music, daemon=True)
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
    buttons.append(create_btn_with_image("images/back.png", 75, 0, 0, "back", prev_music))
    buttons.append(create_btn_with_image("images/play.png", 75, 0, 1, "play",
                                         lambda: play_with_threading.start()))
    buttons.append(create_btn_with_image("images/next.png", 75, 0, 2, "next", next_music))

    menu = tk.Menu(root)
    root.config(menu=menu)
    open_menu = tk.Menu(menu)
    menu.add_cascade(label="Меню", menu=open_menu)
    open_menu.add_command(label="Добавить песню", command=add_music)
    open_menu.add_command(label="Удалить песню", command=delete_music)
    open_menu.add_command(label="Создать плейлист", command=create_playlist)
    open_menu.add_command(label="Удалить данный плейлист", command=delete_playlist)
    open_menu.add_command(label="Выбрать другой плейлист", command=choose_playlist)
    open_menu.add_command(label="Изменить порядок песен",
                          command=lambda: instruction_edit_order())

    list_box = tk.Listbox(root, width=47, height=10, selectbackground="gray", selectforeground="white",
                          selectmode=tk.SINGLE)
    list_box.pack()

    # Получение текущей директории
    current_dir = os.getcwd()

    with open(os.path.join(current_dir, "music", "playLists.json"), "r") as json_file:
        dictionary = json.load(json_file)
        current_playlist_name = dictionary["current_playlist"]
        playlists = dictionary["playlists"]
        for i in range(0, len(playlists)):
            if playlists[i]["name"] == current_playlist_name:
                current_playlist = playlists[i]  # текущий плейлист из JSON
                break
    rewrite_listbox()
    rewrite_playlist()
    list_box.bind("<<ListboxSelect>>", lambda event: play_on_click())
    if len(playlist) < 1:
        lock_play_buttons("disabled")

    root.mainloop()
