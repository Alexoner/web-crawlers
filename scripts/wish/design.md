## concurrency
1. Task map/queue to maintain the active requests
2. Asynchronous HTTP request

## stop criteria
1. Finished fetching:received items has size of zero
2. Invalid request:received items has size of zero

## timeout,dead requests
Periodically check for dead tasks,replace them with new tasks

## exception
Catch exception to prevent the main program from exiting
