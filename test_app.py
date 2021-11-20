"""File containing the unit tests for the app.py file"""

import app

config = app.load_config("config.json")


def test_load_config():
    """Test case to test the load_config function"""
    config = app.load_config("config.json")

    # Not checking all keys, just checking that the config is loaded
    # as the config has email and password and we don't want to hardcode
    # the email and password in the test
    assert config is not None


def test_load_config_no_file():
    """Test case to test the load_config function when wrong file is passed"""
    config = app.load_config("config_no_file.json")

    assert config is None


def test_load_config_invalid_file():
    """Test case to test the load_config function when config with wrong keys is passed"""
    config = app.load_config("testing_files/invalid_config.json")

    assert config is None


def test_get_tickets():
    """Test case to test the get_tickets function"""
    tickets = app.get_tickets(page=1, config=config)

    assert tickets is not None


def test_get_tickets_invalid_request():
    """Test case to test the get_tickets function with invalid subdomain"""
    subdomain = config["subdomain"]
    config["subdomain"] = ""
    tickets = app.get_tickets(page=1, config=config)
    config["subdomain"] = subdomain

    assert tickets is None


def test_get_ticket_by_id():
    """Test case to test the get_ticket_by_id function"""
    ticket = app.get_ticket_by_id(ticket_id=2, config=config)

    assert ticket is not None


def test_get_ticket_by_id_invalid():
    """Test case to test the get_ticket_by_id function when invalid ID is passed"""
    ticket = app.get_ticket_by_id(ticket_id=0, config=config)

    assert ticket is None


def test_display_tickets_truncate():
    """
    Test case to test the display_tickets function
    when string is long and needs to be truncated
    """
    data = {
        "tickets": [
            {
                "id": 1,
                "subject": "Test ticket " * 50,
                "status": "open",
                "priority": "normal",
            }
        ],
        "count": 1,
    }
    app.display_tickets(data, page=1)
    app.display_tickets({"tickets": []}, page=1)


def test_main():
    """Test case to test the main function"""
    static_input = [
        "1",  # view all tickets
        "1",  # view all tickets
        "2",  # select a valid page number
        "1",  # view all tickets
        "a",  # select an invalid page number
        "1",  # view all tickets
        "10",  # select a page number that has no data
        "2",  # view a ticket by ticket ID
        "2",  # enter a valid ticket ID
        "2",  # view a ticket by ticket ID
        "a",  # enter an invalid ticket ID
        "2",  # view a ticket by ticket ID
        "0",  # enter a tucket ID that does not exist
        "quit",  # quit the program
    ]
    app.main(static_input=static_input)


def test_main_no_config():
    """Test case to test the main function with invalid config file name"""
    app.main("no.json")


def test_main_stop_iteration():
    """Test case to test the StopIteration code in the get_input function"""
    static_input = ["1"]
    app.main(static_input=static_input)
