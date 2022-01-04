from loader import db
from models.get_user_info import get_resource


def give_points(userid: str, points: int) -> None:
    """Дает пользователю после определенного действия `points` очков опыта."""
    user_points = get_resource(userid, "points")
    db.execute(f"UPDATE users SET points = points + {points} WHERE id=?", params=(userid, ), commit=True)

def update_level(userid:str) -> None:
    """Обновляет уровень игрока."""
    lvl = get_resource(userid, "points") // 100
    db.execute(f"UPDATE users SET level = {lvl} WHERE id=?", params=(userid, ), commit=True)