import random


class Ship:
    def __init__(self, length, tp=1, y=None, x=None):
        self._length = length
        self._tp = tp
        self._x = x
        self._y = y
        self._is_move = True
        self._cells = [1 for _ in range(length)]
        self._coords = []
        self._pole = None

    def set_start_coords(self, y, x):  # установка начальных координат
        if 0 <= x < 10  and 0 <= y < 10 :
            self._x = x
            self._y = y
        else:
            raise ValueError

    def get_start_coords(self):  # получение начальных координат корабля
        return (self._y, self._x)

    def try_move(self, fake_ship):  # перемещение корабля. изменение поля и координат внутри объекта корабля
        self._x, self._y = fake_ship._x, fake_ship._y
        for coord in self._coords:
            y = coord[0]
            x = coord[1]
            self._pole._pole[y][x] = 0
        self._coords = []
        x =fake_ship.get_start_coords()[1]
        y = fake_ship.get_start_coords()[0]
        for i in range(self._length):
            self._pole._pole[y][x] = self
            self._coords.append((y, x))
            if self._tp == 1:
                x += 1
            else:
                y += 1

    def move(self, go):  # перемещение корабля в направлении его ориентации на go клеток
        if self._is_move:
            trend = random.choice([-1, 1])
            y, x = self.get_start_coords()
            a = trend * go
            q, w = (0, 1) if self._tp == 1 else (1, 0)
            fake_ship = Ship(self._length, self._tp)
            fake_ship._pole = self._pole
            try:
                fake_ship.set_start_coords(y + (a * q), x + (a * w))
                if fake_ship.is_out_pole(self._pole._size) and self.is_collide(
                    fake_ship):
                    self.try_move(fake_ship)
                else:
                    raise Exception
            except:
                try:
                    fake_ship.set_start_coords(y - (a * q), x - (a * w))
                    if fake_ship.is_out_pole(self._pole._size) and self.is_collide(
                        fake_ship):
                        self.try_move(fake_ship)
                except:
                    pass


            '''fake_ship = Ship(self._length, self._tp, y + a * q, x + a * w)
            fake_ship2 = Ship(self._length, self._tp, y - a * q, x - a * w)
            if fake_ship.is_out_pole(self._pole._size) and self.is_collide(
                    fake_ship):  # проверка, в какую сторону может сдвинуться корабль
                self.try_move(fake_ship)
            elif fake_ship2.is_out_pole(self._pole._size) and self.is_collide(fake_ship2):
                self.try_move(fake_ship2)'''

    def ship_and_ship(self, y, x):  # проверка каждой координаты корабля на наложение на другой корабль
        s = []
        try:
            for i in range(y - 1, y + 2):
                for j in range(x - 1, x + 2):
                    if self._pole._pole[i][j] == self or self._pole._pole[i][j] == 0:
                        s.append(False)
                    else:
                        s.append(True)
        except:
            True
        return any(s)
#Ship(4, 1, 0, 0) и Ship(3, 2, 0, 2)
    def is_collide(self, ship):  # проверка на столкновение с другим кораблем
        y, x = ship.get_start_coords()
        s = []
        for _ in range(self._length):
            s.append(self.ship_and_ship(y, x))
            if self._tp == 1:
                x += 1
            else:
                y += 1
        return any(s)

    def is_out_pole(self, size):  # проверка на выход корабля за пределы игрового поля
        y, x = self.get_start_coords()
        s = x if self._tp == 1 else y
        if s + self._length < size:
            return False
        else:
            return True

    def __getitem__(self, indx):
        return self._cells[indx]

    def __setitem__(self, indx, value):
        self._cells[indx] = value


class GamePole:
    def __init__(self, size=10):
        self._size = size
        self._ships = []
        self._pole = [[0] * self._size for _ in range(self._size)]

    def init(self):
        self._ships.append(Ship(4, tp=random.randint(1, 2)))
        for _ in range(2):
            self._ships.append(Ship(3, tp=random.randint(1, 2)))
        for _ in range(3):
            self._ships.append(Ship(2, tp=random.randint(1, 2)))
        for _ in range(4):
            self._ships.append(Ship(1, tp=random.randint(1, 2)))
        w = [Ship(4, 1, 0, 0),Ship(3, 2, 0, 0)]
        for ship in w:
            print(ship._y, ship._x, id(ship))
            ship._pole = self
            t = 0
            #while t == 0:
                #ship.set_start_coords(random.randint(0, 9), random.randint(0, 9))
                #print(ship.get_start_coords())
            y, x = ship.get_start_coords()
            if ship.is_out_pole(self._size) and not ship.is_collide(ship):
                for i in range(ship._length):
                    if self._pole[y][x] == 0:
                        self._pole[y][x] = ship
                        ship._coords.append((y, x))
                        if ship._tp == 1:
                            x += 1
                        else:
                            y += 1
                    #t = 1

    def show(self): #вызов образа игрового поля в консоль
        show_pole = []
        for row in range(len(self._pole)):
            r = []
            for i in range(len(self._pole[row])):
                w = self._pole[row][i]
                if type(w) != int:
                    if w._tp == 1:
                        a = w._cells[i - w.get_start_coords()[1]]
                    else:
                        a = w._cells[row - w.get_start_coords()[0]]
                else:
                    a = w

                r.append(a)
            show_pole.append(r)
        for row in show_pole:
            print(*row)

    def move_ships(self):
        for ship in self._ships:
            ship.move(1)

Game = GamePole()
Game.init()
Game.show()
#s1 = Ship(4, 1, 0, 0)
#s2 = Ship(3, 2, 0, 2)
#print(s1.is_collide(s2))

'''Game = GamePole()
Game.init()
# print(Game.__dict__)
Game.show()
#for ship in Game._ships:
#    print(ship._coords, ship._y, ship._x,ship._tp)
Game.move_ships()
print()
#for ship in Game._ships:
#    print(ship._coords, ship._y, ship._x,ship._tp)
Game.show()'''

ship = Ship(2)
ship = Ship(2, 1)
ship = Ship(3, 2, 0, 0)

assert ship._length == 3 and ship._tp == 2 and ship._x == 0 and ship._y == 0, "неверные значения атрибутов объекта класса Ship"
assert ship._cells == [1, 1, 1], "неверный список _cells"
assert ship._is_move, "неверное значение атрибута _is_move"

#ship.set_start_coords(1, 2)
#print(ship.get_start_coords(), ship._y)
#assert ship._x == 1 and ship._y == 2, "неверно отработал метод set_start_coords()"
#assert ship.get_start_coords() == (1, 2), "неверно отработал метод get_start_coords()"

ship.move(1)
s1 = Ship(4, 1, 0, 0)
s2 = Ship(3, 2, 0, 0)
s3 = Ship(3, 2, 0, 2)

print(s1.is_collide(s2))
assert s1.is_collide(s2), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 0, 0)"
print(s1.is_collide(s3))
assert s1.is_collide(s3) == False, "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 0, 2)"

s2 = Ship(3, 2, 1, 1)
assert s1.is_collide(s2), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 1, 1)"

s2 = Ship(3, 1, 8, 1)
assert s2.is_out_pole(10), "неверно работает метод is_out_pole() для корабля Ship(3, 1, 8, 1)"

s2 = Ship(3, 2, 1, 5)
assert s2.is_out_pole(10) == False, "неверно работает метод is_out_pole(10) для корабля Ship(3, 2, 1, 5)"

s2[0] = 2
assert s2[0] == 2, "неверно работает обращение ship[indx]"

p = GamePole(10)
p.init()
for nn in range(5):
    for s in p._ships:
        assert s.is_out_pole(10) == False, "корабли выходят за пределы игрового поля"

        for ship in p.get_ships():
            if s != ship:
                assert s.is_collide(ship) == False, "корабли на игровом поле соприкасаются"
    p.move_ships()

gp = p.get_pole()
assert type(gp) == tuple and type(gp[0]) == tuple, "метод get_pole должен возвращать двумерный кортеж"
assert len(gp) == 10 and len(gp[0]) == 10, "неверные размеры игрового поля, которое вернул метод get_pole"

pole_size_8 = GamePole(8)
pole_size_8.init()
