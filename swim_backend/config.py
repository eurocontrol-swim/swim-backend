"""
Copyright 2019 EUROCONTROL
==========================================

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
   disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
   disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

==========================================

Editorial note: this license is an instance of the BSD license template as provided by the Open Source Initiative:
http://opensource.org/licenses/BSD-3-Clause

Details on EUROCONTROL: http://www.eurocontrol.int
"""
import typing as t
import logging.config
import yaml

import flask
from mongoengine import connect
from pymongo import MongoClient
from redis import Redis

__author__ = "EUROCONTROL (SWIM)"


def _from_yaml(filename: str) -> t.Union[t.Dict[str, t.Any], None]:
    """
    Converts a YAML file into a Python dict

    :param filename:
    :return:
    """
    if not filename.endswith(".yml"):
        raise ValueError("YAML config files should end with '.yml' extension (RTFMG).")

    with open(filename) as f:
        obj = yaml.load(f, Loader=yaml.FullLoader)

    return obj or None


def load_app_config(filename: str) -> t.Dict[str, t.Any]:
    """
    It loads the configuration from the provided config file which should be a YAML file.

    :param filename:
    :return:
    """
    config = _from_yaml(filename)

    return config


def configure_logging(app: flask.Flask):
    """
    Initializes the logging of the provided app. The app should be already loaded with the necessary configuration
    which should provide a 'LOGGING' property.

    An example in YAML could be:

        LOGGING:
          version: 1

          handlers:
            console:
              class: logging.StreamHandler
              formatter: default
              level: DEBUG

          formatters:
            default:
              format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
              class: logging.Formatter

          disable_existing_loggers: false

          root:
            level: DEBUG
            handlers: [console]

          loggers:
            requests:
              level: INFO

            openapi_spec_validator:
              level: INFO

            connexion:
              level: INFO

    :param app:
    """
    logging.config.dictConfig(app.config['LOGGING'])


def configure_mongo(**kwargs) -> MongoClient:
    """
    Returns a MongoClient configured with the passed data
    :param kwargs: see mongoengine.connection.connect
    :return: MongoClient
    """
    return connect(**kwargs)


def configure_redis(**kwargs) -> Redis:
    """
    Returns a Redis client configured withthe passed data
    :param kwargs: see redis.client.Redis
    :return: redis.client.Redis
    """
    return Redis(**kwargs)

