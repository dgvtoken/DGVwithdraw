#!/usr/bin/python3 python
# -*- coding: utf-8 -*-
import logging

from config import gdae_config

logging.basicConfig(**gdae_config.logger_config)
logger = logging.getLogger()
