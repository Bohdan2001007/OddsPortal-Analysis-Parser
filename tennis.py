import re
import threading
from math import nan
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class Driver:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=options)

    def __del__(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(f'Error while quitting driver: {repr(e)}')
        print('The driver has been "quitted".')

threadLocal = threading.local()

def create_driver():
    the_driver = getattr(threadLocal, 'the_driver', None)
    if the_driver is None:
        the_driver = Driver()
        setattr(threadLocal, 'the_driver', the_driver)
    return the_driver.driver

class GameData:
    def __init__(self):
        self.date = []
        self.time = []
        self.game = []
        self.score = []
        self.home_odds = []
        self.draw_odds = []
        self.away_odds = []
        self.country = []
        self.league = []

def human_like_scroll(driver, pause_time=5, max_attempts=5000, patience=10):
    html = driver.find_element(By.TAG_NAME, 'html')
    last_count = 0
    stable_iterations = 0

    for i in range(max_attempts):
        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(pause_time)
        current_count = len(driver.find_elements(By.CSS_SELECTOR, 'div[set]>div:not(:first-child)'))
        if current_count == last_count:
            stable_iterations += 1
            if stable_iterations >= patience:
                print(f"No new matches after {patience} attempts. Total: {current_count}")
                break
        else:
            stable_iterations = 0
        last_count = current_count
    return last_count


def generate_matches(pgSoup, defaultVal=nan):
    events = []

    league_containers = pgSoup.select('div.eventRow')
    for league in league_containers:
        country_elem = league.select_one('a[href*="/tennis/"] + div + a')
        league_elem = league.select_one('a[href*="/tennis/"] + div + a + div + a')
        date_elem = league.select_one('div.border-black-borders div.text-black-main')

        country = country_elem.get_text(strip=True) if country_elem else defaultVal
        league_name = league_elem.get_text(strip=True) if league_elem else defaultVal
        date = date_elem.get_text(strip=True) if date_elem else defaultVal

        match_containers = league.select('div.border-black-borders, div.group.flex')

        for evt in match_containers:
            team_elems = evt.select('a[title]')
            if len(team_elems) < 2:
                continue

            evtRow = {
                'date': date if date != defaultVal else nan,
                'country': country if country != defaultVal else nan,
                'league': league_name if league_name != defaultVal else nan,
                'time': nan,
                'game': f"{team_elems[0]['title']} – {team_elems[1]['title']}" if len(team_elems) >= 2 else nan,
                'score': nan,
                'home_odds': nan,
                'away_odds': nan
            }

            time_elem = evt.select_one('p.whitespace-nowrap, div.flex div.text-gray-dark p')
            if time_elem:
                evtRow['time'] = time_elem.get_text(strip=True)

            score_container = evt.select_one('div.text-gray-dark.relative.flex')
            if score_container:
                score_text = score_container.get_text(" ", strip=True)
                match_score = re.search(r'(\d+)\s*–\s*(\d+)', score_text)
                if match_score:
                    evtRow['score'] = f"{match_score.group(1)}:{match_score.group(2)}"

            odds_elems = evt.select('div[data-testid="add-to-coupon-button"] p.height-content')
            if len(odds_elems) >= 2:  # Для тенниса только 2 коэффициента
                evtRow['home_odds'] = odds_elems[0].get_text(strip=True)
                evtRow['away_odds'] = odds_elems[1].get_text(strip=True)

            events.append(evtRow)

    return events


def parse_data(url, return_urls=False):
    browser = create_driver()
    try:
        browser.get(url)
        total_matches = human_like_scroll(browser, pause_time=5, max_attempts=5000, patience=10)
        time.sleep(10)
        soup = bs(browser.page_source, "lxml")
        game_data = GameData()
        rows = generate_matches(soup, defaultVal=nan)
        parsed_count = len(rows)
        print(f"Parsed {parsed_count} matches for URL {url}")

        if rows:
            for row in rows:
                for k in game_data.__dict__:
                    getattr(game_data, k).append(row.get(k, nan))

        if return_urls:
            span = soup.find('span', {'class': 'next-games-date'})
            if span:
                a_tags = span.find_all('a')
                urls = ['https://www.oddsportal.com' + a_tag['href'] for a_tag in a_tags]
                return game_data, urls
            else:
                return game_data, []
        else:
            return game_data

    except Exception as e:
        print(f'Error in parse_data for {url}: {repr(e)}')
        return None


if __name__ == '__main__':
    urls_to_parse = [
        'https://www.oddsportal.com/matches/tennis/20241220/',
        'https://www.oddsportal.com/matches/tennis/20241219/',
        'https://www.oddsportal.com/matches/tennis/20241218/',
        'https://www.oddsportal.com/matches/tennis/20241217/',
        'https://www.oddsportal.com/matches/tennis/20241216/',
        'https://www.oddsportal.com/matches/tennis/20241215/',
        'https://www.oddsportal.com/matches/tennis/20241214/',
        'https://www.oddsportal.com/matches/tennis/20241213/',
        'https://www.oddsportal.com/matches/tennis/20241212/',
        'https://www.oddsportal.com/matches/tennis/20241211/',
        'https://www.oddsportal.com/matches/tennis/20241210/',
        'https://www.oddsportal.com/matches/tennis/20241209/',
        'https://www.oddsportal.com/matches/tennis/20241208/',
        'https://www.oddsportal.com/matches/tennis/20241207/',
        'https://www.oddsportal.com/matches/tennis/20241206/',
        'https://www.oddsportal.com/matches/tennis/20241205/',
        'https://www.oddsportal.com/matches/tennis/20241204/',
        'https://www.oddsportal.com/matches/tennis/20241203/',
        'https://www.oddsportal.com/matches/tennis/20241202/',
        'https://www.oddsportal.com/matches/tennis/20241201/',
        'https://www.oddsportal.com/matches/tennis/20241130/',
        'https://www.oddsportal.com/matches/tennis/20241129/',
        'https://www.oddsportal.com/matches/tennis/20241128/',
        'https://www.oddsportal.com/matches/tennis/20241127/',
        'https://www.oddsportal.com/matches/tennis/20241126/',
        'https://www.oddsportal.com/matches/tennis/20241125/',
        'https://www.oddsportal.com/matches/tennis/20241124/',
        'https://www.oddsportal.com/matches/tennis/20241123/',
        'https://www.oddsportal.com/matches/tennis/20241122/',
        'https://www.oddsportal.com/matches/tennis/20241121/',
        'https://www.oddsportal.com/matches/tennis/20241120/',
        'https://www.oddsportal.com/matches/tennis/20241119/',
        'https://www.oddsportal.com/matches/tennis/20241118/',
        'https://www.oddsportal.com/matches/tennis/20241117/',
        'https://www.oddsportal.com/matches/tennis/20241116/',
        'https://www.oddsportal.com/matches/tennis/20241115/',
        'https://www.oddsportal.com/matches/tennis/20241114/',
        'https://www.oddsportal.com/matches/tennis/20241113/',
        'https://www.oddsportal.com/matches/tennis/20241112/',
        'https://www.oddsportal.com/matches/tennis/20241111/',
        'https://www.oddsportal.com/matches/tennis/20241110/',
        'https://www.oddsportal.com/matches/tennis/20241109/',
        'https://www.oddsportal.com/matches/tennis/20241108/',
        'https://www.oddsportal.com/matches/tennis/20241107/',
        'https://www.oddsportal.com/matches/tennis/20241106/',
        'https://www.oddsportal.com/matches/tennis/20241105/',
        'https://www.oddsportal.com/matches/tennis/20241104/',
        'https://www.oddsportal.com/matches/tennis/20241103/',
        'https://www.oddsportal.com/matches/tennis/20241102/',
        'https://www.oddsportal.com/matches/tennis/20241101/',
    ]

    game_data_dfList = []

    for link in urls_to_parse:
        result = parse_data(link, False)
        if result is None:
            print(f'Error retrieving data from {link}')
        else:
            df = pd.DataFrame(result.__dict__)
            game_data_dfList.append(df)

    if game_data_dfList:
        games = pd.concat(game_data_dfList, ignore_index=True)

        games = games.drop_duplicates(
            subset=['date', 'time', 'game', 'score', 'home_odds', 'draw_odds', 'away_odds', 'country', 'league'],
            keep='first')

        games.to_csv("tennis.csv", index=False, encoding='utf-8-sig')
        print(games)
        print("output9.csv")
    else:
        print('!?NO GAMES?!')

    try:
        del threadLocal
    except Exception as e:
        print(f'Error during thread cleanup: {repr(e)}')

    import gc
    gc.collect()





























