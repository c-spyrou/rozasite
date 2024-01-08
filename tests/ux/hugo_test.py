"""Hugo test suite"""
# pylint: disable=no-member
import pytest
from selenium.webdriver.support.ui import WebDriverWait \
    #  pylint: disable=import-error
from selenium.webdriver.common.by import By  # pylint: disable=import-error

DEFAULT_TIMEOUT = 15
SITENAME = "AFC Roza"


def get_default_url(url):
    """get the default URL for the site"""
    if url[-1] == "/":  # pylint: disable=no-else-return
        return url
    else:
        return url + "/"


def get_default_title():
    """Get the default title of the site"""
    return SITENAME


@pytest.mark.usefixtures("setup")
class TestHugo:
    """Class to analyse the web site"""
    def get_button_by_link_name(self, linktext):
        """get button from a specific link"""
        return self.driver.find_element(By.LINK_TEXT, linktext)

    def wait_for_page_to_load(self, url, title):
        """wait for a page to load"""
        self.driver.get(url)
        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
            lambda driver: title in self.driver.title
        )

    def load_index_page(self, url):
        """Load the index page"""
        self.wait_for_page_to_load(url, get_default_title())

    def test_index_page(self, url):
        """check the index page is configured correctly"""
        page_url = get_default_url(url)
        page_title = get_default_title()

        self.load_index_page(url)
        assert page_title == self.driver.title
        assert page_url == self.driver.current_url
        self.driver.save_screenshot("test_index_page_00.png")

    def test_journey_page(self, url):
        """check the journey page is configured correctly"""
        self.load_index_page(url)

        page_url = get_default_url(url)+"journey/"
        page_title = get_default_title() + " | Our Journey"

        our_journey = self.get_button_by_link_name("Our Journey")
        our_journey.click()

        # first_post = self.get_button_by_link_name("Rasci")
        # first_post.click()

        self.wait_for_page_to_load(page_url, page_title)

        assert page_title == self.driver.title
        assert page_url == self.driver.current_url

        # self.driver.save_screenshot("test_first_post_00.png")

    def test_squad_page(self, url):
        """check the squad page is configured correctly"""
        self.load_index_page(url)

        page_url = get_default_url(url)+"squad/"
        page_title = get_default_title() + " | Squad"

        our_journey = self.get_button_by_link_name("Squad")
        our_journey.click()

        # first_post = self.get_button_by_link_name("Rasci")
        # first_post.click()

        self.wait_for_page_to_load(page_url, page_title)

        assert page_title == self.driver.title
        assert page_url == self.driver.current_url

        # self.driver.save_screenshot("test_first_post_00.png")

    def test_table_page(self, url):
        """check the league table page is configured correctly"""
        self.load_index_page(url)

        page_url = get_default_url(url)+"table/"
        page_title = get_default_title() + " | League Table"

        our_journey = self.get_button_by_link_name("League Table")
        our_journey.click()

        # first_post = self.get_button_by_link_name("Rasci")
        # first_post.click()

        self.wait_for_page_to_load(page_url, page_title)

        assert page_title == self.driver.title
        assert page_url == self.driver.current_url

        # self.driver.save_screenshot("test_first_post_00.png")

    def test_fixtures_page(self, url):
        """check the league table page is configured correctly"""
        self.load_index_page(url)

        page_url = get_default_url(url)+"fixtures/"
        page_title = get_default_title() + " | Fixtures & Results"

        our_journey = self.get_button_by_link_name("Fixtures & Results")
        our_journey.click()

        # first_post = self.get_button_by_link_name("Rasci")
        # first_post.click()

        self.wait_for_page_to_load(page_url, page_title)

        assert page_title == self.driver.title
        assert page_url == self.driver.current_url

        # self.driver.save_screenshot("test_first_post_00.png")