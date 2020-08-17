import unittest
import os

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        print("setup")
        suit = unittest.TestSuite()
        loader = unittest.TestLoader()
        loader = unittest.TestLoader()
        runner = unittest.TextTestRunner()
        suit.addTest(loader.loadTestsFromModule())
        path = os.path.dirname(os.path.abspath(__file__))
        suit.addTest(loader.discover(path))



    def test01(self):
        print('test01')
        self.assertEqual(1,1)

    def test02(self):
        print('test02')
        self.assertGreaterEqual(5,4)

    def tearDown(self) -> None:
        print("teardown")

if __name__ == '__main__':
    unittest.main()