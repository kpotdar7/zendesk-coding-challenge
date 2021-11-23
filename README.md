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
    $ python app.py
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
app.py          113      4    96% 
```

### Comments on design

- Even though OAuth is a more secure way to authenticate, I've used basic authentication for the ease of the code reviewer (assuming that the code reviewer has not generated the API token for their account).
- Renaming the config file from "config_sample.json" to "config.json" is required as I'm using the `.gitignore` file to ignore the "config.json" file that has my credentials.
- When the user starts the program and wants to see all the tickets, the program will fetch only the first 25 records. The user can then use the pagination to fetch the rest if more than 25 tickets are available.
- The config filename can be passed as an argument to the program instead of hardcoding it. But doing so was reducing the code coverage of the unit tests. So, I went ahead with the hardcoded "config.json" filename. 
- As this is a CLI application, providing user input during testing is a bit difficult. I've made minor changes to the code to make it easier for testing. 
	- Added `config_file` and `static_input` as additional parameters to the `main()` function. 
	- Created a new function to read user input -- `get_input` -- which either reads the input from the user or uses the `static_input` to generate the user input.