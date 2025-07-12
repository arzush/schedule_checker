from schedule import Schedule, fetch_schedule

def print_slots(slots, label):
    print(f"\n{label}:")
    for s in slots:
        print(f"  {s.start.strftime('%H:%M')} - {s.end.strftime('%H:%M')}")

if __name__ == "__main__":
    date = input("Введите дату (гггг-мм-дд): ").strip()
    schedule_data = fetch_schedule()
    schedule = Schedule(schedule_data)

    busy = schedule.get_busy_slots(date)
    free = schedule.get_free_slots(date)

    print_slots(busy, "Занятые интервалы")
    print_slots(free, "Свободные интервалы")

    check = input("\nПроверить доступность интервала? (д/н): ").lower()
    if check == 'д':
        start = input("  Время начала (чч:мм): ").strip()
        end = input("  Время окончания (чч:мм): ").strip()
        available = schedule.is_available(date, start, end)
        print("Доступен" if available else "Недоступен")

    find = input("\nНайти слот заданной длительности? (д/н): ").lower()
    if find == 'д':
        minutes = int(input("  Длительность (в минутах): "))
        slot = schedule.find_available_slot(date, minutes)
        print(f"Первый подходящий слот: {slot}" if slot else "Нет подходящих слотов")