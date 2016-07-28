#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  Copyright Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################

_validators = {}
_defaultFunctions = {}


def registerValidator(key, fn):
    """
    Register a validator for a given setting key.

    :param key: The setting key.
    :type key: str
    :param fn: The function that will validate this key.
    :type fn: callable
    """
    _validators[key] = fn


def getValidator(key):
    """
    Retrieve the validator function for the given key. Returns ``None`` if none is registered.
    """
    return _validators.get(key)


def registerDefaultFunction(key, fn):
    """
    Register a default value function for a given setting key.

    :param key: The setting key.
    :type key: str
    :param fn: The function that will return the default value for this key.
    :type fn: callable
    """
    _defaultFunctions[key] = fn


def getDefaultFunction(key):
    """
    Retrieve the default value function for the given key. Returns ``None`` if none is registered.
    """
    return _defaultFunctions.get(key)


class validator(object):  # noqa: class name
    def __init__(self, key):
        """
        Create a decorator indicating that the wrapped function is responsible for
        validating the given key.

        :param key: The key that this function validates.
        :type key: str
        """
        self.key = key

    def __call__(self, fn):
        registerValidator(self.key, fn)
        return fn


class default(object):  # noqa: class name
    def __init__(self, key):
        """
        Create a decorator indicating that the wrapped function is responsible for
        providing the default value for the given key.

        :param key: The key that this function validates.
        :type key: str
        """
        self.key = key

    def __call__(self, fn):
        registerDefaultFunction(self.key, fn)
        return fn
