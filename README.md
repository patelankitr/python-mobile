
# HexEngine - Mobile Automation Solution

## Tech Stack

This document provides an overview of the technologies used in the automation framework.

## Python
Used for scripting and writing automation logic.

## Appium
A tool for mobile automation, enabling interaction with mobile applications across different platforms.

## pytest
A framework for test execution and reporting, offering powerful features for writing scalable tests.

## Selenium/WebDriver
Used for testing web views inside mobile apps, ensuring proper functionality and compatibility.

## Allure Report
A test reporting tool that provides detailed insights into test execution results.

## Logging
Utilized to track execution flow and failures, aiding in debugging and analysis.

## CI/CD
Integrated with Jenkins/GitHub Actions to automate the testing process, ensuring continuous integration and deployment.



get all installed packages

`pip freeze > requirements.txt`

To Install Packages from requirements.txt

`pip install -r requirements.txt`
## content-desc
![img.png](img.png)

### use

`    
"continue_text_button": {
    "locator_type": "content",
        "locator": "CONTINUE"
      }
`

Emoji cheat sheet

`https://www.webfx.com/tools/emoji-cheat-sheet`

Methods:
tap_on_element
double_tap_on_element
enter_text
swipe_element_to_element
swipe_by_direction
swipe_by_coordinates
text_print

element_visible
element_not_visible
element_present
long_press_element
multi_tap


## Android TV
```
    "androidTV": {
      "platform": "android",
      "appPath/appPackage": "com.google.android.apps.tv.launcherx",
      "platformVersion": "11",
      "deviceName": "Smart TV",
      "automationName": "UiAutomator2",
      "appActivity": "com.google.android.apps.tv.launcherx.home.HomeActivity",
      "capabilities": {
        "appWaitDuration": 30000,
        "newCommandTimeout": 60,
        "noReset": true,
        "autoGrantPermissions": true,
        "dontStopAppOnReset": true
      }
    }
```

