import os
import json
import sys
import uuid
from datetime import datetime
import logging
from utils.logger import setup_logger

ENV = os.getenv("ENV")

APP_NAME = "distributed-python"
CONTAINER_ID = str(uuid.uuid1())

#LOGGING

LOGGING_LEVEL = logging.INFO

log_file_name = 'logs_{}_{}.log'.format(CONTAINER_ID, datetime.now().strftime('%Y_%m_%d'))
heartbeat_log_file_name = 'logs_heartbeat_{}_{}.log'.format(CONTAINER_ID, datetime.now().strftime('%Y_%m_%d'))
create_log_directory()

if ENV == "production":
    MONGO_JOB_COLLECTION = "jobs"
    MONGO_JOB_META_COLLECTION = "job_meta"
    MONGO_JOB_DB = "task_meta_prod"
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_QUEUE_NAME = "jobqueue"
    MONGODB_URI = 'mongodb://admin:admin@localhost:27017/task_meta_prod'
    logger = setup_logger('APP_NAME', '/data/logs/production/{}'.format(log_file_name))

elif ENV == "staging":
    MONGO_JOB_COLLECTION = "jobs"
    MONGO_JOB_DB = "task_meta_staging"
    CELERY_BROKER_URL = 'redis://localhost:6379/2'
    CELERY_QUEUE_NAME = "jobqueue"
    MONGODB_URI = 'mongodb://admin:admin@localhost:27017/task_meta_staging'
    logger = setup_logger('APP_NAME', './data/logs/staging/{}'.format(log_file_name))

elif ENV == "dev":
    MONGO_JOB_COLLECTION = "jobs"
    MONGO_JOB_DB = "task_meta_dev"
    CELERY_BROKER_URL = 'redis://localhost:6379/2'
    CELERY_QUEUE_NAME = "jobqueue"
    MONGODB_URI = 'mongodb://admin:admin@localhost:27017/task_meta_dev'
    logger = setup_logger('APP_NAME', './data/logs/dev/{}'.format(log_file_name))
