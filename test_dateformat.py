from dateformat import ddmmyyyy_date_pattern, yyyymmdd_date_pattern, mmddyyyy_date_pattern, monthdyr_date_pattern, dmonthyr_date_pattern, yrmonthd_date_pattern
import re
import unittest

class TestDatePatterns(unittest.TestCase):

    def test_ddmmyyyy_date_pattern(self):
        # Test valid dates
        self.assertTrue(re.match(ddmmyyyy_date_pattern, '01/12/2023'))
        self.assertTrue(re.match(ddmmyyyy_date_pattern, '31-01-1999'))
        # Test invalid dates
        self.assertFalse(re.match(ddmmyyyy_date_pattern, '31/13/2023'))  # Invalid month
        self.assertFalse(re.match(ddmmyyyy_date_pattern, '99/99/9999'))  # Completely invalid date

    def test_yyyymmdd_date_pattern(self):
        # Test valid dates
        self.assertTrue(re.match(yyyymmdd_date_pattern, '2023/12/01'))
        self.assertTrue(re.match(yyyymmdd_date_pattern, '1999-01-31'))
        # Test invalid dates
        self.assertFalse(re.match(yyyymmdd_date_pattern, '2023/13/31'))  # Invalid month
        self.assertFalse(re.match(yyyymmdd_date_pattern, '2023/12/32'))  # Invalid day

    def test_mmddyyyy_date_pattern(self):
        # Test valid dates
        self.assertTrue(re.match(mmddyyyy_date_pattern, '12/31/2023'))
        self.assertTrue(re.match(mmddyyyy_date_pattern, '01-01-1999'))
        # Test invalid dates
        self.assertFalse(re.match(mmddyyyy_date_pattern, '13/31/2023'))  # Invalid month
        self.assertFalse(re.match(mmddyyyy_date_pattern, '12/32/2023'))  # Invalid day

    def test_monthdyr_date_pattern(self):
        # Test valid dates
        self.assertTrue(re.match(monthdyr_date_pattern, 'January 01, 2023'))
        self.assertTrue(re.match(monthdyr_date_pattern, 'Dec 31, 1999'))
        # Test invalid dates
        self.assertFalse(re.match(monthdyr_date_pattern, 'Jan 32, 2023'))  # Invalid day
        self.assertFalse(re.match(monthdyr_date_pattern, 'Febuary 30, 2023'))  # Invalid date for month

    def test_dmonthyr_date_pattern(self):
        # Test valid dates
        self.assertTrue(re.match(dmonthyr_date_pattern, '01 January, 2023'))
        self.assertTrue(re.match(dmonthyr_date_pattern, '31 Dec, 1999'))
        # Test invalid dates
        self.assertFalse(re.match(dmonthyr_date_pattern, '32 January, 2023'))  # Invalid day
        self.assertFalse(re.match(dmonthyr_date_pattern, '30 Febuary, 2023'))  # Invalid date for month

    def test_yrmonthd_date_pattern(self):
        # Test valid dates
        self.assertTrue(re.match(yrmonthd_date_pattern, '2023, January 01'))
        self.assertTrue(re.match(yrmonthd_date_pattern, '1999, Dec 31'))
        # Test invalid dates
        self.assertFalse(re.match(yrmonthd_date_pattern, '2023, January 32'))  # Invalid day
        self.assertFalse(re.match(yrmonthd_date_pattern, '2023, Febuary 30'))  # Invalid date for month

# Run the tests
if __name__ == '__main__':
    unittest.main()
