import json
import math
import sys

import requests

# Load config file
try:
    with open("config.json") as f:
        CONFIG = json.load(f)
except FileNotFoundError:
    print("Config file not found. Exiting...")
    sys.exit()

TICKETS_PER_PAGE = 25

# Check validity of the config file
if "subdomain" not in CONFIG or "email" not in CONFIG or "password" not in CONFIG:
    print("Error: config file is missing required fields.")
    sys.exit()


def get_tickets(page: int) -> dict:
    """
    Function to get a list of tickets for the given page number.

    Args:
        page (int): page number to get tickets from

    Returns:
        A JSON object containing the list of tickets if the request was successful,
        otherwise None.
    """
    # Set up request
    url = "https://{}.zendesk.com/api/v2/tickets".format(CONFIG["subdomain"])
    auth = (CONFIG["email"], CONFIG["password"])
    params = {"page": page, "per_page": TICKETS_PER_PAGE}

    try:
        # Get tickets
        response = requests.get(url, auth=auth, params=params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
        print("Error: could not connect to the API endpoint.")
        return None

    # If request successful
    if response.status_code == 200:
        # Get tickets from response
        data = response.json()
        return data
    else:
        print(response.text)
        print("Error: could not connect to the API endpoint", url)
        return None


def get_ticket_by_id(ticket_id: int) -> dict:
    """
    Function to get a single ticket by ticket ID.

    Args:
        ticket_id (int): ID of the ticket to get

    Returns:
        A JSON object containing the ticket if the request was successful,
        otherwise None.
    """
    # Set up request
    url = "https://{}.zendesk.com/api/v2/tickets/{}".format(CONFIG["subdomain"], ticket_id)
    auth = (CONFIG["email"], CONFIG["password"])

    try:
        # Get ticket
        response = requests.get(url, auth=auth)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
        print("Error: ticket not found.")
        return None

    # If request successful
    if response.status_code == 200:
        # Get ticket from response
        ticket = response.json()["ticket"]
        return ticket
    else:
        print(response.text)
        print("Error: could not connect to the API endpoint", url)
        return None


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

    # If there are tickets
    print("\nTicket ID\tSubject\tStatus")
    for ticket in data["tickets"]:
        print("{}\t{}\t{}".format(ticket["id"], ticket["subject"], ticket["status"]))

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
    print("Description:", ticket["description"])
    print()


def main() -> None:
    """Main function to display the menu and run the program."""
    print("\nWelcome to the ticket viewer!")

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
            data = get_tickets(page=page)

            # Update pagination variable
            pagination = data["count"] > 25

            # Display the tickets
            if data is not None:
                display_tickets(data, page=page)

        # View a ticket by ticket ID
        elif choice == "2":
            try:
                ticket_id = int(input("Enter ticket ID: "))
            except ValueError:
                print("Error: ticket ID must be an integer.")
                continue

            # Get a dictionary (JSON) of a single ticket
            ticket = get_ticket_by_id(ticket_id)

            # Display the ticket
            if ticket is not None:
                display_single_ticket(ticket)


if __name__ == "__main__":
    main()
