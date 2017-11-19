# -*- coding: utf-8 -*-
"""
The ``yzconfig`` package provides application configuration interface.

Settings can be taken from any object, e.g. ``django.conf.settings`` in django.

The complete description is in documentation for :class:`~yzconfig.YzConfig`.
"""
from .yzconfig import YzConfig, ImproperlyConfigured
