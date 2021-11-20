import json
import math

import requests
import urllib3
from tabulate import tabulate

TICKETS_PER_PAGE = 25


def load_config(config_file) -> dict:
    """
    Function to load the configuration file.
    
    Args:
        config_file (str): path to the configuration file
    """
    try:
        with open(config_file) as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Config file not found. Exiting...")
        return None

    # Check validity of the config file
    if "subdomain" not in config or "email" not in config or "password" not in config:
        print("Error: config file is missing required fields.")
        return None

    return config


def get_tickets(page: int, config: dict) -> dict:
    """
    Function to get a list of tickets for the given page number.

    Args:
        page (int): page number to get tickets from
        config (dict): configuration dictionary

    Returns:
        A JSON object containing the list of tickets if the request was successful,
        otherwise None.
    """
    # Set up request
    url = "https://{}.zendesk.com/api/v2/tickets".format(config["subdomain"])
    auth = (config["email"], config["password"])
    params = {"page": page, "per_page": TICKETS_PER_PAGE}

    try:
        # Get tickets
        response = requests.get(url, auth=auth, params=params)
        response.raise_for_status()
    except (requests.exceptions.HTTPError, urllib3.exceptions.LocationParseError):
        print("Error: could not connect to the API endpoint.")
        return None
        
    return response.json()


def get_ticket_by_id(ticket_id: int, config: dict) -> dict:
    """
    Function to get a single ticket by ticket ID.

    Args:
        ticket_id (int): ID of the ticket to get
        config (dict): configuration dictionary

    Returns:
        A JSON object containing the ticket if the request was successful,
        otherwise None.
    """
    # Set up request
    url = "https://{}.zendesk.com/api/v2/tickets/{}".format(config["subdomain"], ticket_id)
    auth = (config["email"], config["password"])

    try:
        # Get ticket
        response = requests.get(url, auth=auth)
        response.raise_for_status()
    except (requests.exceptions.HTTPError, urllib3.exceptions.LocationParseError):
        print("Error: ticket not found.")
        return None

    return response.json()["ticket"]


def display_tickets(data: dict, page: int) -> None:
    """
    Function to display the list of tickets.

    Args:
        data (dict): JSON object containing the list of tickets
        page (int): page number of the list of tickets
    """
    # If there are no tickets
    if len(data["tickets"]) == 0:
        print("No tickets found.")
        return

    # Create a table of tickets to display
    headers = ["Ticket ID", "Subject", "Status", "Priority"]
    table = []
    for ticket in data["tickets"]:
        subject = ticket["subject"]
        # If subject is too long, truncate it
        if len(subject) > 60:
            subject = subject[:57] + "..."
        table.append([ticket["id"], subject, ticket["status"], ticket["priority"]])

    print("\n", tabulate(table, headers=headers))

    # Extract the total number of pages
    total_tickets = data["count"]
    total_pages = math.ceil(total_tickets / TICKETS_PER_PAGE)

    # Get start and end ticket numbers
    start_ticket = (page - 1) * TICKETS_PER_PAGE + 1
    end_ticket = start_ticket + TICKETS_PER_PAGE - 1
    print(
        "\nViewing tickets {}-{} (page {} of {})".format(
            start_ticket, end_ticket, page, total_pages
        )
    )


def display_single_ticket(ticket: dict) -> None:
    """
    Function to display a single ticket.

    Args:
        ticket (dict): JSON object containing the ticket
    """
    print("\nTicket ID:", ticket["id"])
    print("Subject:", ticket["subject"])
    print("Status:", ticket["status"])
    print("Priority:", ticket["priority"])
    print("Description:", ticket["description"])
    print()


def main() -> None:
    """Main function to display the menu and run the program."""
    print("\nWelcome to the ticket viewer!")

    # Load configuration file
    config = load_config("config.json")

    # Exit if config file is invalid
    if config is None:
        return

    # Set pagination variable to decide whether to use pagination or not
    pagination = False

    while True:
        # Display menu
        print("\nMenu:")
        print("1. View all tickets")
        print("2. View a ticket by ticket ID")
        print("Type 'quit' to exit")
        choice = input("\nEnter your choice: ")

        # If user wants to quit
        if choice == "quit":
            print("\nThanks for using the ticket viewer! Goodbye.")
            break

        # View all tickets
        elif choice == "1":
            if pagination:
                try:
                    page = input("Enter page number (leave blank for first page): ")
                    page = 1 if page.strip() == "" else int(page)
                except ValueError:
                    print("Error: page number must be an integer.")
                    continue
            else:
                page = 1

            # Get a dictionary (JSON) of tickets
            data = get_tickets(page=page, config=config)

            # Display the tickets
            if data is not None:
                # Update pagination variable
                pagination = data["count"] > 25
                display_tickets(data, page=page)

        # View a ticket by ticket ID
        elif choice == "2":
            try:
                ticket_id = int(input("Enter ticket ID: "))
            except ValueError:
                print("Error: ticket ID must be an integer.")
                continue

            # Get a dictionary (JSON) of a single ticket
            ticket = get_ticket_by_id(ticket_id, config=config)

            # Display the ticket
            if ticket is not None:
                display_single_ticket(ticket)


if __name__ == "__main__":
    main()
