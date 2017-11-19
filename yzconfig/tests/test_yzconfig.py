# -*- coding: utf-8 -*-
# Date: 10.05.16
from __future__ import absolute_import
import os
import unittest

from yzconfig import ImproperlyConfigured
from yzconfig.yzconfig import import_symbol


class _Settings(object):
    PREFIX1_VAR1 = 'yes'
    PREFIX1_VAR2 = 'no'
    PREFIX1__HIDDEN = "Not included from settings"
    PREFIX1__HIDDEN_2 = "Not included from settings"
    PREFIX2_VAR1 = True
    PREFIX2_VAR2 = False
    PREFIX2_VAR3 = 3


testsettings = _Settings()


class DjangolessTest(unittest.TestCase):
    def test_import(self):
        # for coverage ;-)
        self.assertIs(import_symbol('yzconfig.tests.testsettings'), testsettings)
        with self.assertRaises(ImportError):
            import_symbol('nosuchmodule')
        with self.assertRaises(ImportError):
            import_symbol('yzconfig.tests.nosuchvar')

    def test_settings(self):
        from yzconfig.yzconfig import ENV_YZCONFIG_MODULE, YzConfig
        os.environ[ENV_YZCONFIG_MODULE] = 'yzconfig.tests.testsettings'

        class SettingsEx(YzConfig):
            VAR1 = 'var1'  # exists in settings = 'yes'
            VAR2 = 'var2'  # exists in settings = 'no'
            VAR3 = 'var3'  # not set in settings
            _HIDDEN = "hidden"  # never changed by settings

        settings_test = SettingsEx('PREFIX1_')

        self.assertEqual(settings_test.VAR1, 'yes')  # taken from settings
        self.assertEqual(settings_test.VAR2, 'no')  # taken from settings
        self.assertEqual(settings_test.VAR3, 'var3')  # taken from self
        self.assertEqual(settings_test._HIDDEN, 'hidden')  # taken from self, never changes

        with self.assertRaises(AttributeError):
            settings_test._HIDDEN_2

    def test_check(self):
        from yzconfig.yzconfig import ENV_YZCONFIG_MODULE, YzConfig
        os.environ[ENV_YZCONFIG_MODULE] = 'yzconfig.tests.testsettings2'

        class SettingsEx(YzConfig):
            VAR4 = None

            def _check_settings(self):
                assert self.VAR4 is not None

        with self.assertRaises(ImproperlyConfigured):
            settings_test = SettingsEx('PREFIX1_')

    def test_settings_subclass(self):
        from yzconfig.yzconfig import ENV_YZCONFIG_MODULE, YzConfig
        os.environ[ENV_YZCONFIG_MODULE] = 'yzconfig.tests.testsettings'

        class Settings(YzConfig):
            VAR1 = 'no'  # exists in settings = 'yes'
            VAR3 = 'var3'  # does not exist in settings

        class SubSettings(Settings):
            VAR1 = 'var1'  # exists in settings = 'yes'
            VAR2 = 'var2'  # exists in settings = 'no'
            MY_OTHER_VAR = 'other'  # set own, does not exist in settings
            _HIDDEN = 'hidden'  # never changed by settings

            def my_func(self):
                """Must remain callable and return"""
                return "test"

        sub_settings = SubSettings("PREFIX1_")
        self.assertEqual(sub_settings.VAR1, 'yes')  # taken from settings
        self.assertEqual(sub_settings.VAR2, 'no')  # taken from settings
        self.assertEqual(sub_settings.VAR3, 'var3')  # taken from parent
        self.assertEqual(sub_settings.MY_OTHER_VAR, 'other')  # taken from self
        self.assertEqual(sub_settings._HIDDEN, 'hidden')  # taken from self, never changes
        self.assertEqual(sub_settings.my_func(), 'test')

        with self.assertRaises(AttributeError):
            sub_settings._HIDDEN_2

