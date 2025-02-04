import asyncio
from temporalio.worker import Worker
from temporalio.client import Client
from temporal_activity import process_api_documentation


async def run_worker():
    # Connect to Temporal server
    client = await Client.connect("temporal:7233")

    # Create a worker to listen for activities
    worker = Worker(client, task_queue="api-doc-extractor", activities=[process_api_documentation])

    # Start the worker to process activities
    print("Worker is starting...")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(run_worker())
