from django.test import TestCase

# NOTE: We usually don't use these print statements inside functions. This is only for
# knowledge purposes of this tutorial, to see the class behaviour.

# class YourTestClass(TestCase):
#     @classmethod
#     def setUpTestData(self):
#         print("setUpTestData: Run once to set up non-modified data for all class methods.")
#         pass

#     def setUp(self):
#         print("setUp: Run once for every test method to setup clean data.")
#         pass

#     def test_false_is_false(self):
#         print("Method: test_false_is_false.")
#         self.assertFalse(False)

#     def test_false_is_true(self):
#         print("Method: test_false_is_true.")
#         self.assertTrue(False)

#     def test_one_plus_one_equals_two(self):
#         print("Method: test_one_plus_one_equals_two.")
#         self.assertEqual(1 + 1, 2)

    # def tearDown(self):
    #     # Clean up run after every test method.
    #     pass
