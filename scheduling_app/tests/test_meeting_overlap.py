import datetime

from django.test import TestCase

from scheduling_app.models import Meeting, Days


# Create your tests here.
class TestOverlappingMeeting(TestCase):
    meeting1: Meeting
    meeting2: Meeting
    def setUp(self) -> None:
        self.meeting1 = Meeting.objects.create(
            start_date='2023-01-18',
            end_date='2023-04-05',
            start_time='06:30',
            end_time='08:30',
            days='-'
        )
        self.meeting2 = Meeting.objects.create(
            start_date='2023-01-18',
            end_date='2023-04-05',
            start_time='06:30',
            end_time='08:30',
            days='-'
        )

    def setup_overlapping_dates(self):
        self.meeting1.start_date = datetime.date(year=2023, month=8, day=10)
        self.meeting1.end_date = datetime.date(year=2023, month=10, day=28)
        self.meeting2.start_date = datetime.date(year=2023, month=7, day=9)
        self.meeting2.end_date = datetime.date(year=2023, month=11, day=1)

    def setup_disjoint_dates(self):
        self.meeting1.start_date = datetime.date(year=2023, month=1, day=10)
        self.meeting1.end_date = datetime.date(year=2023, month=4, day=28)
        self.meeting2.start_date = datetime.date(year=2023, month=4, day=29)
        self.meeting2.end_date = datetime.date(year=2023, month=11, day=1)

    def setup_same_dates(self):
        self.meeting1.start_date = self.meeting2.start_date = datetime.date(year=2023, month=1, day=10)
        self.meeting1.end_date = self.meeting2.end_date = datetime.date(year=2023, month=4, day=28)

    def setup_overlapping_times(self):
        self.meeting1.start_time = datetime.time(hour=10, minute=10)
        self.meeting1.end_time = datetime.time(hour=12, minute=15)
        self.meeting2.start_time = datetime.time(hour=11, minute=30)
        self.meeting2.end_time = datetime.time(hour=13, minute=15)

    def setup_disjoint_times(self):
        self.meeting1.start_time = datetime.time(hour=10, minute=10)
        self.meeting1.end_time = datetime.time(hour=12, minute=15)
        self.meeting2.start_time = datetime.time(hour=8, minute=30)
        self.meeting2.end_time = datetime.time(hour=9, minute=15)

    def setup_same_times(self):
        self.meeting1.start_time = self.meeting2.start_time = datetime.time(hour=10, minute=10)
        self.meeting1.end_time = self.meeting2.end_time = datetime.time(hour=12, minute=15)

    def setup_overlapping_days(self):
        self.meeting1.days = 'MoWeFr'
        self.meeting2.days = 'TuWeTh'

    def setup_disjoint_days(self):
        self.meeting1.days = 'MoWeFr'
        self.meeting2.days = 'SaSu'

    def setup_same_days(self):
        self.meeting1.days = self.meeting2.days = 'SaSu'

    """
    Multiple Base Choice Coverage:
        Characteristic 1: Dates (A)
            Overlap     Same    Disjoint
        Characteristic 2: Times (B)
            Overlap     Same    Disjoint
        Characteristic 3: Days  (C)
            Overlap     Same    Disjoint
    
    Base Choices:
        BC1: A2-B3-C1
        BC2: A2-B1-C3
        BC3: A1-B2-C3
    Test Requirements:
        for BC1: A2-B3-C1
            A1-B3-C1, A3-B3-C1, A2-B1-C1, A2-B2-C1, A2-B3-C2 A2-B3-C3 
        for BC2: A2-B1-C3
            A1-B1-C3, A3-B1-C3, A2-B2-C3, A2-B3-C3, A2-B1-C1, A2-B1-C2
        for BC3: A1-B2-C3
            A2-B2-C3, A3-B2-C3, A1-B1-C3, A1-B3-B3, A1-B2-C1, A1-B2-C2
    """
    def test_BC1(self):
        self.setup_same_dates()
        self.setup_disjoint_times()
        self.setup_overlapping_days()
        self.assertFalse(self.meeting1.overlaps(self.meeting2))

    def test_A1B3C1(self):
        self.setup_overlapping_dates()
        self.setup_disjoint_times()
        self.setup_overlapping_days()
        self.assertFalse(self.meeting1.overlaps(self.meeting2))

    def test_A3B3C1(self):
        self.setup_disjoint_dates()
        self.setup_disjoint_times()
        self.setup_overlapping_days()
        self.assertFalse(self.meeting1.overlaps(self.meeting2))

    def test_A2B1C1(self):
        self.setup_same_dates()
        self.setup_overlapping_times()
        self.setup_overlapping_days()
        self.assertTrue(self.meeting1.overlaps(self.meeting2))

    def test_A2B2C1(self):
        self.setup_same_dates()
        self.setup_same_times()
        self.setup_overlapping_days()
        self.assertTrue(self.meeting1.overlaps(self.meeting2))

    def test_A2B3C2(self):
        self.setup_same_dates()
        self.setup_disjoint_times()
        self.setup_same_days()
        self.assertFalse(self.meeting1.overlaps(self.meeting2))

    def test_A2B3C3(self):
        self.setup_same_dates()
        self.setup_disjoint_times()
        self.setup_disjoint_days()
        self.assertFalse(self.meeting1.overlaps(self.meeting2))
    def test_BC2(self):
        self.setup_same_dates()
        self.setup_overlapping_times()
        self.setup_disjoint_days()
        self.assertFalse(self.meeting1.overlaps(self.meeting2))

    def test_A1B1C3(self):
        self.setup_overlapping_dates()
        self.setup_overlapping_times()
        self.setup_disjoint_days()
        self.assertFalse(self.meeting1.overlaps(self.meeting2))

    def test_A3B1C3(self):
        self.setup_disjoint_dates()
        self.setup_overlapping_times()
        self.setup_disjoint_days()
        self.assertFalse(self.meeting1.overlaps(self.meeting2))

    def test_A2B2C3(self):
        self.setup_same_dates()
        self.setup_same_times()
        self.setup_disjoint_days()
        self.assertFalse(self.meeting1.overlaps(self.meeting2))

    def test_A2B1C2(self):
        self.setup_same_dates()
        self.setup_overlapping_times()
        self.setup_same_days()
        self.assertTrue(self.meeting1.overlaps(self.meeting2))

    def test_BC3(self):
        self.setup_overlapping_dates()
        self.setup_same_times()
        self.setup_disjoint_days()
        self.assertFalse(self.meeting1.overlaps(self.meeting2))

    def test_A3B2C3(self):
        self.setup_disjoint_dates()
        self.setup_same_times()
        self.setup_disjoint_days()
        self.assertFalse(self.meeting1.overlaps(self.meeting2))

    def test_A1B3C3(self):
        self.setup_overlapping_dates()
        self.setup_disjoint_times()
        self.setup_disjoint_days()
        self.assertFalse(self.meeting1.overlaps(self.meeting2))

    def test_A1B2C1(self):
        self.setup_overlapping_dates()
        self.setup_same_times()
        self.setup_overlapping_days()
        self.assertTrue(self.meeting1.overlaps(self.meeting2))

    def test_A1B2C2(self):
        self.setup_overlapping_dates()
        self.setup_same_times()
        self.setup_same_days()
        self.assertTrue(self.meeting1.overlaps(self.meeting2))

    def test_no_days(self):
        self.setup_overlapping_dates()
        self.setup_overlapping_times()
        self.assertFalse(self.meeting1.overlaps(self.meeting2))

    def test_same_times(self):
        self.setup_overlapping_dates()
        self.setup_overlapping_days()
        self.meeting1.start_time = datetime.time(hour=0, second=0)
        self.meeting1.end_time = datetime.time(hour=0, second=0)
        self.meeting2.start_time = datetime.time(hour=0, second=0)
        self.meeting2.end_time = datetime.time(hour=0, second=0)
        self.assertTrue(self.meeting1.overlaps(self.meeting2))

    def test_get_day_set_primary_formatting1(self):
        self.meeting1.days = 'MoWeFr'
        day_set = self.meeting1.get_day_set()
        self.assertSetEqual({Days.MONDAY, Days.WEDNESDAY, Days.FRIDAY}, day_set)

    def test_get_day_set_primary_formatting2(self):
        self.meeting1.days = 'SaSuTuTh'
        day_set = self.meeting1.get_day_set()
        self.assertSetEqual({Days.SUNDAY, Days.SATURDAY, Days.TUESDAY, Days.THURSDAY}, day_set)

    def test_get_day_set_primary_formatting3(self):
        self.meeting1.days = 'TuSaFrMo'
        day_set = self.meeting1.get_day_set()
        self.assertSetEqual({Days.MONDAY, Days.TUESDAY, Days.FRIDAY, Days.SATURDAY}, day_set)

    def test_get_day_set_secondary_formatting1(self):
        self.meeting1.days = 'M,W,F'
        day_set = self.meeting1.get_day_set()
        self.assertSetEqual({Days.MONDAY, Days.WEDNESDAY, Days.FRIDAY}, day_set)

    def test_get_day_set_secondary_formatting2(self):
        self.meeting1.days = 'M,W,T,R'
        day_set = self.meeting1.get_day_set()
        print(day_set)
        self.assertSetEqual({Days.MONDAY, Days.WEDNESDAY, Days.TUESDAY, Days.THURSDAY}, day_set)

    def test_get_day_set_secondary_formatting3(self):
        self.meeting1.days = 'T,Sa,Su'
        day_set = self.meeting1.get_day_set()
        self.assertSetEqual({Days.TUESDAY, Days.SATURDAY, Days.SUNDAY}, day_set)

    def test_get_day_set_none(self):
        self.meeting1.days = '-'
        day_set = self.meeting1.get_day_set()
        self.assertSetEqual(set(), day_set)