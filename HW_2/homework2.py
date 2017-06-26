from datetime import date

# Задание 2. ООП и исключения.
#
# Напишите реализации объявленных ниже классов. Для проверки
# корректности реализации ваших функций, запустите этот файл
# на выполнение с помощью интерпретатора:
#
# python3 homework2.py
#
# Если написанный вами код не содержит синтаксических ошибок,
# вы увидите результаты тестов ваших решений.


# 1. Класс Student
#
# Реализуйте класс Student со следующими переменными:
#   name        строка
#   birthdate   дата рождения, объект типа date из библиотеки datetime
#   email       строка
# 
# Реализуйте следующие методы:
# __init__
#   Инициализация переменных. Метод должен проверять значения аргументов,
#   и возбуждать исключение ValueError, если
#   - строка name - пустая
#   - дата birthdate - в будущем,
#   - строка email не содержит символ '@'.
#
# __eq__
#   Для сравнения экземпляров. Два объекта равны, если равны значения всех переменных.
#
# __str__
#   Строковое представление объекта вида "name <email>"
#
# age
#   Возвращает целое число - возраст в годах

class Student:

    def __init__(self, name, birthdate, email):
        if name == '' or birthdate > date.today() or '@' not in email:
            raise ValueError
        else:
            self.name = name
            self.birthdate = birthdate
            self.email = email

    def __eq__(self, other):
        if self.email == other.email and self.birthdate == other.birthdate and self.email == other.email:
            return True
        else:
            return False

    def __str__(self):
        return '{} <{}>'.format(self.name, self.email)

    def age(self):
        return date.today().year - self.birthdate.year 

# 2. Класс Course
#
# Реализуйте класс Course со следующими аттрибутами
#   title       строка
#   start_date  дата начала, дата рождения, объект типа date из библиотеки datetime
#   end_date    дата окончания, дата рождения, объект типа date из библиотеки datetime
#
# и методами
# __init__
#   Инициализация. Должен возбуждать исключение ValueError, если start_date
#   больше end_date или строка title пустая.
#
# enroll(student)
#   Регистрация студента на курс. Возбуждает исключение CourseFinished (реализуйте исключение),
#   если курс уже завершен, т.е. дата end_date уже прошла. В случае, если студент
#   уже зарегистрирован на курс, возбуждает исключение AlreadyEnrolled (также реализуйте).
#
# num_enrolled
#   Возвращает количество зарегистрированных студентов.

class Course:
    enrolled_student = []

    def __init__(self, title, start_date, end_date):
        if start_date < end_date:
            self.title = title
            self.start_date = start_date
            self.end_date = end_date
        else:
            raise ValueError
    
    def enroll(self, student):
        if self.end_date < date.today():
            if student not in self.enrolled_student:
                self.enrolled_student.append(student)
            else:
                raise AlreadyEnrolled
        else:
            raise CurseFinished

    def num_enrolled(self):
        return len(self.enrolled_student)

class CurseFinished(Exception):
    """
    Raise exception when course already finished
    """
    pass

class  AlreadyEnrolled(Exception):
    """
    Raise exception when student is already enrolled
    """
    pass    



##### Конец задания. Дальше идет проверочный код, который вы не правите.



import unittest

class TestStudent(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(ValueError):
            Student('', date(1970, 1, 1), 'evil@fbi.gov')
        with self.assertRaises(ValueError):
            Student('Random J. Hacker', date(2018, 1, 1), 'evil@fbi.gov') # Старые тесты
        with self.assertRaises(ValueError):
            Student('Random J. Hacker', date(1970, 1, 1), 'evil#fbi.gov')

    def test_eq(self):
        s1 = Student('Random J. Hacker', date(1970, 1, 1), 'evil@fbi.gov')
        s2 = Student('Random J. Hacker', date(1970, 1, 1), 'evil@fbi.gov')
        s3 = Student('Student 1', date(1989, 1, 1), 'student@web-academy.com.ua')
        self.assertEqual(s1, s2)
        self.assertNotEqual(s1, s3)

    def test_str(self):
        s = Student('Student', date(1985, 1, 1), 'student@web-academy.com.ua')
        self.assertEqual('Student <student@web-academy.com.ua>', str(s))    

    def test_age(self):
        s = Student('Random J. Hacker', date(1970, 1, 1), 'evil@fbi.gov')
        self.assertEqual(s.age(), 47) # Старые тесты


class TestCourse(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(ValueError):
            Course('Python/Django for beginners', date(2016, 6, 1), date(2016, 5, 1))
    
    def test_num_enrolled(self):
        c = Course('Python/Django for beginners', date(2016, 5, 21), date(2016, 7, 1))
        c.enroll(Student('Student 1', date(1980, 1, 1), 'student1@web-academy.com.ua'))
        c.enroll(Student('Student 2', date(1980, 1, 1), 'student2@web-academy.com.ua'))
        self.assertEqual(c.num_enrolled(), 2)


if __name__ == '__main__':
    unittest.main()
