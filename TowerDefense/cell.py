from interface import implements
from subject import Subject


class Cell(implements(Subject)):
    TYPE2COL = {'path': 'saddlebrown', 'cannon': 'darkgrey', 'other': 'darkgreen'}

    def __init__(self, canvas, x, y, size, type='other'):
        self._canvas = canvas
        self._x = x
        self._y = y
        self._size = size
        self._upperLeftX = x * size
        self._upperLeftY = y * size
        self._lowerRightX = self._upperLeftX + size
        self._lowerRightY = self._upperLeftY + size
        self._tag = "cell" + str(x) + str(y)
        self._id = None
        self._mouseIn = False
        self.set_type(type)
        self._id = self._canvas.create_rectangle(self._upperLeftX, self._upperLeftY,
                                                 self._lowerRightX, self._lowerRightY,
                                                 fill=Cell.TYPE2COL[self._type],
                                                 outline=Cell.TYPE2COL[self._type], tag=self._tag)
        self._canvas.tag_bind(self._id, "<Enter>", self.highlight)
        self._canvas.tag_bind(self._id, "<Leave>", self.clear)
        self._canvas.tag_bind(self._id, "<Button-1>", self.notify_observers)
        self._observers = []

    def __contains__(self, xy):
        x, y = xy
        return self._upperLeftX < x < self._lowerRightX and self._upperLeftY < y < self._lowerRightY

    def notify_observers(self, event=None):
        for observer in self._observers:
            observer.update(self)

    def register_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        observer_index = self._observers.index(observer)
        self._observers.pop(observer_index)

    def highlight(self, event=None):
        self._canvas.itemconfig(self._id, fill='lightgrey', outline='lightgrey')
        self._mouseIn = True

    def clear(self, event=None):
        self._mouseIn = False
        self._canvas.itemconfig(self._id, fill=Cell.TYPE2COL[self._type], outline=Cell.TYPE2COL[self._type])

    def get_type(self):
        return self._type

    def get_row(self, event):
        return int(event.x / self._size)

    def get_column(self, event):
        return int(event.y / self._size)

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_center_x(self):
        return self._upperLeftX + (self._size / 2)

    def get_center_y(self):
        return self._upperLeftY + (self._size / 2)

    def get_center(self):
        return self.get_center_x(), self.get_center_y()

    def set_type(self, type):
        assert type in ('path', 'cannon', 'other')
        self._type = type
        if self._id is not None:
            self._canvas.itemconfig(self._id, fill=Cell.TYPE2COL[self._type], outline=Cell.TYPE2COL[self._type])
        if self._type == 'cannon':
            self._canvas.create_oval(self._upperLeftX + 4, self._upperLeftY + 4,
                                      self._lowerRightX - 5, self._lowerRightY - 5,
                                      fill='black', outline='black', tag=self._tag)
