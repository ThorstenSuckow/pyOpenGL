import unittest
import time
from core.util import Util

class Test(unittest.TestCase):

    def test_getCurrentSpeed(self):
        
        current = time.time_ns()
        start = current - (4 * 10**9)

        # 20 px per second
        self.assertEqual(80, Util.getCurrentSpeed(20, 0, current, start))
        
        # no acc (=max-speed)
        self.assertEqual(80, Util.getCurrentSpeed(0, 80, current, start))
        

        pass



if __name__ == '__main__':
    unittest.main()
