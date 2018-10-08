import os
import time
import logging


class VirtuAutomation():
    """Login to gmail with valid username and password"""

    def __init__(self, user, password, driver):
        logging.basicConfig(filename='log_vitru_automation.txt', level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        # my username
        self.user = user
        # my password
        self.password = password
        # Providing chrome webdriver path
        self.driver = driver
        # self.driver.implicitly_wait(15)  # seconds
        self.driver.maximize_window()

    def click_function_by_id(self, value=None):
        '''
        Use this function when the link or button is accessable with Html ID
        :param value: Pass the html ID of link or button
        :return: Opens the page / do the action of button you clicked on
        '''
        self.driver.find_element_by_id(value).click()

    def click_function_by_xpath(self, value=None):
        '''
        Use this function when the link or button is not accessable with Html ID
        :param value: Pass the valid xpath of the link or button
        :return: Opens the page / do the action of button you clicked on
        '''
        self.driver.find_element_by_xpath(value).click()

    def click_function_by_class(self, value=None):
        '''
        Use this function when the link or button is not accessable with Html ID
        :param value: Pass the valid xpath of the link or button
        :return: Opens the page / do the action of button you clicked on
        '''
        self.driver.find_elements_by_class_name(value).click()

    def login(self):
        # Open gmail.com
        self.driver.get("http://www.gmail.com")
        # Enter username
        element = self.driver.find_element_by_id("identifierId")
        element.send_keys(self.user)
        # Click on the next button to enter password
        self.driver.find_element_by_xpath("//*[@id='identifierNext']/content/span").click()
        time.sleep(5)  # 5 seconds of sleep time
        # Enter the passowrd
        element1 = self.driver.find_element_by_xpath("//*[@id='password']/div[1]/div/div[1]/input")
        element1.send_keys(self.password)
        time.sleep(1)
        # Click on the submit button to login
        self.driver.find_element_by_xpath("//*[@id='passwordNext']/content/span").click()
        return True

    def get_recent_email(self, sender):
        """ Get the latest mails - reverse the mail list and find the first mail by sender """
        last_recent_email = []
        email_elements = self.driver.find_elements_by_xpath("//*[@class='yW']/span")
        reversed_elem = reversed(email_elements)
        for e in reversed_elem:
            if sender in e.text:
                last_recent_email = e
        return last_recent_email

    def click_mail(self, sender):
        """get the most recent email with name of the sender - used to avoid checking all the mails"""
        recent_mail = self.get_recent_email(sender)  # one.get_recent_email(sender)
        # logging.debug('Clicking on the mail with sender name ' + recent_mail.text)
        recent_mail.click()
        return True

    def click_unlock_btn(self):
        """ Click on encrypted email """
        logging.debug('Clicking on the unlock button')
        xpath = "//a[contains(@style,'color:#ffffff;font-family:Helvetica,Arial,sans-serif;font-size:22px;" \
                "font-weight:lighter;text-decoration:none;display:inline-block;border-radius:2px;" \
                "padding-top:15px;padding-right:18px;padding-bottom:15px;padding-left:18px;border:1px solid #4585ff')]"
        # self.driver.find_element_by_xpath().click(xpath)
        self.click_function_by_xpath(value=xpath)
        return True

    def get_virtu_btns_by_class(self, btn_class):
        """ Change the context to the active tab where user is present """
        # -1 always switches the context to new tab to virtu website
        self.driver.switch_to.window(self.driver.window_handles[-1])
        # get the buttons with the class userEmail
        logging.debug("Fetching Virtu Btns ")
        # javascript can also be used to get elements - we can execute js in selenium also
        # login_btns = self.driver.execute_script("return document.getElementsByClassName('" + btn_class + "')")
        login_btns = self.driver.find_elements_by_class_name(btn_class)
        return login_btns

    def click_virtru_user_login_btn(self, user, btn_class):
        """ Click the button that matches the email id of the user """
        try:
            page_btns = self.get_virtu_btns_by_class(btn_class=btn_class)
            logging.debug('clicking on the select email')
            # get the index of the buttons by their class
            # click on the button based on their text values
            for i in range(len(page_btns)):
                logging.debug(page_btns[i].text)
                if user in page_btns[i].text:  # loginBtn = i
                    # click the first or second button in virtu page based on their text
                    self.driver. \
                        execute_script("document.getElementsByClassName('" + btn_class + "')[" + str(i) + "].click()")
        except:
            pass
            logging.debug("*********")
        return True

    def login_with_gmail(self):
        # Click on the login with gmail button on virtru website
        self.click_virtru_user_login_btn(user='LOGIN WITH', btn_class='oauthButton')
        logging.debug('Clicked on Login with Google')
        time.sleep(5)
        return True

    def click_send_verification_email(self):
        # click on Send me an email button
        self.click_virtru_user_login_btn(user='SEND ME AN EMAIL', btn_class='sendEmailButton')
        logging.debug('Clicked on send email')
        self.set_sleep(3)
        logging.debug('Closing virtu tab')
        # close the vitu tab and go to gmail
        self.close_tab()
        # switch the context to old tab - gmail
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.set_sleep(1)
        # go back to gmail page from the mail
        self.driver.execute_script("window.history.go(-1)")
        logging.debug('Back to gmail')
        return True

    def click_on_verify_mail(self):
        # get the latest mail with the sender name verify
        self.click_mail(sender='verify')
        self.set_sleep(5)
        # get the last email with dots in the loop if present
        dot_img = self.driver. \
            find_elements_by_xpath("//img[@src='//ssl.gstatic.com/ui/v1/icons/mail/images/cleardot.gif']")
        dot_img_len = len(dot_img)

        if (dot_img_len > 0):
            img_index = dot_img_len - 1
            # click on the last email
            dot_img[img_index].click()
            self.set_sleep(2)
        # click on the verify me button
        self.click_function_by_xpath("//a[contains(.,'VERIFY ME')]")
        # -1 always switches the context to new tab to virtu
        # switch the context to new virtu website again
        self.driver.switch_to.window(self.driver.window_handles[-1])
        return True

    def get_decrypted_text(self):
        # Get the decrypted text along with the attachment names(if any)
        logging.debug("In get encrypted string")
        textSpan = self.driver.find_elements_by_xpath("//span[@id='tdf-body']/div[1]")
        decrypted_result = ''
        for li in textSpan:
            decrypted_result = li.text
        return decrypted_result

    def get_result_attachments(self):
        # Returns the list of attachments inside decrypted list
        has_attachements = self.driver.find_elements_by_class_name("virtru-attachment")
        # has_attachement_len = len(has_attachements)
        attachments_text = []
        for i in has_attachements:
            attachments_text.append(i.text)
        # logging.debug('done')
        return attachments_text

    def get_string_diff(self, string1, string2):
        # Used to replace the attachment names in the encrypted text with blank value
        string1 = string1.replace(string2, '')
        return string1

    def extract_text_without_attachments(self):
        # remove all attachments names from decrypted text and return only the decrypted message
        text1 = self.get_decrypted_text()
        attached = self.get_result_attachments()
        extracted_string = ''
        for i in attached:
            text1 = self.get_string_diff(text1, i)
        return text1.rstrip()

    def set_sleep(self, seconds):
        # set the time to sleep for the page to load
        time.sleep(seconds)

    def page_has_loaded(self):
        # check if the page has loaded completely by checing the ready state
        self.log.info("Checking if {} page is loaded.".format(self.driver.current_url))
        page_state = self.driver.execute_script('return document.readyState;')
        return page_state == 'complete'

    def read_input_mail(self, file_name):
        # Used for reading the text within input email
        with open(file_name) as f:
            return f.read()

    def get_attached_file_info(self):
        # Used to retrieve the information of the attached file
        attached = self.get_result_attachments()
        attached_file_data = []
        for i in range(len(attached)):
            split_attached = attached[i].split(" (")
            name_with_tdf = split_attached[0]
            file_name = name_with_tdf.split("\n")[0]
            file_size = split_attached[1].split(")")[0]
            file_info = {'file_name': file_name, 'file_size': file_size}
            attached_file_data.append(file_info)
        return attached_file_data

    def get_attached_file_names(self):
        # Returns the file names of all the attachments without .pdf extension
        attached = self.get_result_attachments()
        attached_file_data = []
        for i in range(len(attached)):
            split_attached = attached[i].split(" (")
            name_with_tdf = split_attached[0]
            file_name = name_with_tdf.split("\n")[0]
            file_size = split_attached[1].split(")")[0]
            file_info = {'file_name': file_name, 'file_size': file_size}
            attached_file_data.append(file_name)
        return attached_file_data

    def get_file_size(self, path):
        # Getting the file size
        return os.path.getsize(path)

    def bytesto(bytes, to, bsize=1024):
        # Convert the file size from bytes to mb

        a = {'k': 1, 'm': 2, 'g': 3, 't': 4, 'p': 5, 'e': 6}
        r = float(bytes)
        for i in range(a[to]):
            r = r / bsize

        return (r)

    def close_tab(self):
        # close the current tab
        self.driver.close()
