#!/usr/bin/env python

import argparse
import datetime
import json
import logging
import os
import random
import re
import sys
import time
from GoogleSerarch import GoogleSearch  # Import GoogleSearch module

__version__ = "2.6.1"

class Pagodo:
    """Pagodo class object"""

    def __init__(
        self,
        google_dorks_file,
        domain="",
        max_search_result_urls_to_return_per_dork=100,
        save_pagodo_results_to_json_file=None,
        proxies="",
        save_urls_to_file=None,
        minimum_delay_between_dork_searches_in_seconds=37,
        maximum_delay_between_dork_searches_in_seconds=60,
        disable_verify_ssl=False,
        verbosity=4,
        specific_log_file_name="pagodo.py.log",
    ):
        """Initialize Pagodo class object."""

        # Logging
        self.log = logging.getLogger("pagodo")
        log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)s] %(message)s")

        # Setup file logging.
        log_file_handler = logging.FileHandler(specific_log_file_name)
        log_file_handler.setFormatter(log_formatter)
        self.log.addHandler(log_file_handler)

        # Setup console logging.
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        self.log.addHandler(console_handler)

        # Assign log level.
        self.verbosity = verbosity
        self.log.setLevel((6 - self.verbosity) * 10)

        # Run parameter checks.
        self._validate_params(google_dorks_file, minimum_delay_between_dork_searches_in_seconds, 
                              maximum_delay_between_dork_searches_in_seconds, max_search_result_urls_to_return_per_dork)

        # All passed parameters look good, assign to the class object.
        self.google_dorks_file = google_dorks_file
        self.google_dorks = self._load_dorks(google_dorks_file)
        self.domain = domain
        self.max_search_result_urls_to_return_per_dork = max_search_result_urls_to_return_per_dork
        self.save_pagodo_results_to_json_file = self._generate_filename(save_pagodo_results_to_json_file, ".json")
        self.proxies = proxies.strip().strip(",").split(",")
        self.save_urls_to_file = self._generate_filename(save_urls_to_file, ".txt")
        self.minimum_delay_between_dork_searches_in_seconds = minimum_delay_between_dork_searches_in_seconds
        self.maximum_delay_between_dork_searches_in_seconds = maximum_delay_between_dork_searches_in_seconds
        self.disable_verify_ssl = disable_verify_ssl

        # Generate list of random delay values.
        self.delay_between_dork_searches_list = self._generate_delay_list()

        self.total_urls_found = 0
        self.proxy_rotation_index = 0

    def _validate_params(self, google_dorks_file, min_delay, max_delay, max_urls):
        if not os.path.exists(google_dorks_file):
            print("Specify a valid file containing Google dorks with -g")
            sys.exit(0)
        if min_delay < 0 or max_delay < 0 or max_delay <= min_delay:
            print("Invalid delay parameters.")
            sys.exit(0)
        if max_urls < 0:
            print("max_search_result_urls_to_return_per_dork (-m) must be greater than 0")
            sys.exit(0)

    def _load_dorks(self, dorks_file):
        dorks = []
        with open(dorks_file, "r", encoding="utf-8") as fh:
            for line in fh.read().splitlines():
                if line.strip():
                    dorks.append(line)
        return dorks

    def _generate_filename(self, filename, default_extension):
        if filename is None:
            base_name = f'pagodo_results_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}'
            return f"{base_name}{default_extension}"
        return filename

    def _generate_delay_list(self):
        return sorted([round(random.uniform(self.minimum_delay_between_dork_searches_in_seconds,
                                            self.maximum_delay_between_dork_searches_in_seconds), 1)
                       for _ in range(20)])

    def _handle_long_query(self, query):
        if len(query.split(" ")) > 32:
            ignored_string = " ".join(query.split(" ")[32:])
            self.log.warning(
                "Google limits queries to 32 words (separated by spaces):  Removing from search query: "
                f"'{ignored_string}'"
            )
            updated_query = " ".join(query.split(" ")[:32])
            if query.endswith('"'):
                updated_query = f'{updated_query}"'
            self.log.info(f"New search query: {updated_query}")
            return updated_query
        return query

    def _remove_false_positives(self, urls_list):
        ignore_url_list = [
            "https://www.kb.cert.org",
            "https://www.exploit-db.com/",
            "https://twitter.com/ExploitDB/",
        ]
        return [url for url in urls_list if not any(re.search(ignore_url, url, re.IGNORECASE) for ignore_url in ignore_url_list)]

    def _process_found_urls(self, dork, urls_list, urls_list_size):
        self.log.info(f"Results: {urls_list_size} URLs found for Google dork: {dork}")
        dork_urls_list_as_string = "\n".join(urls_list)
        self.log.info(f"dork_urls_list:\n{dork_urls_list_as_string}")
        self.total_urls_found += urls_list_size

        if self.save_urls_to_file:
            with open(self.save_urls_to_file, "a") as fh:
                fh.write(f"# {dork}\n")
                for url in urls_list:
                    fh.write(f"{url}\n")
                fh.write("#" * 50 + "\n")

        self.pagodo_results_dict["dorks"][dork] = {
            "urls_size": urls_list_size,
            "urls": urls_list,
        }

    def go(self):
        """Start pagodo Google dork search."""
        initiation_timestamp = datetime.datetime.now().isoformat()
        self.log.info(f"Initiation timestamp: {initiation_timestamp}")
        dork_counter = 1
        total_dorks_to_search = len(self.google_dorks)
        self.pagodo_results_dict = {
            "dorks": {},
            "initiation_timestamp": initiation_timestamp,
            "completion_timestamp": "",
        }

        for dork in self.google_dorks:
            self.pagodo_results_dict["dorks"][dork] = {"urls_size": 0, "urls": []}
            try:
                dork = dork.strip()
                if self.domain:
                    query = f"site:{self.domain} {dork}"
                else:
                    query = dork

                query = self._handle_long_query(query)

                proxy_index = self.proxy_rotation_index % len(self.proxies)
                proxy = self.proxies[proxy_index]
                self.proxy_rotation_index += 1

                client = GoogleSearch(
                    query,
                    num_results=self.max_search_result_urls_to_return_per_dork,
                   
