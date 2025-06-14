#!/usr/bin/env python3
#Kafka Producer - Repetitive steam API call

import os
import time
import json
import logging
import requests
from kafka import KafkaProducer
from datetime import datetime

# Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
STEAM_API_KEY = os.getenv('STEAM_API_KEY')
SYNC_INTERVAL = int(os.getenv('SYNC_INTERVAL', 30))  # secondes
KAFKA_TOPIC = 'dota-matches-sync'

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SteamAPIProducer:
    def __init__(self):
        # Retry connection to Kafka
        max_retries = 10
        retry_count = 0

        while retry_count < max_retries:
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    key_serializer=lambda k: k.encode('utf-8') if k else None,
                    api_version=(2, 6, 0)
                )
                logger.info(f"Connected to Kafka at {KAFKA_BOOTSTRAP_SERVERS}")
                break
            except Exception as e:
                retry_count += 1
                logger.warning(f"Failed to connect to Kafka (attempt {retry_count}/{max_retries}): {e}")
                if retry_count >= max_retries:
                    raise
                time.sleep(5)

    def fetch_steam_live_matches(self):
        try:
            if not STEAM_API_KEY:
                raise ValueError("STEAM_API_KEY not configured")

            api_url = f"https://api.steampowered.com/IDOTA2Match_570/GetLiveLeagueGames/v1/?key={STEAM_API_KEY}"
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()

            data = response.json()
            matches = data.get("result", {}).get("games", [])

            logger.info(f"Fetched {len(matches)} live matches from Steam API")
            return matches

        except requests.RequestException as e:
            logger.error(f"Error fetching Steam API: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching matches: {e}")
            return []

    def send_sync_event(self):
        """Envoie un événement de synchronisation"""
        try:
            # Déclenche juste une synchronisation, pas besoin d'envoyer les données
            # Le consumer appellera l'API Django qui récupérera les données fraîches
            event = {
                'timestamp': datetime.utcnow().isoformat(),
                'event_type': 'sync_matches',
                'trigger': 'scheduled'
            }

            # Utilise timestamp comme clé pour partitioning
            key = str(int(time.time()))

            self.producer.send(
                KAFKA_TOPIC,
                key=key,
                value=event
            )

            self.producer.flush()
            logger.info("Sent sync trigger event")

        except Exception as e:
            logger.error(f"Error sending sync event: {e}")

    def run(self):
        """Boucle principale du producer"""
        logger.info(f"Starting Steam API Producer (interval: {SYNC_INTERVAL}s)")
        logger.info(f"Steam API Key configured: {'Yes' if STEAM_API_KEY else 'No'}")

        while True:
            try:
                logger.info("Triggering match synchronization...")
                self.send_sync_event()

                logger.info(f"Waiting {SYNC_INTERVAL} seconds before next sync...")
                time.sleep(SYNC_INTERVAL)

            except KeyboardInterrupt:
                logger.info("Shutting down producer...")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(10)  # Attendre avant de réessayer

        self.producer.close()


if __name__ == "__main__":
    producer = SteamAPIProducer()
    producer.run()