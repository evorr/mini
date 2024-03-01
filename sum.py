import get
import read
import easygui

choice = easygui.buttonbox(choices=(["Scan folder", "Read bd"]))  # возвращает текст кнопки
if choice == "Scan folder":
    get.start()
