import sys
import requests
from temporalio.client import Client
from temporal_activity import process_api_documentation  # Import the activity

# Fetch the URL from the command line argument
if len(sys.argv) < 2:
    print("Usage: python extract_api_info.py <api_docs_url>")
    sys.exit(1)

api_docs_url = sys.argv[1]


async def main():
    # Create a Temporal client to connect to the Temporal server
    client = await Client.connect("temporal:7233")

    # Trigger the workflow to process the documentation
    result = await client.execute_workflow(process_api_documentation, api_docs_url)

    # Output the result
    print(f"Extracted API Information: {result}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
