import unittest
from schedule import Schedule

mock_data = {
    "days": [
        {"id": 1, "date": "2025-07-11", "start": "09:00", "end": "17:00"},
        {"id": 2, "date": "2025-07-12", "start": "10:00", "end": "18:00"},
    ],
    "timeslots": [
        {"id": 1, "day_id": 1, "start": "09:00", "end": "10:30"},
        {"id": 2, "day_id": 1, "start": "12:00", "end": "13:00"},
        {"id": 3, "day_id": 1, "start": "15:00", "end": "16:00"},
        {"id": 4, "day_id": 2, "start": "11:00", "end": "12:30"},
]
}


class TestSchedule(unittest.TestCase):
    def setUp(self):

        self.schedule = Schedule(mock_data)

    def test_get_day_schedule_exists(self):
        day = self.schedule.get_day_schedule("2025-07-11")
        self.assertIsNotNone(day)
        self.assertEqual(day['id'], 1)

    def test_get_day_schedule_not_exists(self):
        day = self.schedule.get_day_schedule("2025-07-13")
        self.assertIsNone(day)

    def test_get_busy_slots(self):
        busy = self.schedule.get_busy_slots("2025-07-11")
        self.assertEqual(len(busy), 3)
        self.assertEqual(busy[0].start.strftime("%H:%M"), "09:00")
        self.assertEqual(busy[1].end.strftime("%H:%M"), "13:00")

    def test_get_busy_slots_empty(self):
        busy = self.schedule.get_busy_slots("2025-07-13")
        self.assertEqual(busy, [])

    def test_get_free_slots(self):
        free = self.schedule.get_free_slots("2025-07-11")
        expected = [("10:30", "12:00"), ("13:00", "15:00"), ("16:00", "17:00")]
        free_times = [(slot.start.strftime("%H:%M"), slot.end.strftime("%H:%M")) for slot in free]
        self.assertEqual(free_times, expected)

    def test_is_available_true(self):
        self.assertTrue(self.schedule.is_available("2025-07-11", "10:30", "11:30"))

    def test_is_available_false(self):
        self.assertFalse(self.schedule.is_available("2025-07-11", "08:00", "09:00"))

    def test_find_available_slot(self):
        slot = self.schedule.find_available_slot("2025-07-11", 90)  # 90 минут
        self.assertIsNotNone(slot)
        self.assertEqual(slot.start.strftime("%H:%M"), "10:30")
        self.assertEqual(slot.end.strftime("%H:%M"), "12:00")

    def test_find_available_slot_none(self):
        slot = self.schedule.find_available_slot("2025-07-11", 180)  # 3 часа
        self.assertIsNone(slot)


if __name__ == "__main__":
    unittest.main()