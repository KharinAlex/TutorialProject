from django.test import LiveServerTestCase
from django.shortcuts import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class AccountTestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(AccountTestCase, self).setUp()
        self.navbar = {'profile': None, 'home': None, 'news': None, 'about': None, 'signin': None}

    def tearDown(self):
        self.selenium.quit()
        super(AccountTestCase, self).tearDown()

    def find_elements(self):
        selenium = self.selenium

        self.navbar['profile'] = selenium.find_element_by_class_name('navbar-brand')
        self.navbar['home'] = selenium.find_element_by_partial_link_text('Home')
        self.navbar['news'] = selenium.find_element_by_partial_link_text('News')
        self.navbar['about'] = selenium.find_element_by_partial_link_text('About us')
        self.navbar['signin'] = selenium.find_element_by_class_name('navbar-btn')

    def test_navbar(self):
        selenium = self.selenium

        self.assertIsNotNone(selenium)
        selenium.get('http://127.0.0.1:8000')
        #find elements
        self.find_elements()

        self.assertIsNotNone(self.navbar['profile'])
        self.assertIsNotNone(self.navbar['home'])
        self.assertIsNotNone(self.navbar['news'])
        self.assertIsNotNone(self.navbar['about'])
        self.assertIsNotNone(self.navbar['signin'])
        
        self.navbar['home'].click()
        self.assertEqual('http://127.0.0.1:8000/home/', selenium.current_url)
        self.find_elements()
        self.navbar['news'].click()
        self.assertEqual('http://127.0.0.1:8000/news/', selenium.current_url)
        self.find_elements()
        self.navbar['about'].click()
        self.assertEqual('http://127.0.0.1:8000/about/', selenium.current_url)