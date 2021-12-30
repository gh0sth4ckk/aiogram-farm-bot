import sqlite3
from typing import Optional

class Database:
    def __init__(self, path="db.sqlite3") -> None:
        self.path = path # Путь до бд
    
    @property
    def connect(self) -> str:
        """Создание подключения к базе данных"""
        return sqlite3.connect(self.path)
    
    def execute(self, sql:str, params:tuple=None, fethcone=False, fetchall=False, commit=False) -> Optional[str]:
        """Создает запрос к базе данных
        sql str: Запрос к базе данных в виде строки.
        params tuple[опционально]: Значения вопросительных знаков если таковые присутствуют.
        fetchone, fetchall bool[опиционально]: Один на выбор, возвращает либо один элемент, либо все.
        commit bool[опционально]: Подтверждение внесения или иземенения информации в бд если таковой требуется.
        """
        data = None
        
        connection = self.connect # Подключение
        cursor = connection.cursor()
        
        if params is not None: # Если параметры присутствуют
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        if commit:
            connection.commit()
        if fethcone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close() # Закрытие соединения
        return data