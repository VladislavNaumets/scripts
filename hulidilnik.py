import datetime
from decimal import Decimal
from typing import List, Dict, Any, Tuple, Optional

# Тип для словаря продуктов
Goods = Dict[str, List[Dict[str, Any]]]

# 1. Добавление новой партии продукта
def add(items: Goods, title: str, amount: Decimal, expiration_date: Optional[str] = None):
    date = datetime.datetime.strptime(expiration_date, '%Y-%m-%d').date() if expiration_date else None
    entry = {'amount': amount, 'expiration_date': date}
    if title in items:
        items[title].append(entry)
    else:
        items[title] = [entry]

# 2. Добавление продукта из текстовой заметки
def add_by_note(items: Goods, note: str):
    parts = note.split()
    for i in range(len(parts) - 1, 0, -1):
        try:
            amount = Decimal(parts[i])
            title = ' '.join(parts[:i])
            expiration_date = parts[i + 1] if i + 1 < len(parts) else None
            add(items, title, amount, expiration_date)
            return
        except Exception:
            continue
    raise ValueError("Невозможно разобрать строку")

# 3. Поиск продуктов по названию
def find(items: Goods, needle: str) -> List[str]:
    needle = needle.lower()
    return [name for name in items if needle in name.lower()]

# 4. Подсчёт общего количества продукта
def amount(items: Goods, needle: str) -> Decimal:
    needle = needle.lower()
    total = Decimal('0')
    for name, entries in items.items():
        if needle in name.lower():
            for entry in entries:
                total += entry['amount']
    return total

# 5. Поиск просроченных или скоро истекающих продуктов
def expire(items: Goods, in_advance_days: int = 0) -> List[Tuple[str, Decimal]]:
    now = datetime.date.today()
    deadline = now + datetime.timedelta(days=in_advance_days)
    expired = {}
    for title, entries in items.items():
        for entry in entries:
            exp = entry['expiration_date']
            if exp is not None and exp <= deadline:
                expired[title] = expired.get(title, Decimal('0')) + entry['amount']
    return list(expired.items())

# Пример использования
if __name__ == "__main__":
    goods = {}

    add(goods, 'Яйца', Decimal('10'), '2023-09-30')
    add(goods, 'Яйца', Decimal('3'), '2023-10-15')
    add(goods, 'Вода', Decimal('2.5'))

    add_by_note(goods, 'Яйца гусиные 4 2023-07-15')

    print("Поиск по 'йц':", find(goods, 'йц'))
    print("Количество 'яйца':", amount(goods, 'яйца'))
    print("Просроченные на сегодня:", expire(goods))
    print("Просроченные через 30 дней:", expire(goods, 30))
    print("Все товары:", goods)