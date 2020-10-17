import json
import time
from getpass import getpass

from selenium import webdriver


class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class InstagramApplication:
    def __init__(self):
        self.username = ''
        self.password = ''
        self.target = ''
        self.browser = ''
        self.link = 'https://www.instagram.com'
        self.followers = []
        self.following = []
        self.not_following_back_target = []
        self.target_not_following_back = []
        self.initialize()

    def initialize(self):
        print('''
    Instagram Followers Checker
    Created by Melihşah Akın (Evasionn)
    github: https://github.com/evasionn
    email: asalyazilim@gmail.com

    ''')

        self.username = input('username: ')
        self.password = getpass(prompt='password: ')
        self.target = input('target username: ')

        # COLLECTING DATA
        try:
            self.browser = webdriver.Chrome()
        except Exception:
            print('Chrome webdriver is required. you can install it with: sudo apt install chromium-chromedriver')
            exit(1)
        self.go_instagram()
        self.login()
        self.go_profile_page()
        self.get_followers()
        self.get_following()
        self.calculate_target_not_following_back()
        self.calculate_not_following_back_target()
        self.browser.quit()

    def go_instagram(self):
        self.browser.get(self.link)
        time.sleep(2)

    def login(self):
        username_field = self.browser.find_element_by_name('username')
        password_field = self.browser.find_element_by_name('password')

        username_field.send_keys(self.username)
        password_field.send_keys(self.password)
        time.sleep(1)

        login_btn = self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')
        login_btn.click()
        time.sleep(4)

    def go_profile_page(self):
        self.browser.get(f'{self.link}/{self.target}')
        time.sleep(2)

    def scroll_down(self):
        js_scroll_down = '''
            scroll = document.querySelector(".isgrP");
            scroll.scrollTo(0, scroll.scrollHeight);
            return scroll.scrollHeight;
        '''
        previous = 0
        while True:
            last = self.browser.execute_script(js_scroll_down)
            time.sleep(0.8)
            if previous == last:
                break
            previous = last

    def get_data(self):
        self.scroll_down()
        followers = self.browser.find_elements_by_css_selector('.FPmhX.notranslate._0imsa')

        return_list = []
        for follower in followers:
            return_list.append(follower.text)

        self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button').click()
        return return_list

    def get_followers(self):
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul'
                                           '/li[2]/a').click()
        time.sleep(4)
        self.followers = self.get_data()

    def get_following(self):
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click()
        time.sleep(4)
        self.following = self.get_data()

    def print_information(self):
        print(f'''
{Color.WARNING}Target username: {self.target}
Number of people followed by {self.target}: {len(self.followers)}
Number of people {self.target} is following: {len(self.following)}
{Color.ENDC}
''')

    def print_follower_list(self):
        print(Color.OKGREEN)
        print(f'There are {len(self.followers)} people followed by {self.target} \n')
        count = 1
        for x in self.followers:
            print(f'{count} -- > {x}')
            count += 1
        print(Color.ENDC)

    def print_following_list(self):
        print(Color.OKCYAN)
        print(f'There are {len(self.following)} people {self.target} is following \n')
        count = 1
        for x in self.following:
            print(f'{count} -- > {x}')
            count += 1
        print(Color.ENDC)

    def print_target_not_following_back(self):
        print(Color.HEADER)
        print(f'There are {len(self.target_not_following_back)} people that {self.target} is not following back \n')
        count = 1
        for x in self.target_not_following_back:
            print(f'{count} -- > {x}')
            count += 1
        print(Color.ENDC)

    def print_not_following_back_target(self):
        print(Color.FAIL)
        print(f'There are {len(self.not_following_back_target)} people that are not following back {self.target} \n')
        count = 1
        for x in self.not_following_back_target:
            print(f'{count} -- > {x}')
            count += 1
        print(Color.ENDC)

    def calculate_not_following_back_target(self):
        self.not_following_back_target = [x for x in self.following if x not in self.followers]

    def calculate_target_not_following_back(self):
        self.target_not_following_back = [x for x in self.followers if x not in self.following]

    def save_data(self):
        data = {'target_username': self.target, 'follower_list': self.followers, 'following_list': self.following,
                'not_target_following_back': self.target_not_following_back,
                'not_following_back_target': self.not_following_back_target}
        with open(f'{self.target}_{int(time.time())}.json', 'w') as output_file:
            json.dump(data, output_file)


def command_list(target):
    print(f'''
{Color.OKBLUE}{Color.BOLD}You can type the number of action to run it{Color.ENDC}

{Color.BOLD}1) Print account information
2) List the people are followed by {target} 
3) List the people are following {target}
4) List the people are not following back to {target}
5) List the people are not followed back by {target}
6) Save data

type 'exit' to close application
{Color.ENDC}
''')


def main():
    try:
        app = InstagramApplication()
        command = ''
        while command != 'exit':
            command_list(app.target)
            command = input('Your choice: ')
            if command == '1':
                app.print_information()
            elif command == '2':
                app.print_following_list()
            elif command == '3':
                app.print_follower_list()
            elif command == '4':
                app.print_not_following_back_target()
            elif command == '5':
                app.print_target_not_following_back()
            elif command == '6':
                app.save_data()
            elif command != 'exit':
                print('WRONG INPUT DETECTED')
    except KeyboardInterrupt:
        print('')
        pass


if __name__ == '__main__':
    main()
