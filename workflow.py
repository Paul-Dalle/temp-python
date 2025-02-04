from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from temporal_worker import hello

@workflow.defn
class SayHello:
    @workflow.run
    async def run(self, name: str) -> str:
        return await workflow.execute_activity(hello, name, start_to_close_timeout=timedelta(seconds=10))