---
layout: default
---

[Home](index.html) | [Documentation](documentation.html) | [Install on linux](install-on-linux.html) | [Install on windows](install-on-windows.html)

## Documentation

> /!\ WARNING /!\ 
>This page is not finished yet

### Kissenium configuration

> kissenium.ini

Parameter | Values | Description
----------|--------|-------------
**LogLevel** | DEBUG, INFO, WARNING, ERROR | Configure the loglevel
**CaptureOnAssertFail** | True, False | Get a capture when an assert fail
**CaptureOnFail** | True, False | Get a capture when an error show up
**CaptureSize** | Full, Browser | Capture the content of the screen or the the browser content
**RecordScenarios** | True, False | Record a video of each test
**CaptureEndOfTest** | True, False | Take a capture when a test end
**FailOnAssertError** | Full, Browser | Fail when assert return false
**FailOnError** | True, False | Fail when an unexpected error show up
**PageWait** | Integer | How much time we will wait for a page to fully load
**Browser** | Firefox, Chrome | Which browser to use
**BrowserSize** | Maximize, width*height | Configure the size of the browser
**BrowserMessage** | True, False | Print message in the navigator
**DimForDemo** | True, False | Dim page to bring eye to one element

### Create a test

#### Create your first test file

Create your test file at the following place : `scenarios/my-test.py` with the following content :

```python
# coding: utf-8
import unittest
from utils.generics.test import GenericTest


class MyTest(GenericTest):

    def test_1_my_test(self):
        self.browser.get('http://www.kissenium.org')
```

Add your test to the following places: `scenarios/__init__.py` and `kissenium.py`.

```python
# coding: utf-8
from .demo import TestDemo
from .my-test import MyTest

```

Modify the init of the runner class like this :

```python
class Runner:

    def __init__(self):
        self.prepare_for_run()
        self.logger = Log4Kissenium().setup("Kissenium", "Kissenium")
        self.logger.info("Logger created.")
        self.test_classes_to_run = [scenarios.TestDemo, scenarios.MyTest] # Add your class test here
        self.loader = TestLoader()
        self.suites = []
```