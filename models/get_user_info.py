from loader import db

def get_resource(userid: str, resource: str) -> int:
    """Получаем оперделенный ресурс из бд. `userid`=id пользователя, `resource={wood, coins, level, barn_accumulation}`"""
    user_resource = db.execute(sql=f"SELECT {resource} FROM users WHERE id=?", params=(userid, ), fethcone=True)
    return user_resource[0]


def get_animals(userid: str, animal: str) -> int:
    """Получаем количество определенного животного. `animal={sheep, chicken, cow}`"""
    user_animal = db.execute(sql=f"SELECT {animal} FROM animals WHERE user_id=?", params=(userid, ), fethcone=True)
    return user_animal[0]


def get_item(userid: str, item: str) -> int:
    """Получаем количество определенного предмета. `item={wool, egg, milk}`"""
    user_item = db.execute(sql=f"SELECT {item} FROM user_items WHERE user_id = ?", params=(userid, ), fethcone=True)
    return user_item[0]
