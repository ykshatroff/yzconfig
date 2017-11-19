yzconfig
========

![build](https://travis-ci.org/ykshatroff/yzconfig.svg?branch=master)

Simple application configuration tool for Django (and others)

Summary
-------

`yzconfig` allows you to:

* Define all settings for all of your Django project's applications in one python object (usually, a module)
* Use name prefixes to instantiate the settings object of an application 

Usage
-----

`yzconfig` takes an arbitrary object and populates `settings` with values from its attributes whose names
are constructed as `prefix + attr` where `attr` is a `settings` class attribute and `prefix` is given as argument to
`settings` constructor.

An application's settings are defined in a class which inherits from `YzConfig`, then a settings object
is instantiated with the desired prefix:
```python
from yzconfig import YzConfig

class Settings(YzConfig):
    VALUE = "default"
    _SKIPPED_VALUE = 'skipped'

settings = Settings('TEST_')
```

If your Django settings contain a `TEST_VALUE` property, then the `settings` object's `VALUE` will contain its value,
otherwise it will remain with `"default"`.

Attributes beginning with `_` will not be overwritten. 

`yzconfig` can be used with Django or standalone. For the latter case, it's possible to provide a python dotted path
to the settings object in `YZCONFIG_MODULE` environment variable. The default is to import `settings`. 
To be used with Django, no extra actions are required.
