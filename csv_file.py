import os,sys

class CSV:
    def __init__(self):
        # Имя файла
        self.filename = ""
        # Разделитель
        self.delem = ""
        # Данные
        self.data = list()

    def Load(self,**args):
        if 'filename' in args.keys():
            self.filename = args['filename']
        else:
            raise NameError
        if 'delem' in args.keys():
            self.delem = args['delem']
        else:
            self.delem = ";"
        # Открываем файл, имя файла задаём через переменную
        # Файл открываем на чтение "r"
        # Кодировка UTF-8 ибо нехуй
        # read  -> читаем данные
        # split -> делим их на список через разделитель,
        # в нашем случае разделитель это новая строка.
        # В данном случае у нас получился массив из СТРОК
        temp_file = open(self.filename,"r",encoding="UTF-8").read().split("\n")
        # Проходимся циклом по каждой СТРОКЕ файла
        for line in temp_file:
            # СТРОКУ делим на СТОЛБЦЫ
            line = line.split(self.delem)
            # Добавляем в переменную новую строку
            self.data.append(line)

    def Save(self,**args):
        if 'filename' in args.keys():
            filename_current = args['filename']
        else:
            filename_current = self.filename
        if 'delem' in args.keys():
            delem_current = args['delem']
        else:
            delem_current = self.delem
        # Открываем файл
        file1 = open(filename_current,"w",encoding="UTF-8")
        # Создаём переменную для хранения всего файла
        line1 = str()
        for line in self.data: # Проходим каждую строку
            line1 += delem_current.join(line) # Добавляем данные в строку через разделитель
            line1 += "\n" # Переход на новую стрроку
        line1=line1[:len(line1)-1] # Лайфхак для удаления последней строки
        file1.write(line1) # Пишем файл
        file1.close()

    def Update(self,x,y,data):
        self.data[y][x]=data

    def rows(self): # Строки
        return len(self.data)

    def columns(self): # Столбцы
        max_l = 0
        for line in self.data:
            if max_l < len(line):
                max_l = len(line)
        return max_l
            

if __name__ == "__main__":
    pass
