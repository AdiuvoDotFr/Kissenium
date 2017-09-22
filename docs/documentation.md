---
layout: default
---

[Home](index.html) | [Documentation](documentation.html) | [Install on linux](install-on-linux.html) | [Install on windows](install-on-windows.html)

## Documentation

> This page is not finished yet

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
**PageWait** | Integer | How much we will wait for a page to fully load
**Browser** | Firefox, Chrome | Which browser to use
**BrowserSize** | Maximize, width*height | Configure the size of the browser
**BrowserMessage** | True, False | Print message in the navigator
**DimForDemo** | True, False | Dim page to bring eye to one element
