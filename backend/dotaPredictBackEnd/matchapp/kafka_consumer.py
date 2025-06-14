#!/usr/bin/env python3
# Kafka Consumer - dotapredict API call to update matches

import os
import json
import logging
import requests
import time
from kafka import KafkaConsumer
from datetime import datetime

# Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
DJANGO_API_URL = os.getenv('DJANGO_API_URL', 'http://localhost:8000')
KAFKA_TOPIC = 'dota-matches-sync'
CONSUMER_GROUP = 'dota-matches-consumer'

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DjangoAPIConsumer:
    def __init__(self):
        # Attendre que Django soit prêt
        self.wait_for_django()

        # Retry connection to Kafka
        max_retries = 10
        retry_count = 0

        while retry_count < max_retries:
            try:
                self.consumer = KafkaConsumer(
                    KAFKA_TOPIC,
                    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
                    group_id=CONSUMER_GROUP,
                    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                    key_deserializer=lambda k: k.decode('utf-8') if k else None,
                    auto_offset_reset='latest',
                    enable_auto_commit=True,
                    api_version=(2, 6, 0)
                )
                logger.info(f"Connected to Kafka topic: {KAFKA_TOPIC}")
                break
            except Exception as e:
                retry_count += 1
                logger.warning(f"Failed to connect to Kafka (attempt {retry_count}/{max_retries}): {e}")
                if retry_count >= max_retries:
                    raise
                time.sleep(5)

    def wait_for_django(self):
        """Attendre que l'API Django soit disponible"""
        max_retries = 30
        retry_count = 0

        while retry_count < max_retries:
            try:
                response = requests.get(f"{DJANGO_API_URL}/admin/", timeout=5)
                logger.info("Django API is ready")
                return
            except requests.RequestException:
                retry_count += 1
                logger.info(f"Waiting for Django API... (attempt {retry_count}/{max_retries})")
                time.sleep(5)

        raise Exception("Django API not available after maximum retries")

    def call_django_api(self, event):
        """Appelle l'endpoint Django pour sauvegarder les matchs"""
        try:
            # Utilise votre endpoint existant
            url = f"{DJANGO_API_URL}/api/match/saveLiveMatches/"

            # Headers
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'DotaKafkaConsumer/1.0'
            }

            # Appel POST
            response = requests.post(url, headers=headers, timeout=60)
            response.raise_for_status()

            result = response.json()
            logger.info(
                f"Django API call successful: "
                f"created={result.get('created', 0)}, "
                f"updated={result.get('updated', 0)}, "
                f"total={result.get('total', 0)}"
            )

            return True

        except requests.exceptions.Timeout:
            logger.error("Django API call timed out")
            return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Django API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}")
                try:
                    logger.error(f"Response body: {e.response.text}")
                except:
                    pass
            return False

        except Exception as e:
            logger.error(f"Unexpected error calling Django API: {e}")
            return False

    def process_message(self, message):
        """Traite un message Kafka"""
        try:
            event = message.value
            event_type = event.get('event_type')
            timestamp = event.get('timestamp')

            logger.info(f"Processing event: type={event_type}, timestamp={timestamp}")

            if event_type == 'sync_matches':
                success = self.call_django_api(event)

                if success:
                    logger.info("Successfully processed sync event")
                else:
                    logger.error("Failed to process sync event")

            else:
                logger.warning(f"Unknown event type: {event_type}")

        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def run(self):
        """Boucle principale du consumer"""
        logger.info(f"Starting Django API Consumer for topic: {KAFKA_TOPIC}")
        logger.info(f"Django API URL: {DJANGO_API_URL}")

        try:
            for message in self.consumer:
                try:
                    self.process_message(message)
                except Exception as e:
                    logger.error(f"Error processing message: {e}")

        except KeyboardInterrupt:
            logger.info("Shutting down consumer...")
        except Exception as e:
            logger.error(f"Error in consumer loop: {e}")
        finally:
            self.consumer.close()


if __name__ == "__main__":
    consumer = DjangoAPIConsumer()
    consumer.run()