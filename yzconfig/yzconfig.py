# -*- coding: utf-8 -*-
# Date: 03.06.14
"""
THe ``yzconfig`` package provides application configuration interface.

Settings can be taken from any object, e.g. ``django.conf.settings`` in django.
"""
from __future__ import absolute_import
import os
try:
    from django.core.exceptions import ImproperlyConfigured
except ImportError:
    HAS_DJANGO = False

    class ImproperlyConfigured(ValueError):
        pass
else:
    HAS_DJANGO = True


ENV_YZCONFIG_MODULE = 'YZCONFIG_MODULE'


def import_symbol(dotted_name):
    """Import an arbitrary symbol (including modules) by its dotted name"""
    try:
        spec = dotted_name.rsplit('.', 1)
        try:
            mod_name, attr = spec
        except ValueError:
            sym = __import__(dotted_name, None, None, [])
        else:
            mod = __import__(mod_name, None, None, [attr])
            sym = getattr(mod, attr)
    except (ImportError, AttributeError, ValueError):
        raise ImportError("Can not import %r" % dotted_name)
    return sym


class YzConfig(object):
    """Configuration provider

    Class ``DefaultSettings`` is a more convenient style for per-application settings
    allowing to see (and index via IDE) what settings are defined

    Usage:

    * given some existing configuration object, e.g. ``django.conf.settings``, or the Config class below:

    >>> class Config(object):
    ...     TEST_GLOBAL_SETTING = "global"
    ...     TEST__SKIPPED_SETTING = 'whatever'

    * define your own settings in a subclass:

    >>> class Settings(YzConfig):
    ...     GLOBAL_SETTING = "original"
    ...     UNCHANGED_SETTING = "unchanged"
    ...     _SKIPPED_SETTING = 'skipped'

    * initialize a settings instance with prefix (omit ``config`` argument to use imported ``settings``)

    >>> settings = Settings('TEST_', config=Config)
    >>> settings.GLOBAL_SETTING
    'global'
    >>> settings.UNCHANGED_SETTING
    'unchanged'
    >>> settings._SKIPPED_SETTING
    'skipped'

    * now it's possible to delete the ``Settings`` class to save memory, because the settings object is single

    >>> del Settings

    * optionally add check function ``_check_settings()`` with assertions about settings
    * if for some reason you need to disable settings checks, it is possible with the following configuration settings:

        * to disable checks globally, set ``YZCONFIG_CHECK_SETTINGS`` to ``False``
        * on a per-package basis, set ``prefix+'CHECK_SETTINGS'`` to ``False``
    """
    #: name of configuration variable that disables settings check if set to False
    _CHECK_SETTINGS_ATTR = 'YZCONFIG_CHECK_SETTINGS'
    #: whether to check settings in __init__
    CHECK_SETTINGS = True

    def __init__(self, prefix='', config=None):
        """Identify settings to be used

        For all public fields of the DefaultSettings subclass, e.g. class.VAR:

        * try to use a ``config`` attribute with the given ``prefix`` as settings variable: e.g. PREFIX_VAR
        * if none found, use the value of class.VAR

        :param prefix: the ``namespace`` prefix for the application's settings
        :param config: optional configuration object
        :raises: ImproperlyConfigured
        """
        self._prefix = prefix
        if config is None:
            config = self.get_settings()

        for var in dir(self.__class__):
            if not var.startswith('_'):  # skip hidden vars
                try:
                    final_setting = getattr(config, "%s%s" % (prefix, var))
                except AttributeError:
                    final_setting = getattr(self, var)
                setattr(self, var, final_setting)

        self._on_settings_loaded()

        need_check = self.CHECK_SETTINGS and getattr(config, self._CHECK_SETTINGS_ATTR, True)
        if need_check:
            try:
                self._check_settings()
            except AssertionError as e:
                raise ImproperlyConfigured(str(e))

    @classmethod
    def get_settings(cls):
        """
        Try to obtain a settings object from a dotted path to the object, then from django settings.
        Fall back to an empty object

        :return: object
        """
        try:
            settings = getattr(cls, '_settings')
        except AttributeError:
            module_name = os.environ.get(ENV_YZCONFIG_MODULE)
            if module_name:
                try:
                    settings = import_symbol(module_name)
                except ImportError:
                    raise ImproperlyConfigured("Failed to import symbol %r given in environment variable" % module_name)
            elif HAS_DJANGO:
                try:
                    from django.conf import settings
                except ImportError as e:
                    raise e
            else:
                try:
                    import settings
                except ImportError:
                    raise ImproperlyConfigured("Failed to import settings")
            cls._settings = settings
        return settings

    def _on_settings_loaded(self):
        """
        A hook after settings have been assigned
        """
        pass

    def _check_settings(self):
        """
        Check any settings after initialization, using assert statements.
        If assertion fails, ``ImproperlyConfigured`` will be raised with the assertion message as value

        >>> class Settings(YzConfig):
        ...     GOOD_SETTING = 100
        ...     BAD_SETTING = ""
        ...     def _check_settings(self):
        ...         assert self.GOOD_SETTING is not None, "GOOD_SETTING is None"
        ...         assert self.BAD_SETTING, "BAD_SETTING is empty"
        >>> settings = Settings(config=None)
        Traceback (most recent call last):
        ...
        ImproperlyConfigured: BAD_SETTING is empty

        :raises: AssertionError
        """
        pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
