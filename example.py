# Standard library imports
import typing as T
import datetime
from pathlib import Path
import tempfile
import logging
from logging.handlers import RotatingFileHandler
import atexit
import sys
import time
from argparse import ArgumentParser

# Selenium-Python package imports
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException, InvalidElementStateException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class TheClub():
    def __init__(
        self, 
        credentials_filename: Path = Path("./.credentials.txt"), 
        path_to_chromedriver: Path = Path("./chromedriver")
    ):
        # logging.basicConfig(
        #     filename=Path(__file__).parent / 'logs/log.txt',
        #     filemode='w',
        #     level=logging.INFO
        # )
        self.init_logging()
        self.max_players = 4
        self.driver = self.initialize_browser(path_to_chromedriver=path_to_chromedriver)
        self.get_credentials(filename=credentials_filename)

    def init_logging(self, log_level: str = 'INFO'):
        logger = logging.getLogger('YourLogger')
        logger.setLevel(log_level)

        log_handler = logging.handlers.RotatingFileHandler(
            filename=Path(__file__).parent / 'logs/log.txt', 
            maxBytes=2048, 
            backupCount=10
        )
        log_handler.setLevel(log_level)
        logger.addHandler(log_handler)

        console = logging.StreamHandler()
        console.setLevel(log_level)
        logger.addHandler(console) 
        self.logger = logger 

    def log(self, msg: T.Any, level: str = 'info'):
        """Print out a log statement"""
        getattr(self.logger, level.lower())(msg)

    def get_credentials(self, filename: Path):
        """Load the user credentials into memory"""
        with open(filename, 'r') as f:
            self.username, self.password = f.readline().strip().split(' ')

    def initialize_browser(self, path_to_chromedriver: str):
        """Initalize the Selenium Driver for Chrome"""
        options = webdriver.ChromeOptions()
        # run in 'headless' mode
        # options.add_argument('--headless')
        # allow to run as 'root' user
        options.add_argument("--no-sandbox")
        # disabling extensions
        options.add_argument("--disable-extensions")
        # applicable to windows os only
        options.add_argument("--disable-gpu")
        # overcome limited resource problems
        options.add_argument("--disable-dev-shm-usage")
        # specify download directory
        options.add_experimental_option(
            'prefs',
            {
                'download.default_directory': tempfile.gettempdir()
            }
        )
        driver = webdriver.Chrome(
            executable_path=path_to_chromedriver,
            options=options
        )
        driver.maximize_window()
        assert isinstance(driver, RemoteWebDriver)

        # remember to close the browser when the script exits
        atexit.register(driver.close)
        return driver

    def wait_on_visible(self, xpath: str, timeout: int = 60):
        """Wait for an element to be visible"""
        try:
            resolved = WebDriverWait(self.driver, timeout=timeout).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            self.log(f'{xpath}', 'debug')
            return resolved
        except (TimeoutException, ) as ex:
            self.log(f'wait_on_visible: URL: {self.driver.current_url} unable to locate XPATH: {xpath} in timeout: {timeout}', level='error')
            raise ex
        except (NoSuchElementException, ElementNotVisibleException, InvalidElementStateException, ) as ex:
            self.log(f'wait_on_visible: URL: {self.driver.current_url} unable to locate XPATH: {xpath}', level='error')
            raise ex

    def move_to_xpath(self, xpath: str, timeout: int = 60):
        """Simulate mouse movement to a specified element"""
        try:
            resolved = self.wait_on_visible(xpath=xpath, timeout=timeout)
            action = ActionChains(self.driver)
            action.move_to_element(resolved).perform()
            return resolved
        except (TimeoutException, ) as ex:
            self.log(f'move_to_xpath: Unable to locate element: {xpath} within {timeout} seconds', level='error')
            raise ex

    def click_on_xpath(self, xpath: str, timeout: int = 60):
        """Wait for an element to be clickable, then click on it"""
        try:
            resolved = self.move_to_xpath(xpath=xpath, timeout=timeout)
            resolved = WebDriverWait(self.driver, timeout=timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            resolved.click()
            return resolved
        except (TimeoutException, ) as ex:
            self.log(f'click_on_xpath: Unable to locate element: {xpath} within {timeout} seconds', level='error')
            raise ex

    def get_element_text(self, xpath: str, timeout: int = 60) -> T.Optional[str]:
        """Extract the visible text from a given element"""
        try:
            return self.wait_on_visible(xpath=xpath, timeout=timeout).text
        except (NoSuchElementException, ElementNotVisibleException, InvalidElementStateException, ) as ex:
            return None

    def load_home_page(self, url: str = "https://theclubat12oaks.com/") -> None:
        """Make initial request to the homepage"""
        # open Selenium and load the home page
        self.driver.get(url=url)

    def login(self, ) -> None:
        """Perform a login using stored credentials"""
        # locate the login button
        resolved = self.click_on_xpath(
            xpath='//div[contains(@class, "member-login-btn")]/a'
        )

        # locate the Member Number field
        resolved = self.click_on_xpath(
            xpath='//form[contains(@class, "sign-in-form")]/fieldset//input[@type="text"]'
        )
        # type in the Member Number
        resolved.clear()
        resolved.send_keys(self.username)

        # locate the Password field
        resolved = self.click_on_xpath(
            xpath='//form[contains(@class, "sign-in-form")]/fieldset//input[@type="password"]'
        )
        # type in the password
        resolved.clear()
        resolved.send_keys(self.password)

        # click the Sign In button
        resolved = self.click_on_xpath(
            xpath='//form[contains(@class, "sign-in-form")]/div[contains(@class, "button-holder")]/button[@type="submit"]'
        )

        # verify it was successful, we should see the "Logout" button now
        resolved = self.wait_on_visible(
            xpath='//a[contains(text(), "Logout")]'
        )

    def logout(self, ) -> None:
        """Perform a logout of the site"""
        # locate the Logout button
        resolved = self.click_on_xpath(
            xpath='//a[contains(text(), "Logout")]'
        )
        
        # verify it was successful, we should see the "Login" button now
        resolved = self.wait_on_visible(
            xpath='//div[contains(@class, "member-login-btn")]/a'
        )

    def tee_time(self, ) -> None:
        """Navigate to Golf times"""
        # mouse-over the Golf menu option
        resolved = self.move_to_xpath(
            xpath='//a/span[contains(@class, "textured-nav-heading")][contains(text(), "Golf")]'
        )

        # locate the Tee Time sub-menu option
        resolved = self.click_on_xpath(
            xpath='//a/span[contains(@class, "textured-nav-unselected-item")][contains(text(), "Book a Tee Time")]'
        )

        # verify it was successful, the header should be "Tee Time"
        resolved = self.wait_on_visible(
            xpath='//h1[contains(., "Tee Time")]'
        )

    def select_date(self, desired_date: datetime.datetime) -> None:
        """Navigate to the specified date"""
        # locate calendar button
        resolved = self.click_on_xpath(
            xpath='//span[contains(@class, "ui-icon-calendar")]'
        )

        # locate the specified date
        year = desired_date.year
        month = desired_date.month
        day = desired_date.day
        # the website uses zero-based months
        resolved = self.click_on_xpath(
            xpath=f'//td[@data-handler="selectDay"][@data-month="{month-1}"][@data-year="{year}"]/a[contains(text(), "{day}")]'
        )

        # verify it was successful, the selected date should be what we clicked on
        resolved = self.wait_on_visible(
            xpath=f'//input[@readonly="readonly"][@value="{month:02}/{day:02}/{year}"]'
        )

        # verify the date is available for booking
        try:
            resolved = self.wait_on_visible(
                xpath='//label[contains(@class, "portlet-msg-alert")][contains(text(), "not open")]',
                timeout=0.2
            )
            self.log(f'{desired_date.isoformat()} is not open for Reservations', 'error')
            sys.exit(0)
        except TimeoutException:
            pass


    def locate_available_times(self, desired_times: T.List[str], players: T.List[str]) -> bool:
        """Attempt to book a specific time"""
        # locate the desired_times, in order
        for option in desired_times:
            # only look for slots which are available
            try:
                resolved = self.click_on_xpath(
                    xpath=f'//div[contains(@class, "block-available")]//div[contains(., "{option}")]//a[contains(., "Reserve")]',
                    timeout=0.2
                )
            except TimeoutException:
                self.log(f'Tee Time: {option} was not available ...', 'warning')
                continue

            if self.attempt_to_book(players=players):
                self.log(f'Successfully booked: {option}')
                return True

        self.log(f"Unable to locate any available times for specified date", 'warning')
        return False

    def attempt_to_book(self, players: T.List[str]) -> bool:
        """Enter in player information and attempt to book"""
        if len(players) > self.max_players:
            self.log(f'Site allows a maximum of {self.max_players}, but discovered {len(players)} .. only the first {self.max_players} will be added', 'warning')

        num_players = min(len(players), self.max_players)

        # select number of players
        resolved = self.click_on_xpath(
            xpath=f'//div[contains(@class, "reservation-players")][1]/div[{num_players}]'
        )

        # wait for num-players to be updated
        resolved = self.wait_on_visible(
            xpath=f'//div[contains(@class, "ui-state-active")]/span[text()="{num_players}"]'
        )

        # enter in player information
        for idx in range(0, num_players):
            self.add_player_to_time(player_name=players[idx])

        # submit booking request
        resolved = self.click_on_xpath(
            xpath='//a[contains(., "Book Now")]'
        )

        # # verify it was successful
        # resolved = self.wait_on_visible(
        #     xpath=''
        # )
        return True

    def add_player_to_time(self, player_name: str) -> None:
        """Search for the player by name, and add them to the roster"""
        if self.is_player_on_roster(player_name=player_name, timeout=0.2):
            self.log(f'Player: {player_name} is already on the roster')
            return

        # click add Member
        resolved = self.click_on_xpath(
            xpath=f'//a/i[contains(@class, "fa-plus")][1]'
        )

        # find the search field
        resolved = self.click_on_xpath(
            xpath='//input[@aria-autocomplete="listbox"][not(@disabled)]'
        )

        # send the players name to search
        resolved.clear()
        resolved.send_keys(player_name)

        # click on the desired player
        resolved = self.click_on_xpath(
            xpath=f'//li[@data-item-label="{player_name}"]'
        )

        # verify it was successful
        if not self.is_player_on_roster(player_name=player_name):
            raise RuntimeError(f'Unable to validate {player_name} is on the roster')

    def is_player_on_roster(self, player_name: str, timeout: int = 60) -> bool:
        try:
            resolved = self.wait_on_visible(
                xpath=f'//input[@value="{player_name}"]',
                timeout=timeout
            )
            return True
        except TimeoutException:
            return False

    def run(self, desired_date: datetime.datetime, desired_times: T.List[str], players: T.List[str]) -> None:
        """Orchestrate the sequence of events"""
        self.load_home_page()
        self.login()
        self.tee_time()
        self.select_date(desired_date=desired_date)
        self.locate_available_times(desired_times=desired_times, players=players)
        self.logout()


def locate_next_day_of_week(day_of_week: str) -> datetime.datetime:
    """Given a day of the week, return the next calendar date for that day"""
    # 'weekday' is zero-based starting at 0=Monday ... 7=Sunday
    if day_of_week.lower() == 'monday':
        desired_day_of_week = 0
    elif day_of_week.lower() == 'tuesday':
        desired_day_of_week = 1
    elif day_of_week.lower() == 'wednesday':
        desired_day_of_week = 2
    elif day_of_week.lower() == 'thursday':
        desired_day_of_week = 3
    elif day_of_week.lower() == 'friday':
        desired_day_of_week = 4
    elif day_of_week.lower() == 'saturday':
        desired_day_of_week = 5
    elif day_of_week.lower() == 'sunday':
        desired_day_of_week = 6
    else:
        raise ValueError(f'Unknown day of week: {day_of_week}')
        
    today = datetime.datetime.today()
    return today + datetime.timedelta(days=((desired_day_of_week-today.weekday()) % 7) or 7)


def parse_args():
    """Parse the input arguments into variable names"""
    parser = ArgumentParser(
        description='12 Oaks Golf Reservations',
        add_help=True
    )
    parser.add_argument(
        '--chromedriver_path', type=str, required=False, default='./chromedriver',
        help="Location of the downloaded ChromeDriver (default: ./chromedriver)"
    )
    parser.add_argument(
        '--credentials_filename', type=str, required=False, default='./.credentials.txt',
        help="Filename which contains the user credentials (default: ./.credentials.txt)"
    )
    parser.add_argument(
        '--day_of_week', type=str, required=False, default='Tuesday',
        help="Next day of week to search for times (default: Tuesday)"
    )
    parser.add_argument(
        '--tee_times', type=str, required=False, default='08:20',
        help='Pipe separated list of times to check (default: "08:20")'
    )
    parser.add_argument(
        '--players', type=str, required=False, default="Amor, Joe|Crovitz, Mat|Wagner, Robert|Coley, David",
        help='Pipe separated list of players to add'
    )
    return parser.parse_args()


def main(args):
    """Execute the main logic"""
    ts = locate_next_day_of_week(day_of_week=args.day_of_week)
    tt = args.tee_times.split('|')
    mp = args.players.split('|')

    obj = TheClub(
        credentials_filename=args.credentials_filename
    )

    obj.log(f'Searching Date: {ts.strftime("%Y-%m-%d")}')
    obj.log(f'For Times: {tt}')
    obj.log(f'With Members: {mp}')
    
    obj.run(
        desired_date=ts,
        desired_times=tt,
        players=mp
    )


if __name__ == "__main__":
    main(args=parse_args())
