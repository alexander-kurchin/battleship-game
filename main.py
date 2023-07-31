# 1. Внутренняя логика игры -
# корабли, игровая доска и вся логика связанная с ней.

class BoardOutException(Exception):
    """
    Класс для представления ошибки выстрела за пределы игрового поля.
    """

    def __str__(self):
        """
        Устанавливает выводимое сообщение об ошибке
        """

        return 'Эта точка за пределами игровой доски!'


class BoardUsedException(Exception):
    """
    Класс для представления ошибки выстрела в уже стрелянную точку.
    """

    def __str__(self):
        """
        Устанавливает выводимое сообщение об ошибке
        """

        return 'Вы уже стреляли в эту точку!'


class Dot():
    """
    Класс для представления точки на поле.

    Атрибуты
    --------
    x : int
        Координата по оси x
    y : int
        Координата по оси y
    """

    def __init__(self, x, y):
        """
        Устанавливает все необходимые атрибуты для объекта Dot.

        Атрибуты
        --------
        x : int
            Координата по оси x
        y : int
            Координата по оси y
        """

        self.x = x
        self.y = y

    def __eq__(self, other):
        """
        Позволяет проверять точки на равенство.
        Теперь, чтобы проверить, находится ли точка в списке,
        достаточно просто использовать оператор in.
        """

        return self.x == other.x and self.y == other.y


class Ship():
    """
    Класс для представления корабля на поле.

    Атрибуты
    --------
    length : int
        Длина.
    bow : Dot
        Точка, где размещён нос корабля.
    direction : ???
        Направление корабля (вертикальное/горизонтальное)
    lives : int
        Количеством жизней (сколько точек корабля еще не подбито).

    Методы
    --------
    @property
    dots():
        Возвращает список всех точек корабля.
    """

    def __init__(self, length, bow, direction, lives):
        """
        Устанавливает все необходимые атрибуты для объекта Ship.

        Атрибуты
        --------
        length : int
            Длина.
        bow : Dot
            Точка, где размещён нос корабля.
        direction : ???
            Направление корабля (вертикальное/горизонтальное)
        lives : int
            Количеством жизней (сколько точек корабля еще не подбито).
        """

        self.length = length
        self.bow = bow
        self.direction = direction
        self.lives = lives

    @property
    def dots(self) -> list:
        """
        Возвращает список всех точек корабля.
        """

        pass


class Board():
    """
    Класс для представления игровой доски.

    Атрибуты
    --------
    table : list
        Двумерный список, в котором хранятся состояния каждой из клеток.
    ships : list
        Список кораблей доски.
    hide : bool
        Информация о том, нужно ли скрывать
        корабли на доске (для вывода доски врага),
        или нет (для своей доски).
    live_ships : int
        Количество живых кораблей на доске.

    Методы
    --------
    add_ship(Ship):
        Ставит корабль на доску (если не получается, выбрасываем исключения).
    contour(Ship):
        Обводит корабль по контуру (т.е. помечает соседние точки,
        где корабля по правилам быть не может).
    show(hide):
        Выводит доску в консоль в зависимости от параметра hide.
    out(Dot):
        Возвращает True , если точка выходит за пределы поля,
        и False, если не выходит.
    shot(Dot):
        Делает выстрел по доске (если есть попытка выстрелить
        за пределы или в использованную точку, выбрасывает исключения).
    """

    def __init__(self, table, ships, hide, live_ships):
        """
        Устанавливает все необходимые атрибуты для объекта Board.

        Атрибуты
        --------
        table : list
            Двумерный список, в котором хранятся состояния каждой из клеток.
        ships : list
            Список кораблей доски.
        hide : bool
            Информация о том, нужно ли скрывать
            корабли на доске (для вывода доски врага),
            или нет (для своей доски).
        live_ships : int
            Количество живых кораблей на доске.
        """

        self.table = table
        self.ships = ships
        self.hide = hide
        self.live_ships = live_ships

    def add_ship(self, ship):
        """
        Ставит корабль на доску (если не получается, выбрасываем исключения).
        """

        pass

    def contour(self, ship):
        """
        Обводит корабль по контуру (т.е. помечает соседние точки,
        где корабля по правилам быть не может).
        """

        pass

    def show(self, hide):
        """
        Выводит доску в консоль в зависимости от параметра hide.
        """

        pass

    def out(self, dot):
        """
        Возвращает True , если точка выходит за пределы поля,
        и False, если не выходит.
        """

        pass

    def shot(self, dot):
        """
        Делает выстрел по доске (если есть попытка выстрелить
        за пределы или в использованную точку, выбрасывает исключения).
        """

        pass


# 2. Внешняя логика игры -
# пользовательский интерфейс,
# искусственный интеллект,
# игровой контроллер, который считает побитые корабли.


class Player():
    """
    Класс для представления игрока. Этот класс будет родителем
    для классов AI (игрок-компьютер) и User (игрок-пользователь).

    Атрибуты
    --------
    own_board : Board
        Собственная доска.
    opponent_board: Board
        Доска соперника.

    Методы
    --------
    ask():
        Спрашивает игрока, в какую клетку он делает выстрел.
        Потомки должны реализовать этот метод.
    move():
        Делает ход в игре.
        Вызываем метод ask, делаем выстрел по вражеской доске (Board.shot),
        отлавливаем исключения, и, если они есть, пытаемся повторить ход.
        Возвращает True, если этому игроку нужен повторный
        ход (например, если он подбил корабль).
    """

    def __init__(self, own_board, opponent_board):
        """
        Устанавливает все необходимые атрибуты для объекта Player.

        Атрибуты
        --------
        own_board : Board
            Собственная доска.
        opponent_board: Board
            Доска соперника.
        """

        self.own_board = own_board
        self.opponent_board = opponent_board

    def ask(self):
        """
        Спрашивает игрока, в какую клетку он делает выстрел.
        Потомки должны реализовать этот метод.
        """

        pass

    def move() -> bool:
        """
        Делает ход в игре.
        Вызываем метод ask, делаем выстрел по вражеской доске (Board.shot),
        отлавливаем исключения, и, если они есть, пытаемся повторить ход.
        Возвращает True, если этому игроку нужен повторный
        ход (например, если он подбил корабль).
        """

        pass


class AI(Player):
    """
    Класс для представления игрока-компьютера.

    Наследуемые атрибуты
    --------
    own_board : Board
        Собственная доска.
    opponent_board: Board
        Доска соперника.

    Наследуемые методы
    --------
    move():
        Делает ход в игре.
        Вызываем метод ask, делаем выстрел по вражеской доске (Board.shot),
        отлавливаем исключения, и, если они есть, пытаемся повторить ход.
        Возвращает True, если этому игроку нужен повторный
        ход (например, если он подбил корабль).

    Методы
    --------
    ask():
        Спрашивает игрока, в какую клетку он делает выстрел.
        Для AI это будет выбор случайной точки.
    """

    def ask(self):
        """
        Спрашивает игрока, в какую клетку он делает выстрел.
        Для AI это будет выбор случайной точки.
        """

        pass


class User(Player):
    """
    Класс для представления игрока-пользователя.

    Наследуемые атрибуты
    --------
    own_board : Board
        Собственная доска.
    opponent_board: Board
        Доска соперника.

    Наследуемые методы
    --------
    move():
        Делает ход в игре.
        Вызываем метод ask, делаем выстрел по вражеской доске (Board.shot),
        отлавливаем исключения, и, если они есть, пытаемся повторить ход.
        Возвращает True, если этому игроку нужен повторный
        ход (например, если он подбил корабль).

    Методы
    --------
    ask():
        Спрашивает игрока, в какую клетку он делает выстрел.
    """

    def ask(self):
        """
        Спрашивает игрока, в какую клетку он делает выстрел.
        """

        pass


class Game():
    """
    Класс для представления игры.

    Атрибуты
    --------
    user : User
        Игрок-пользователь.
    user_board : Board
        Доска пользователя.
    ai : AI
        Игрок-компьютер, объект класса Ai .
    ai_board : Board
        Доска компьютера.

    Методы
    --------
    random_board():
        Генерирует случайную доску.
        Для этого мы просто пытаемся в случайные клетки изначально пустой
        доски расставлять корабли (в бесконечном цикле пытаемся поставить
        корабль в случайную току, пока наша попытка не окажется успешной).
        Лучше расставлять сначала длинные корабли, а потом короткие. Если
        было сделано много (несколько тысяч) попыток установить корабль, но
        это не получилось, значит доска неудачная и на неё корабль уже не
        добавить. В таком случае нужно начать генерировать новую доску.
    greet():
        Приветствует в консоли пользователя и рассказывает о формате ввода.
    loop():
        Игровой цикл. Там мы просто последовательно вызываем метод move для
        игроков и делаем проверку, сколько живых кораблей осталось на досках,
        чтобы определить победу.
    start():
        Запуск игры. Сначала вызываем greet, а потом loop.
    """

    def __init__(self, user, user_board, ai, ai_board):
        """
        Устанавливает все необходимые атрибуты для объекта Game.

        Атрибуты
        --------
        user : User
            Игрок-пользователь.
        user_board : Board
            Доска пользователя.
        ai : AI
            Игрок-компьютер, объект класса Ai .
        ai_board : Board
            Доска компьютера.
        """

        self.user = user
        self.user_board = user_board
        self.ai = ai
        self.ai_board = ai_board

    def random_board():
        """
        Генерирует случайную доску.
        Для этого мы просто пытаемся в случайные клетки изначально пустой
        доски расставлять корабли (в бесконечном цикле пытаемся поставить
        корабль в случайную току, пока наша попытка не окажется успешной).
        Лучше расставлять сначала длинные корабли, а потом короткие. Если
        было сделано много (несколько тысяч) попыток установить корабль, но
        это не получилось, значит доска неудачная и на неё корабль уже не
        добавить. В таком случае нужно начать генерировать новую доску.
        """

        pass

    def greet():
        """
        Приветствует в консоли пользователя и рассказывает о формате ввода.
        """

        pass

    def loop():
        """
        Игровой цикл. Там мы просто последовательно вызываем метод move для
        игроков и делаем проверку, сколько живых кораблей осталось на досках,
        чтобы определить победу.
        """

        pass

    def start():
        """
        Запуск игры. Сначала вызываем greet, а потом loop.
        """

        pass


if __name__ == '__main__':
    game = Game()
    game.start()
