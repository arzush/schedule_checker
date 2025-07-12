import requests
from datetime import datetime, timedelta
from typing import List, Optional, Dict


class TimeSlot:
    def __init__(self, start: str, end: str):
        self.start = datetime.strptime(start, "%H:%M")
        self.end = datetime.strptime(end, "%H:%M")
        if self.end <= self.start:
            raise ValueError("End time must be after start time")

    def overlaps(self, other: 'TimeSlot') -> bool:
        return self.start < other.end and other.start < self.end

    def duration(self) -> timedelta:
        return self.end - self.start

    def contains(self, other: 'TimeSlot') -> bool:
        return self.start <= other.start and self.end >= other.end

    def __repr__(self):
        return f"{self.start.strftime('%H:%M')} - {self.end.strftime('%H:%M')}"


class Schedule:
    def __init__(self, data: Dict):
        self.days = data.get('days', [])
        self.timeslots = data.get('timeslots', [])

    def get_day_schedule(self, date: str) -> Optional[Dict]:
        return next((day for day in self.days if day['date'] == date), None)

    def get_busy_slots(self, date: str) -> List[TimeSlot]:
        day = self.get_day_schedule(date)
        if not day:
            return []
        return [TimeSlot(ts['start'], ts['end']) for ts in self.timeslots if ts['day_id'] == day['id']]

    def get_free_slots(self, date: str) -> List[TimeSlot]:
        day = self.get_day_schedule(date)
        if not day:
            return []

        work_start = datetime.strptime(day["start"], "%H:%M")
        work_end = datetime.strptime(day["end"], "%H:%M")

        busy_slots = sorted(self.get_busy_slots(date), key=lambda slot: slot.start)
        free_slots = []
        current = work_start

        for slot in busy_slots:
            if slot.start > current:
                free_slots.append(TimeSlot(current.strftime("%H:%M"), slot.start.strftime("%H:%M")))
            current = max(current, slot.end)

        if current < work_end:
            free_slots.append(TimeSlot(current.strftime("%H:%M"), work_end.strftime("%H:%M")))

        return free_slots

    def is_available(self, date: str, start: str, end: str) -> bool:
        try:
            request_slot = TimeSlot(start, end)
        except ValueError:
            return False

        for free in self.get_free_slots(date):
            if free.contains(request_slot):
                return True
        return False

    def find_available_slot(self, date: str, duration_minutes: int) -> Optional[TimeSlot]:
        duration = timedelta(minutes=duration_minutes)
        for slot in self.get_free_slots(date):
            if slot.duration() >= duration:
                new_end = (slot.start + duration).strftime("%H:%M")
                return TimeSlot(slot.start.strftime("%H:%M"), new_end)
        return None


def fetch_schedule(url: str = "https://ofc-test-01.tspb.su/test-task/") -> Dict:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

