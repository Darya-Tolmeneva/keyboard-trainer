import sys
import sqlite3
import random
import csv
from PyQt5 import uic, QtMultimedia
from PyQt5.Qt import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Centre:
    def __init__(self):
        # подключение звука нажатия кнопок
        media = QUrl.fromLocalFile("media/zvuk.mp3")
        content = QtMultimedia.QMediaContent(media)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)
        # подключение базы данных
        self.con = sqlite3.connect("data/profils_db.sqlite")
        self.cur = self.con.cursor()

    def info(self):
        """Открытие окна с информацией по приложению"""
        self.player.play()
        self.i = Info()
        self.i.show()

    def exit_m(self):
        """Открытие главного окна"""
        self.player.play()
        self.m = Main()
        self.m.show()
        self.close()

    def exit(self):
        """Открытие окна профиля пользователя"""
        self.player.play()
        self.p = Profil(self, self.nick)
        self.p.show()
        self.close()


class Main(QMainWindow, Centre):
    def __init__(self):
        super().__init__()
        uic.loadUi('design/main_window.ui', self)
        self.k = 0  # счетчик количества ошибок ввода пароля
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('image/icon.png'))  # добавление иконки приложения
        self.lineEdit_2.setEchoMode(QLineEdit.Password)  # скрытие символа пароля значками
        # привязка нажатия кнопок к определенным функциям
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.signup)
        self.pushButton_3.clicked.connect(self.info)

    def signup(self):
        """Открытие окна регистрации"""
        self.player.play()
        self.sign = Signup()
        self.sign.show()
        self.close()

    def login(self):
        """Проверка на правильность ввода своих данных пользователем"""
        self.player.play()
        if self.lineEdit.text() == "" and self.lineEdit_2.text() == "":
            self.label_2.setText("Данные не введены")
        elif self.lineEdit.text() == "":
            self.label_2.setText("Не введен ник")
        else:
            # делаем повторно т.к. пользователь может ошибиться в вводе и будет ошибка
            self.con = sqlite3.connect("data/profils_db.sqlite")
            self.cur = self.con.cursor()
            result = self.cur.execute("SELECT * FROM profils WHERE nick = ?",
                                      (item_nick := self.lineEdit.text(),)).fetchall()
            if not result:  # проверка наличия введенного ника в базе данных
                self.label_2.setText("Неверный ник")
            else:
                for elem in result:
                    if elem[2] == self.lineEdit_2.text():
                        text = self.lineEdit.text()
                        test = False
                        training = False
                        learning = False
                        statis = False
                        self.load = Loading(self, test, training, text, learning, statis)
                        self.load.show()
                        self.close()
                    elif not self.lineEdit_2.text():  # проверка на то, что заполнено поле для пароля
                        self.label_2.setText("Кажется вы забыли пароль")
                    elif elem[2] != self.lineEdit_2.text():  # проверка соответствия пароля с указанным в базе
                        if self.k < 2:
                            self.label_2.setText("Введен неверный пароль")
                            self.k += 1
                        elif self.k == 2:
                            # если превышено количество попыток, пароль отправляется на указанную в профиле почту
                            # данные для авторизации
                            ad_from = "keyboardd.trainerrr@gmail.com"
                            ad_to = result[0][6]
                            password = "Klepa_Cat19!"
                            # создание наполнения письма
                            msg = MIMEMultipart()
                            msg['From'] = ad_from
                            msg['To'] = ad_to
                            msg['Subject'] = 'Восстановление доступа'
                            body = f"Ваш пароль от клавиатурного тренажера: {result[0][2]}"
                            msg.attach(MIMEText(body, 'plain'))
                            # подключение к серверу, авторизация, отправка письма
                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login(ad_from, password)
                            server.send_message(msg)
                            server.quit()
                            self.label_2.setText("Пароль отправлен на указанную почту!")
            self.con.close()


class Signup(QWidget, Centre):
    def __init__(self):
        super().__init__()
        uic.loadUi('design/signup.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('image/icon.png'))  # добавление иконки приложения
        self.lineEdit_2.setEchoMode(QLineEdit.Password)  # скрытие символа пароля значками
        # привязка нажатия кнопок к определенным функциям
        self.pushButton_5.clicked.connect(self.sign)
        self.pushButton_6.clicked.connect(self.exit_m)
        self.pushButton_4.clicked.connect(self.info)

    def sign(self):
        """Проверка на правильность ввода данных пользователем"""
        self.player.play()
        self.f = False
        alph = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
        if self.lineEdit.text() == "" and self.lineEdit_2.text() == "" and self.lineEdit_3.text() == "":
            self.label_2.setText("Данные не введены")
        elif self.lineEdit.text() == "" or self.lineEdit_2.text() == "" or self.lineEdit_3.text() == "":
            self.label_2.setText("Введены не все данные")
        else:
            result = self.cur.execute("SELECT * FROM profils WHERE nick = ?",
                                      (item_nick := self.lineEdit.text(),)).fetchall()
            if result:  # проверка на уникальность придуманного ника
                self.label_2.setText("Данный ник уже занят :(")
            elif ("@" not in self.lineEdit_3.text()) or ("." not in self.lineEdit_3.text()) or \
                    ("." == self.lineEdit_3.text()[-1]):  # проверка на то, что введена почта, а не что-то другое
                self.label_2.setText("Кажется вы некорректно ввели почту")
            elif (len(self.lineEdit_2.text()) < 8) or (self.lineEdit_2.text().isdigit()) or \
                    (self.lineEdit_2.text().isalpha()):  # проверка сложности придуманного пароля
                self.label_2.setText("Пароль недостаточно защищен")
            else:
                for i in self.lineEdit.text():
                    if i not in alph and i.isalpha():
                        self.f = True
                        break
                if self.f:  # проверка на то, что ник состоит из букв латинского алфавита
                    self.label_2.setText("Используйте латиницу при создании ника!")
                else:  # все подходит, вносим в базу и переключаем на следующее окно
                    self.cur.execute("INSERT INTO profils(nick, password, mail) VALUES(?, ?, ?)",
                                     (item_nick := self.lineEdit.text(),
                                      self.lineEdit_2.text(),
                                      self.lineEdit_3.text(),))
                    nick = self.lineEdit.text()
                    test = False
                    training = False
                    learning = False
                    statis = False
                    self.load = Loading(self, test, training, nick, learning, statis)
                    self.load.show()
                    self.close()
                    self.con.commit()


class Loading(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('design/loading.ui', self)
        # заводим переменные и передаем им значения из args
        self.test = args[1]
        self.training = args[2]
        self.t = args[3]
        self.learn = args[4]
        self.st = args[5]
        # создаем счетчик, он потребуется нам дальше
        self.timer = QTimer()
        self.second = 0
        # добавляем гифку
        self.gif = QMovie('image/cute-happy.gif')
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('image/icon.png'))  # добавление иконки приложения
        # запускаем гифку
        self.label_2.setScaledContents(True)
        self.label_2.setMovie(self.gif)
        self.gif.start()
        # запускаем таймер
        self.timer.timeout.connect(self.update)
        self.timer.start(500)

    def update(self):
        self.second += 1
        if self.second == 5:
            self.timer.stop()
            if not self.test and not self.training and not self.learn and not self.st:
                self.p = Profil(self, self.t)
                self.p.show()  # открываем окно профиля
                self.close()
            elif self.test:
                self.te = Test(self, self.t)
                self.te.show()  # открываем окно теста
                self.close()
            elif self.training and not self.learn:
                self.tra = Training(self, self.t)
                self.tra.show()  # открываем окно тренировок
                self.close()
            elif self.learn:
                self.le = Learning(self, self.t)
                self.le.show()  # открываем окно обучения
                self.close()
            elif self.st:
                self.stat = Statistics(self, self.t)
                self.stat.show()  # открываем окно статистики
                self.close()


class Statistics(QWidget, Centre):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('design/statistics.ui', self)
        self.nick = args[-1]
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('image/icon.png'))  # добавление иконки приложения
        # получаем точки для построения графика и строим график
        result = self.cur.execute("SELECT nick, all_progress FROM profils WHERE nick=?",
                                  (item_nick := self.nick,)).fetchall()
        tochk = result[0][1].split(", ")
        tochk = [int(i) for i in tochk[1:]]
        self.graphicsView.clear()
        self.graphicsView.plot([i for i in tochk], pen="w")
        if len(tochk) < 2:
            self.label_5.setText("Пока что недостаточно пройдено тестов, чтобы увидеть всю статистику")
            self.label_5.adjustSize()
        # привязка нажатия кнопок к определенным функциям
        self.pushButton_3.clicked.connect(self.exit)
        self.pushButton_4.clicked.connect(self.info)


class Learning(QWidget, Centre):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('design/learning.ui', self)
        self.nick = args[-1]
        # добавляем изображение
        self.pixmap2 = QPixmap("image/keyboard.jpg")

        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('image/icon.png'))  # добавление иконки приложения
        # настраиваем отображение подключенного изображения
        self.pixmap2 = self.pixmap2.scaled(900, 360, Qt.IgnoreAspectRatio)
        self.label_2.setGeometry(80, 270, 900, 360)
        self.label_2.setPixmap(self.pixmap2)
        # считываем текст для вывода на экран, выводим этот текст
        with open("data/learning.txt", encoding="utf-8") as f:
            data = f.readlines()
        mess = ""
        for i in data:
            mess += i
        self.textEdit.setText(mess)
        self.textEdit.setStyleSheet("border: 0; font: 75 10pt 'Trebuchet MS'; color: rgb(197, 198, 199)")
        # привязка нажатия кнопок к определенным функциям
        self.pushButton_4.clicked.connect(self.info)
        self.pushButton_5.clicked.connect(self.contin)

    def contin(self):
        self.player.play()
        test = False
        training = True
        learning = False
        stat = False
        self.load = Loading(self, test, training, self.nick, learning, stat)
        self.load.show()
        self.close()


class Profil(QWidget, Centre):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('design/profil.ui', self)
        self.nick = args[-1]
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('image/icon.png'))  # добавление иконки приложения
        # выводим на экран информацию о пользователе
        self.label.setText(self.nick)
        result = self.cur.execute("SELECT * FROM profils WHERE nick = ?",
                                  (item_nick := self.nick,)).fetchall()
        progg = self.cur.execute("SELECT id FROM progress").fetchall()
        self.label_2.setText((str(result[0][3])) + "/" + str(len(progg)))
        self.label_3.setText(str(result[0][5]))
        self.label_4.setText(str(result[0][4]))
        self.lineEdit.setText(str(result[0][6]))
        # настраиваем отображение подключенного изображения
        self.pixmap = QPixmap("image/avatar.jpg")
        self.pixmap = self.pixmap.scaled(300, 300, Qt.IgnoreAspectRatio)
        self.image = QLabel(self)
        self.image.setGeometry(30, 35, 220, 220)
        self.image.setPixmap(self.pixmap)
        # привязка нажатия кнопок к определенным функциям
        self.pushButton.clicked.connect(self.training)
        self.pushButton_2.clicked.connect(self.testing)
        self.pushButton_3.clicked.connect(self.exit_m)
        self.pushButton_4.clicked.connect(self.info)
        self.pushButton_5.clicked.connect(self.mail)
        self.pushButton_6.clicked.connect(self.statist)

    def statist(self):
        """Открытие статистики пользователя"""
        self.player.play()
        test = False
        training = False
        learn = False
        statis = True
        self.load = Loading(self, test, training, self.nick, learn, statis)
        self.load.show()
        self.close()

    def training(self):
        """Открытие окна тренировок"""
        self.player.play()
        test = False
        training = True
        statis = False
        result = self.cur.execute("SELECT * FROM profils WHERE nick = ?",
                                  (item_nick := self.nick,)).fetchall()
        idd = result[0][3]
        if idd == 0:  # если запуск первый, открываем обучающее окно
            learn = True
            self.load = Loading(self, test, training, self.nick, learn, statis)
        else:
            learn = False
            self.load = Loading(self, test, training, self.nick, learn, statis)
        self.load.show()
        self.close()

    def testing(self):
        """Открытие окна тестирования"""
        self.player.play()
        test = True
        training = False
        learn = False
        statis = False
        self.load = Loading(self, test, training, self.nick, learn, statis)
        self.load.show()
        self.close()

    def mail(self):
        """Проверка почты"""
        self.player.play()
        if "@" not in self.lineEdit.text() or "." not in self.lineEdit.text() or "." == self.lineEdit.text()[-1]:
            self.label_9.setText("Кажется вы некорректно ввели почту")
        else:
            upd = "UPDATE profils SET mail = ? WHERE nick = ?"
            data = (self.lineEdit.text(), self.nick)
            self.cur.execute(upd, data)
            self.con.commit()
            self.label_9.setText("Успешно сохранено!")
            self.label_9.setStyleSheet("QLabel#label_9 { color : green}")


class Info(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('design/info.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('image/icon.png'))  # добавление иконки приложения
        # считываем текст для вывода на экран, выводим этот текст
        with open("data/info.txt", encoding="utf-8") as f:
            data = f.readlines()
        mess = ""
        for i in data:
            mess += i
        self.plainTextEdit.setPlainText(mess)


class Test(QWidget, Centre):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('design/test.ui', self)
        self.nick = args[-1]
        # добавляем изображение
        self.pixmap2 = QPixmap("image/keyboard.jpg")
        # создаем счетчик, он потребуется нам дальше
        self.timer = QTimer()

        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('image/icon.png'))  # добавление иконки приложения
        # считываем таблицу и рандомно выбираем строку, которую отобразим для теста
        with open('data/tabl.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            s = random.randint(0, 7)
            for index, row in enumerate(reader):
                if index == s:
                    strin = "".join(row)
        self.textEdit.setText(strin)
        # настраиваем отображение подключенного изображения
        self.pixmap2 = self.pixmap2.scaled(820, 290, Qt.IgnoreAspectRatio)
        self.label.setGeometry(0, 0, 820, 290)
        self.label.setPixmap(self.pixmap2)
        # привязка нажатия кнопок к определенным функциям
        self.pushButton_4.clicked.connect(self.info)
        self.pushButton_3.clicked.connect(self.exit)
        # подключение к отслеживанию вводимого текста
        self.lineEdit.textChanged.connect(self.keyboard)
        self.lineEdit.setFocus()
        # убираем границу у textEdit и lineEdit (визуально не сочетается)
        self.textEdit.setStyleSheet("border: 0; font: 75 10pt 'Trebuchet MS'; color: rgb(197, 198, 199)")
        self.lineEdit_2.setStyleSheet("border: 0")
        # подключение счетчика
        self.timer.timeout.connect(self.update)
        # флаг для начала отсчета
        self.f = False

    def update(self):
        self.second += 1

    def keyboard(self):
        """Контроль введенного текста, начало отсчета и конец"""
        if len(self.lineEdit.text()) == 1 and not self.f:
            # начало отсчета
            self.f = True
            self.second = 0
            self.timer.start(1000)
        if len(self.lineEdit.text()) == len(self.textEdit.toPlainText()):
            # конец отсчета, вывод результатов
            self.timer.stop()
            self.r = Result(self, self.nick, self.second, len(self.textEdit.toPlainText()), True)
            self.r.show()
            self.close()
        # проверка на соответветсвие введенного текста заданному
        if (self.lineEdit.text() == self.textEdit.toPlainText()[:len(self.lineEdit.text())]) and \
                (len(self.lineEdit.text()) != len(self.textEdit.toPlainText())):
            self.lineEdit_2.setStyleSheet("border: 0; background-color : green")
        elif (self.lineEdit.text() != self.textEdit.toPlainText()[:len(self.lineEdit.text())]) and \
                (len(self.lineEdit.text()) != len(self.textEdit.toPlainText())):
            self.lineEdit_2.setStyleSheet("border: 0; background-color : red")


class Training(QWidget, Centre):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('design/test.ui', self)
        self.nick = args[-1]
        self.f = False  # флаг для начала отсчета
        self.timer = QTimer()  # подключение счетчика
        self.pixmap2 = QPixmap("image/keyboard.jpg")  # подключение изображения
        self.col_er = 0  # счетчик ошибок
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('image/icon.png'))  # добавление иконки приложения
        # настраиваем отображение подключенного изображения
        self.pixmap2 = self.pixmap2.scaled(820, 290, Qt.IgnoreAspectRatio)
        self.label.setGeometry(0, 0, 820, 290)
        self.label.setPixmap(self.pixmap2)
        # поиск нужного урока и вывод текста из урока
        result = self.cur.execute("SELECT * FROM profils WHERE nick = ?",
                                  (item_nick := self.nick,)).fetchall()
        self.all_id = len(self.cur.execute("SELECT * FROM progress").fetchall())
        self.id = result[0][3]
        if self.id == self.all_id:  # если обучение пройдено, начинается сначала
            upd = "UPDATE profils SET progress = ? WHERE nick = ?"
            self.id = 0
            data = (self.id, self.nick)
            self.cur.execute(upd, data)
            self.con.commit()
        text = self.cur.execute("SELECT * FROM progress WHERE id = ?",
                                (item_nick := self.id,)).fetchall()
        self.textEdit.setText(text[0][-1])
        self.label_2.setText(f"Exercise: {int(self.id) + 1}")
        # подключение к отслеживанию вводимого текста
        self.lineEdit.textChanged.connect(self.keyboard)
        self.lineEdit.setFocus()
        # привязка нажатия кнопок к определенным функциям
        self.pushButton_4.clicked.connect(self.info)
        self.pushButton_3.clicked.connect(self.exit)
        # подключение счетчика
        self.timer.timeout.connect(self.update)
        # убираем границу у textEdit и lineEdit (визуально не сочетается)
        self.textEdit.setStyleSheet("border: 0; font: 75 10pt 'Trebuchet MS'; color: rgb(197, 198, 199)")
        self.lineEdit_2.setStyleSheet("border: 0")

    def update(self):
        self.second += 1

    def keyboard(self):
        """Контроль введенного текста, начало отсчета и конец"""
        if len(self.lineEdit.text()) == 1 and not self.f:
            # начало отсчета
            self.f = True
            self.second = 0
            self.timer.start(1000)
        if len(self.lineEdit.text()) == len(self.textEdit.toPlainText()):
            self.timer.stop()
            # если урок последний, показывается окно с поздравлениями
            if self.all_id - 1 == self.id:
                self.end = End(self, self.nick)
                media = QUrl.fromLocalFile("media/end.mp3")
                content = QtMultimedia.QMediaContent(media)
                self.player = QtMultimedia.QMediaPlayer()
                self.player.setMedia(content)
                self.player.play()
                self.end.show()
                self.close()
            else:
                self.r = Result(self, self.nick, self.second, self.col_er, False)
                self.r.show()
                self.close()
        # проверка на соответветсвие введенного текста заданному
        if (self.lineEdit.text() == self.textEdit.toPlainText()[:len(self.lineEdit.text())]) and \
                (len(self.lineEdit.text()) != len(self.textEdit.toPlainText())):
            self.lineEdit_2.setStyleSheet("border: 0; background-color : green")
        elif (self.lineEdit.text() != self.textEdit.toPlainText()[:len(self.lineEdit.text())]) and \
                (len(self.lineEdit.text()) != len(self.textEdit.toPlainText())):
            self.lineEdit_2.setStyleSheet("border: 0; background-color : red")
            self.col_er += 1


class End(QWidget, Centre):
    def __init__(self, *args):
        super().__init__()
        self.nick = args[1]
        uic.loadUi('design/end.ui', self)
        # добавление гифки
        self.gif = QMovie('image/end.gif')
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('image/icon.png'))  # добавление иконки приложения
        # запуск гифки
        self.label.setScaledContents(True)
        self.label.setMovie(self.gif)
        self.gif.start()
        # обновление уровня
        upd = "UPDATE profils SET progress = ? WHERE nick = ?"
        result = self.cur.execute("SELECT progress FROM profils WHERE nick = ?",
                                  (item_nick := self.nick,)).fetchall()
        data = (result[0][0] + 1, self.nick)
        self.cur.execute(upd, data)
        self.con.commit()
        # привязка нажатия кнопок к определенным функциям
        self.pushButton_4.clicked.connect(self.exit)


class Result(QWidget, Centre):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('design/result.ui', self)
        # заводим переменные и передаем им значения из args
        self.test = args[-1]
        self.nick = args[1]
        self.seconds = args[2]
        if self.test:  # если был тест, то создаем перемнную с длинной текста из теста
            self.len_text = args[3]
        else:
            if args[3] == 0:  # если была тренировка, то создаем переменную с наличием ошибок и переменную с их кол-вом
                self.not_er = True
            else:
                self.not_er = False
            self.col_er = args[3]
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('image/icon.png'))  # добавление иконки приложения
        self.label_2.setText(f"Затраченное время: {self.seconds} секунд")

        if self.test:
            # выводим результаты
            self.label_3.setText(f"Количество символов: {self.len_text}")
            self.label_4.setText(f"Количество символов в минуту: {(self.len_text * 60) // self.seconds}")
            self.label_5.setText(f"Количсетво слов в минуту: {((self.len_text // 5) * 60) // self.seconds}")
            # обновляем информацию в базе, если побит рекорд
            speed_words = ((self.len_text // 5) * 60) // self.seconds
            speed_symbols = (self.len_text * 60) // self.seconds
            result = self.cur.execute("SELECT * FROM profils WHERE nick = ?",
                                      (item_nick := self.nick,)).fetchall()
            upd = "UPDATE profils SET all_progress = ? WHERE nick = ?"
            data = (result[0][7] + ", " + str(speed_symbols), self.nick)
            self.cur.execute(upd, data)
            if result[0][4] < speed_words:
                upd = "UPDATE profils SET speed_word = ? WHERE nick = ?"
                data = (speed_words, self.nick)
                self.cur.execute(upd, data)
            if result[0][5] < speed_symbols:
                upd = "UPDATE profils SET speed_symbols = ? WHERE nick = ?"
                data = (speed_symbols, self.nick)
                self.cur.execute(upd, data)
        else:
            self.label_3.setText(f"Количество ошибок: {self.col_er}")
            if self.col_er == 0:  # если нет ошибок предлагаем продолжить
                self.pushButton.setText("continue")
            if self.not_er:
                upd = "UPDATE profils SET progress = ? WHERE nick = ?"
                result = self.cur.execute("SELECT progress FROM profils WHERE nick = ?",
                                          (item_nick := self.nick,)).fetchall()
                data = (result[0][0] + 1, self.nick)
                self.cur.execute(upd, data)
        self.con.commit()
        # привязка нажатия кнопок к определенным функциям
        self.pushButton_2.clicked.connect(self.exit)
        self.pushButton.clicked.connect(self.again)

    def again(self):
        """Повторное открытие соответсвующего окна для прохождения"""
        self.player.play()
        if self.test:
            self.test = Test(self, self.nick)
            self.test.show()
        else:
            self.train = Training(self, self.nick)
            self.train.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
