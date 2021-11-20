import app

config = app.load_config("config.json")


def test_load_config():
    config = app.load_config("config.json")

    # Not checking all keys, just checking that the config is loaded
    # as the config has email and password and we don't want to hardcode
    # the email and password in the test
    assert config is not None


def test_load_config_no_file():
    config = app.load_config("config_no_file.json")

    assert config is None


def test_load_config_invalid_file():
    config = app.load_config("testing_files/invalid_config.json")

    assert config is None


def test_get_tickets():
    tickets = app.get_tickets(page=1, config=config)

    assert tickets is not None


def test_get_tickets_invalid_request():
    subdomain = config["subdomain"]
    config["subdomain"] = ""
    tickets = app.get_tickets(page=1, config=config)
    config["subdomain"] = subdomain

    assert tickets is None


def test_get_ticket_by_id():
    ticket = app.get_ticket_by_id(ticket_id=2, config=config)

    assert ticket is not None


def test_get_ticket_by_id_invalid():
    ticket = app.get_ticket_by_id(ticket_id=0, config=config)

    assert ticket is None


def test_display_tickets():
    data = {
        "tickets": [
            {
                "id": 1,
                "subject": "Test ticket",
                "status": "open",
                "priority": "normal",
            }
        ],
        "count": 1
    }
    app.display_tickets(data, page=1)
    app.display_tickets({"tickets": []}, page=1)

    assert True


def test_display_single_ticket():
    data = {
        "id": 1,
        "subject": "Test ticket",
        "status": "open",
        "priority": "normal",
        "description": "Test ticket description"
    }
    app.display_single_ticket(data)

    assert True
