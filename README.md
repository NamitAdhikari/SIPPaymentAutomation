## SIP Payment Automation

This is a simple automation script to automate the payment of SIPs (N** **** BANK currently added) using e**** payment
platform. It uses Selenium to automate the browser and the script is written in Python.

### Requirements

You primarily need `selenium` to run the script. Similarly, you need `python-dotenv` to load the environment variables
from the `.env` file.

```shell
pip install selenium python-dotenv
```

### Usage

You need to create a `.env` file in the root directory of the project following the sample provided as `.env.sample`.
Currently, password has been placed in `.env` file, however, you can choose not to do so.
The shell will prompt you to enter the password(s) if you don't provide it in the `.env` file.

You can simply run the script using the following command:

```shell
python sip_payment_bank1.py
```
