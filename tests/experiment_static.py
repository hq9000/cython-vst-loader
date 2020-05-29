class Test:
    def method_one(self):
        print("Called method_one")

    @staticmethod
    def method_two():
        print("Called method_two")

    @classmethod
    def method_three(cls):
        cls.method_two()


class T2(Test):
    @staticmethod
    def method_two():
        print("T2")


a_test = Test()
a_test.method_one()  # -> Called method_one
a_test.method_two()  # -> Called method_two
a_test.method_three()  # -> Called method_two

b_test = T2()
b_test.method_three()  # -> T2
Test.method_two()  # -> Called method_two
T2.method_three()  # -> T2
