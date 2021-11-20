# Zendesk Coding Challenge

### Installation steps

 - Install any Python version above 3.6 from https://www.python.org/downloads/
 - Run the following commands:
    ```
    $ git clone https://github.com/kpotdar7/zendesk-coding-challenge.git
    $ cd zendesk-coding-challenge
    $ pip install -r requirements.txt
    ```
 - Open the config_sample.json file and replace the "email", "password", and "subdomain" with valid email, password, and subdomain.
 - Rename the **config_sample.json** file to **config.json**.

### Usage

 - Run the following command to start the programs:
    ```
    $ python main.py
    ```
 - Follow the instructions on the screen.
 - To run the unit tests and get the code coverage, run the following command:
    ```
    $ pytest --cov=.
    ```

Code coverage report:

```
Name          Stmts   Miss  Cover
---------------------------------
app.py          110      2    98%
```