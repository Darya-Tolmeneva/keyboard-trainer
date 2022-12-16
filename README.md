# keyboard-trainer
![hippo](https://github.com/Darya-Tolmeneva/keyboard-trainer/blob/master/image/cute-happy.gif)
## Идея и функционал
Основная идея проекта заключается в создании клавиатурного тренажера для всех, кто хочет научиться печатать 10-ю пальцами. Но также данная программа умеет проверять скорость печати в количестве символов в минуту и количестве слов в минуту, вести статистику и отображать ее пользователю, а еще если пользователь забудет пароль (3 раза ошибется при вводе), то программа отправит ему на почту его пароль.
## Реализация
В основе всего приложения лежит класс **Centre** (центральный класс), от него наследуются практически все окна. Он обладает таким функционалом как открытие окна информации, переход на предыдущее и главное окно. В этом классе инициализирован звук нажатия, который издают все кнопки в приложении и подключение к базе данных. После идут классы всех остальных окон. Наполнение уроков заимствовано с https://www.ratatype.ru/ 
## Технологии
В своем коде я использовала модули **smtplib**, **email** благодаря им происходит отправка пароля пользователю на почту, если он забыл его. А еще я использовала **QtMultimedia** для отображения гифки во время загрузки окон. Стоит так же упомянуть, что я использовала библиотеку **pyqtgraph** чтобы показывать пользователю его прогресс в окне статистики.

![hippo](https://github.com/Darya-Tolmeneva/keyboard-trainer/blob/master/image/avatar.gif)
## Idea and functionality
The main idea of the project is to create a keyboard simulator for everyone who wants to learn how to type with 10 fingers. But also this program is able to check the printing speed in the number of characters per minute and the number of words per minute, keep statistics and display it to the user, and if the user forgets the password (makes a mistake 3 times when entering), the program will send him his password by email.
## Implementation
The whole application is based on the **Centre** class (the central class), almost all windows are inherited from it. It has such functionality as opening the information window, switching to the previous and main window. In this class, the clicking sound is initialized, which is produced by all the buttons in the application and the connection to the database. After that come the classes of all the other windows. The content of the lessons is borrowed from https://www.ratatype.ru/
## Technologies
In my code, I used the modules **smtplib**, **email** thanks to them, the password is sent to the user by mail if he forgot it. And I also used **QtMultimedia** to display gifs while loading windows. It is also worth mentioning that I used the **pyqtgraph** library to show the user his progress in the statistics window.

