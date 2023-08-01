from random import randint


BOARD_SIZE = 6
SHIPS_TYPES = [3, 2, 2, 1, 1, 1, 1]


class BoardException(Exception):
    """
    Родительский класс для представления ошибок в игре.
    """

    pass


class BoardOutException(BoardException):
    """
    Класс для представления ошибки выстрела за пределы игрового поля.
    """

    def __str__(self) -> str:
        """
        Устанавливает выводимое сообщение об ошибке
        """

        return '\n\tЭта точка за пределами игровой доски!'


class BoardUsedException(BoardException):
    """
    Класс для представления ошибки выстрела в уже стрелянную точку.
    """

    def __str__(self) -> str:
        """
        Устанавливает выводимое сообщение об ошибке
        """

        return '\n\tВы уже стреляли в эту точку!'


class BoardWrongShipException(BoardException):
    """
    Класс для представления ошибки размещения корабля.
    Эта ошибка нужна только для внутренней логики игры
    и не будет показываться пользователю.
    """

    pass


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

    def __init__(self, x: int, y: int) -> None:
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

    def __eq__(self, other: 'Dot') -> bool:
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
    direction : int
        Направление корабля (вертикальное/горизонтальное)
    lives : int
        Количеством жизней (сколько точек корабля еще не подбито).

    Методы
    --------
    @property
    dots():
        Возвращает список всех точек корабля.
    """

    def __init__(self, length: int, bow: Dot, direction: int) -> None:
        """
        Устанавливает все необходимые атрибуты для объекта Ship.

        Атрибуты
        --------
        length : int
            Длина.
        bow : Dot
            Точка, где размещён нос корабля.
        direction : int
            Направление корабля (вертикальное/горизонтальное)
        lives : int
            Количеством жизней (сколько точек корабля еще не подбито).
        """

        self.length = length
        self.bow = bow
        self.direction = direction
        self.lives = length

    @property
    def dots(self) -> list[Dot]:
        """
        Возвращает список всех точек корабля.
        """

        dot_list = list()
        for i in range(self.length):
            x, y = self.bow.x, self.bow.y

            if self.direction == 0:
                x += i
            elif self.direction == 1:
                y += i

            dot_list.append(Dot(x, y))
        return dot_list

    def is_strike(self, dot: Dot) -> bool:
        """
        Проверяет попадание,
        иными словами, принадлежит ли точка dot этому кораблю.
        """

        return dot in self.dots


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
    mark_oreol(Ship):
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

    def __init__(self) -> None:
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

        self.hide = False
        self.table = [['○'] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        self.ships = list()
        self.locked_dots = list()
        self.live_ships = len(SHIPS_TYPES)

    def add_ship(self, ship):
        """
        Ставит корабль на доску (если не получается, выбрасываем исключения).
        """

        for dot in ship.dots:
            if self.out(dot) or dot in self.locked_dots:
                raise BoardWrongShipException()
        for dot in ship.dots:
            self.table[dot.x][dot.y] = '■'
            self.locked_dots.append(dot)

        self.ships.append(ship)
        self.mark_oreol(ship)

    def mark_oreol(self, ship: Ship, hide: bool = True):
        """
        Формирует ореол корабля, т.е. помечает точки вокруг,
        где другого корабля по правилам быть не может.
        """

        neighbours = [(-1, -1), (0, -1), (1, -1), (-1, 0),
                      (1, 0), (-1, 1), (0, 1), (1, 1)]

        for dot in ship.dots:
            for dx, dy in neighbours:
                x, y = dot.x + dx, dot.y + dy
                current_dot = Dot(x, y)
                if not self.out(current_dot) and current_dot not in self.locked_dots:
                    self.locked_dots.append(current_dot)
                    if not hide:
                        if self.table[x][y] != '×':
                            self.table[x][y] = '•'

    def show(self) -> None:
        """
        Выводит доску в консоль в зависимости от параметра hide.
        """

        print(' X| 1 2 3 4 5 6')
        print('Y◢ ____________')
        for row in range(BOARD_SIZE):
            print(row + 1, end=' | ')
            for col in range(BOARD_SIZE):
                cell = self.table[col][row]
                if self.hide:
                    print('○', end=' ') if cell == '■' else print(cell, end=' ')
                else:
                    print(cell, end=' ')
            print('')
        print('\n')

    def out(self, dot: Dot) -> bool:
        """
        Возвращает True , если точка выходит за пределы поля,
        и False, если не выходит.
        """

        return not (0 <= dot.x < BOARD_SIZE and 0 <= dot.y < BOARD_SIZE)

    def shot(self, dot: Dot) -> bool:
        """
        Делает выстрел по доске.
        Если есть попытка выстрелить за пределы доски или
        в использованную точку, то выбрасывает исключения.
        Возвращает True, если у игрока остаётся право следующего выстрела.
        """

        if self.out(dot):
            raise BoardOutException
        if dot in self.locked_dots:
            raise BoardUsedException
        self.locked_dots.append(dot)
        for ship in self.ships:
            if ship.is_strike(dot):
                ship.lives -= 1
                self.table[dot.x][dot.y] = '×'
                if ship.lives == 0:
                    self.live_ships -= 1
                    self.mark_oreol(ship, hide=False)
                    print('\n\tКорабль потоплен!')
                    input()
                    return False
                else:
                    print('\n\tПопадание!')
                    input()
                    return True
        self.table[dot.x][dot.y] = '•'
        print('\n\tМимо.')
        input()
        return False

    def get_ready(self) -> None:
        """
        Обнуляет перед стартом игры множество заблокированных точек.
        """

        self.locked_dots = list()


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

    def __init__(self, own_board, opponent_board) -> None:
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

        raise NotImplementedError(f'Определите run в {self.__class__.__name__}.')

    def move(self) -> bool:
        """
        Делает ход в игре.
        Вызываем метод ask, делаем выстрел по вражеской доске (Board.shot),
        отлавливаем исключения, и, если они есть, пытаемся повторить ход.
        Возвращает True, если этому игроку нужен повторный
        ход (например, если он подбил корабль).
        """

        try:
            return self.opponent_board.shot(self.ask())
        except ValueError:
            print('\n\tВнимательнее, вводите две цифры через пробел.')
            if self.__class__.__name__ == 'User':
                input('Нажмите -= Enter =-')
            return True
        except Exception as e:
            print(e)
            if self.__class__.__name__ == 'User':
                input('Нажмите -= Enter =-')
            return True


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

    def ask(self) -> Dot:
        """
        Спрашивает игрока, в какую клетку он делает выстрел.
        Для AI это будет выбор случайной точки.
        """

        x, y = randint(1, BOARD_SIZE), randint(1, BOARD_SIZE)
        print(f'x y = {x} {y}', end='')
        input()
        return Dot(x - 1, y - 1)


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

    def ask(self) -> Dot:
        """
        Спрашивает игрока, в какую клетку он делает выстрел.
        """

        x, y = input('x y = ').split()
        if x and y:
            return Dot(int(x) - 1, int(y) - 1)
        else:
            raise ValueError


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
        Запуск игры. Сначала вызываем приветствие, затем игровой цикл.
    """

    def __init__(self) -> None:
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

        self.user_board = self.make_board()
        self.ai_board = self.make_board()
        self.ai_board.hide = True  # TODO
        self.user = User(self.user_board, self.ai_board)
        self.ai = AI(self.ai_board, self.user_board)

    def make_board(self):
        board = None
        while board is None:
            board = self.random_board()
        board.get_ready()
        return board

    def random_board(self):
        board = Board()
        attempts = 0
        for length in SHIPS_TYPES:
            while True:
                if attempts > 2000:
                    return None

                try:
                    board.add_ship(Ship(length,
                                        Dot(randint(0, BOARD_SIZE-1),
                                            randint(0, BOARD_SIZE-1)
                                            ),
                                        randint(0, 1)
                                        )
                                   )
                    break
                except BoardWrongShipException:
                    pass

                attempts += 1
        return board

    def greet(self):
        """
        Приветствует в консоли пользователя и рассказывает о формате ввода.
        """

        logo = """
         ____        _   _   _           _     _          _____                      
        |  _ \      | | | | | |         | |   (_)        / ____|                     
        | |_) | __ _| |_| |_| | ___  ___| |__  _ _ __   | |  __  __ _ _ __ ___   ___ 
        |  _ < / _` | __| __| |/ _ \/ __| '_ \| | '_ \  | | |_ |/ _` | '_ ` _ \ / _ \\
        | |_) | (_| | |_| |_| |  __/\__ \ | | | | |_) | | |__| | (_| | | | | | |  __/
        |____/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/   \_____|\__,_|_| |_| |_|\___|
                                                | |                                  
                                                |_|                                  
        """
        text = """
        Привет! Это «Морской бой». Правила ты знаешь.
        Бой идёт до полного уничтожения одной из сторон.
        К счастью для тебя, компьютер пуляет просто наугад.

        Координаты выстрела вводятся цифрами через пробел:
        \t координата по горизонтали (X), пробел, координата по вертикали (Y) 
        """
        marks = """
        Обозначения:
            ■ - палуба
            • - мимо / ореол корабля
            ○ - море
            × - попадание
        """
        print(logo)
        print(text)
        print(marks)
        input('Нажмите -= Enter =-')

    def show_boards(self) -> None:
        """
        Выводит на экран доски обоих игроков.
        """
        print('\n\n\n' + '-' * 50)
        print('Доска пользователя:\n')
        self.user.own_board.show()
        print('Доска компьютера:\n')
        self.ai.own_board.show()

    def loop(self):
        """
        Игровой цикл. Там мы просто последовательно вызываем метод move для
        игроков и делаем проверку, сколько живых кораблей осталось на досках,
        чтобы определить победу.
        """

        player = 0
        while True:
            self.show_boards()

            if player % 2 == 0:
                print('Ваш ход:')
                repeat = self.user.move()
            else:
                print('Ходит компьютер:')
                repeat = self.ai.move()

            player += 0 if repeat else 1

            if self.ai.own_board.live_ships == 0:
                print('\n\n\n' + '-' * 50)
                # print('#' * 22)
                # print('#    Вы выиграли!    #')
                # print('#' * 22)
                print('#' * 22 + '\n#    Вы выиграли!    #\n' + '#' * 22)
                self.show_boards()
                break

            if self.user.own_board.live_ships == 0:
                print('\n\n\n' + '-' * 50)
                # print('#' * 22)
                # print('# Компьютер выиграл! #')
                # print('#' * 22)
                print('#' * 22 + '\n# Компьютер выиграл! #\n' + '#' * 22)
                self.show_boards()
                break

    def start(self):
        """
        Запуск игры. Сначала вызываем приветствие, затем игровой цикл.
        """

        self.greet()
        self.loop()


if __name__ == '__main__':
    game = Game()
    game.start()
