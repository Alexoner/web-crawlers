## concurrency
1. task map/queue to maintain the active requests
2. asynchronous HTTP request

## stop criteria
1. Finished fetching:received items has size of zero
2. Invalid request:received items has size of zero

## timeout,dead requests
periodically check for dead tasks,replace them with new tasks
