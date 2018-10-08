import unittest
import ChromeLogin as cl
import credentials
from selenium import webdriver

one = cl.VirtuAutomation(user=credentials.user,
                         password=credentials.password, driver=webdriver.Chrome("chromedriver/chromedriver.exe"))


class VirtruUnitTest(unittest.TestCase, cl.VirtuAutomation):

    def test_virtru(self):
        test1 = one.login()
        self.assertEqual(True, test1)
        print("Test 1 : Login Completed")
        one.set_sleep(12)
        test2 = one.click_mail(sender='me')
        self.assertEqual(True, test2)
        print("Test 2 : Clicked on Email completed")
        one.set_sleep(10)
        test3 = one.click_unlock_btn()
        self.assertEqual(True, test3)
        print("Test 3 : Clicked on Unlock button completed")
        one.set_sleep(12)
        test4 = one.click_virtru_user_login_btn(user=credentials.user, btn_class='userEmail')
        self.assertEqual(True, test4)
        print("Test 4 : Clicked on email id in Virtru page completed")
        one.set_sleep(2)
        # test5 = one.login_with_gmail()
        test5 = one.click_send_verification_email()
        self.assertEqual(True, test5)
        print("Test 5 : Clicked on send me verification email in virtru completed")
        # print("Test 5 : Clicked on Login me in through gmail completed")
        one.set_sleep(10)
        test6 = one.click_on_verify_mail()
        self.assertEqual(True, test6)
        print("Test 6 : Clicked on send verify email in gmail completed")
        one.set_sleep(15)
        extracted_content = one.extract_text_without_attachments()
        input_mail_text = one.read_input_mail("inputmail_attachments.txt")
        self.assertMultiLineEqual(input_mail_text, extracted_content)
        print("Test 7 : Verified extracted email content")
        test8 = len(input_mail_text)
        self.assertEqual(len(extracted_content), test8)
        print("Test 8 : Check the extracted email content size")
        test9 = one.get_result_attachments()
        self.assertEqual(2, len(test9))
        print("Test 9 : Check the attachment size")
        test10 = one.get_attached_file_names()
        input_files = ["sunset.jpg", "water.jpg"]
        self.assertCountEqual(input_files, test10)
        print("Test 10 : Check the attachment file name sizes")
        self.assertListEqual(input_files, test10)
        print("Test 11 : Check the attachment file names list")


if __name__ == "__main__":
    unittest.main()
