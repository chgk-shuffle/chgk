import unittest
import results_input

class TestStringMethods(unittest.TestCase):

    def test1(self):
        for i in range(1, 1000):
            for j in range(1, 100):
                a = results_input.foo(i, j)
                b = max(a) - min(a)
                self.assertLessEqual(b, 2)

    def test2(self):
        gl_maxx_dif = 0
        for i in range(30, 150):
            for j in range(4, 9):
                a = results_input.foo(i, j)
                maxx = max(a)
                minn = min(a)
                gl_maxx_dif = max(j - minn, j - maxx, gl_maxx_dif)
                if max(j - minn, j - maxx) > 1:
                    print(">1 ---- " + str(i) + " " + str(j))
                if max(j - minn, j - maxx) > 2:
                    print(">2 ---- " + str(i) + " " + str(j))
        self.assertLessEqual(gl_maxx_dif, 2)


if __name__ == '__main__':
    unittest.main()
