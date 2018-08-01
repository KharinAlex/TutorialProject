from django.test import LiveServerTestCase
from selenium import webdriver


class NavBarTestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(NavBarTestCase, self).setUp()
        self.navbar = {'profile': None, 'home': None, 'news': None, 'about': None, 'signin': None}

    def tearDown(self):
        self.selenium.quit()
        super(NavBarTestCase, self).tearDown()

    def find_elements(self):
        selenium = self.selenium

        self.navbar['profile'] = selenium.find_element_by_class_name('navbar-brand')
        self.navbar['home'] = selenium.find_element_by_partial_link_text('Home')
        self.navbar['news'] = selenium.find_element_by_partial_link_text('News')
        self.navbar['about'] = selenium.find_element_by_partial_link_text('About us')
        self.navbar['media'] = selenium.find_element_by_partial_link_text('Media')
        self.navbar['signin'] = selenium.find_element_by_class_name('navbar-btn')

    def test_navbar(self):
        selenium = self.selenium

        self.assertIsNotNone(selenium)
        selenium.get('http://127.0.0.1:8000')

        self.find_elements()

        self.assertIsNotNone(self.navbar['profile'])
        self.assertIsNotNone(self.navbar['home'])
        self.assertIsNotNone(self.navbar['news'])
        self.assertIsNotNone(self.navbar['media'])
        self.assertIsNotNone(self.navbar['about'])
        self.assertIsNotNone(self.navbar['signin'])

        self.navbar['home'].click()
        self.assertEqual('http://127.0.0.1:8000/home/', selenium.current_url)

        self.find_elements()
        self.navbar['news'].click()
        self.assertEqual('http://127.0.0.1:8000/news/', selenium.current_url)

        self.find_elements()
        self.navbar['media'].click()
        self.assertEqual('http://127.0.0.1:8000/media/', selenium.current_url)

        self.find_elements()
        self.navbar['about'].click()
        self.assertEqual('http://127.0.0.1:8000/about/', selenium.current_url)

        prev_url = selenium.current_url
        self.find_elements()
        self.navbar['profile'].click()
        self.assertEqual(prev_url, selenium.current_url)

        self.find_elements()
        self.navbar['signin'].click()
        self.assertEqual('http://127.0.0.1:8000/auth/login/', selenium.current_url)

        username = selenium.find_element_by_name('username')
        password = selenium.find_element_by_name('password')
        login = selenium.find_element_by_name('signin')
        regist = selenium.find_element_by_name('registr')

        self.assertIsNotNone(username)
        self.assertIsNotNone(password)
        self.assertIsNotNone(login)
        self.assertIsNotNone(regist)

        username.send_keys('testuser1')
        password.send_keys('qwerty123')

        login.click()
        self.assertEqual('http://127.0.0.1:8000/', selenium.current_url)
        self.find_elements()
        self.assertEqual(self.navbar['signin'].text, 'Log out')

        self.navbar['profile'].click()
        self.assertEqual('http://127.0.0.1:8000/auth/profile/', selenium.current_url)

        selenium.get('http://127.0.0.1:8000')

        self.find_elements()
        self.navbar['signin'].click()
        self.assertEqual('http://127.0.0.1:8000/', selenium.current_url)

        self.find_elements()
        self.assertEqual(self.navbar['signin'].text, 'Sign In')