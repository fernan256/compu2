import threading
import time

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import app.flask_app
from app.models import Recitals
from app.services import services
from utils import common_utils
from .scraper_indihoy import scrap_indihoy
from .scraper_livepass import scrap_livepass
from .scraper_songkick import scrap_songkick
from .scraper_tu_entrada import scrap_tu_entrada


class ScraperManager:
    def __init__(self):
        self.scrapers = [scrap_indihoy, scrap_livepass, scrap_songkick, scrap_tu_entrada]
        self.scraper_names = {
            scrap_indihoy: "scrap_indihoy",
            scrap_livepass: "scrap_livepass",
            scrap_songkick: "scrap_songkick",
            scrap_tu_entrada: "scrap_tu_entrada",
        }
        self.lock = threading.Lock()
        self.duplicate_count = 0
        self.saved_count = 0


    def run_scraper(self, scraper, scraper_name):
        try:
            result = scraper()
            with self.lock:
                services.remove_old_events()
                self.is_duplicate_and_save_to_database(result)
            print(f"Thread {scraper_name} completed scraping.")
        except Exception as e:
            print(f"Error scraping with {scraper.__name__}: {e}")


    def is_duplicate_and_save_to_database(self, result):
        with app.flask_app.app_context():
            for event in result:
                date_to_save = event['date']
                if date_to_save != 'Date not available':
                    event_date = date_to_save
                    formatted_date = date_to_save
                else:
                    event_date = None
                    formatted_date = 'Date not available'

                exists = Recitals.query.filter_by(
                    artist=event['artist'],
                    date=event_date,
                    date_string=formatted_date,
                    venue=event['venue'],
                    link=event['link'],
                ).first()
                if exists:
                    self.duplicate_count += 1
                    continue
                else:
                    self.save_to_database(event)


    def save_to_database(self, data):
        with app.flask_app.app_context():
            date_to_save = data['date']
            if date_to_save != 'Date not available':
                event_date = data['date']
                formatted_date = date_to_save
            else:
                event_date = None
                formatted_date = 'Date not available'

            services.add_recital(
                artist=data['artist'],
                date=event_date,
                date_string=formatted_date,
                venue=data['venue'],
                link=data['link']
            )
            self.saved_count += 1

        return True

        
    def trigger_scrapers(self, max_workers=4):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            scraper_functions = set(self.scraper_names.keys())
            for scraper_func in scraper_functions:
                scraper_name = self.scraper_names[scraper_func]
                executor.submit(self.run_scraper, scraper_func, scraper_name)


    def run(self):
        print(f"Running scrapers at {datetime.now()}")
        common_utils.log_queue.put(f"Running scrapers at {datetime.now()}")
        print(f"Total active threads before scraping: {threading.active_count()}")
        common_utils.log_queue.put(f"Total active threads before scraping: {threading.active_count()}")
        self.trigger_scrapers()
        print(f"Scraping completed. Duplicates found: {self.duplicate_count}")
        common_utils.log_queue.put(f"Scraping completed. Duplicates found: {self.duplicate_count}")
        print(f"Events saved to database: {self.saved_count}")
        common_utils.log_queue.put(f"Events saved to database: {self.saved_count}")
