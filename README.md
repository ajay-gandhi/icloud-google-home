# iCloud Google Home

This package allows you to interact with iCloud through your Google Home.
Currently, two features are supported - Find My iPhone and Reminders.

__Note:__ There is absolutely no security implemented with this package. If you
indeed set this up, it is possible for someone to obtain your iCloud email and
password.

## Usage

After setting everything up, you can use the phrases you set to create reminders
or find your phone.

For example:

* __Hey Google, where's my phone?__ Plays a sound on your device (surpasses
  silent mode, etc.)
* __Ok Google, remind me to mow the lawn at 6pm.__ Sets a reminder in your main
  Reminders folder with a due date of 6pm, today.

## Installation

There are two main steps you need to do to get everything running.

### Step 1: Start this server on a public machine

The interactions work by receiving web requests on the included server
(`server.py`). In other words, you have to run the server on a public-facing
machine. One possible way to do this is by running the server on Heroku.

Note that you'll need to install the python packages listed in requirements.txt:

```bash
python -r requirements.txt
```

### Step 2: Create IFTTT applets

Google Home/Google Assistant has an [IFTTT](http://ifttt.com) endpoint, so we
can use that and the Maker channel on IFTTT to allow our Google Home to send
requests to our server.

