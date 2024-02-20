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
import yagooglesearch

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

                # Handle long queries
                query = self._handle_long_query(query)

                proxy_index = self.proxy_rotation_index % len(self.proxies)
                proxy = self.proxies[proxy_index]
                self.proxy_rotation_index += 1

                client = yagooglesearch.SearchClient(
                    query,
                    tbs="li:1",
                    num=100,
                    max_search_result_urls_to_return=self.max_search_result_urls_to_return_per_dork,
                    proxy=proxy,
                    verify_ssl=not self.disable_verify_ssl,
                    verbosity=self.verbosity,
                )

                client.assign_random_user_agent()
                self.log.info(f"Search ( {dork_counter} / {total_dorks_to_search} ) for Google dork [ {query} ] using User-Agent '{client.user_agent}' through proxy '{proxy}'")
                dork_urls_list = client.search()

                # Remove false positives
                dork_urls_list = self._remove_false_positives(dork_urls_list)

                dork_urls_list_size = len(dork_urls_list)
                if dork_urls_list:
                    self._process_found_urls(dork, dork_urls_list, dork_urls_list_size)
                else:
                    self.log.info(f"Results: {dork_urls_list_size} URLs found for Google dork: {dork}")

            except KeyboardInterrupt:
                sys.exit(0)

            except Exception as e:
                self.log.error(f"Error with dork: {dork}.  Exception {e}")
                if type(e).__name__ == "SSLError" and (not self.disable_verify_ssl):
                    self.log.info("If you are using self-signed certificates for an HTTPS proxy, try-rerunning with the -l switch to disable verifying SSL/TLS certificates.  Exiting...")
                    sys.exit(1)

            dork_counter += 1
            if dork != self.google_dorks[-1]:
                pause_time = random.choice(self.delay_between_dork_searches_list)
                self.log.info(f"Sleeping {pause_time} seconds before executing the next dork search...")
                time.sleep(pause_time)

        self.log.info(f"Total URLs found for the {total_dorks_to_search} total dorks searched: {self.total_urls_found}")
        completion_timestamp
