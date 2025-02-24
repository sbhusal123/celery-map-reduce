## Starting a Celery Worker:

``celery -A myproject worker --loglevel=info``

- ``-A myproject``
    - specifies the Celery application to be used
    - ``myproject`` refers to your Celery application instance
    - In the context of a Django project, this would typically be the name of your Django project (or the Celery instance defined in your Django project's celery.py).

- ``worker``
    - This tells Celery to start a worker process that will listen for tasks and execute them.
    - The worker is the core component that processes the tasks sent to it by the message broker (like RabbitMQ, Redis, etc.).

- ``--loglevel=info``
    - This sets the logging level for the worker.
    - Sets log level to ``info``

**Commonly Used Options:**

1. ``-A`` or ``--app``

- Specifies the Celery application to use.
- Example: ``-A myproject`` (Replace myproject with your Django project name).

2. ``--loglevel``
- Sets the log level for the worker. It controls the verbosity of the logs.
- Example: ``--loglevel=info``, ``--loglevel=debug``, ``--loglevel=warning``, etc.
- Default: INFO

```sh
--loglevel=debug
```

3. ``-n`` or ``--hostname``

- Set a custom hostname for the worker.

- Example: ``-n worker1@%h`` (Using %h for the machine's hostname).

```sh
-n worker1
```

4. ``--concurrency``

- Set the number of concurrent worker processes or threads. The default is the number of CPUs available on the machine.

- Example: ``--concurrency=4`` (Run 4 worker processes).

```sh
--concurrency=4
```

5. ``--autoscale``

- Automatically scale the number of worker processes depending on the workload.

- Format: ``--autoscale=10,3`` (Max 10 workers, min 3 workers).

```sh
--autoscale=10,3
```

6. ``--pool``

- Specifies the pool type used to handle tasks. The default is prefork, which uses multiple processes.

- Example: ``--pool=solo`` for a **single-threaded pool**, ``--pool=eventlet`` or ``--pool=gevent`` for **green threads**.

```sh
--pool=gevent
```

7. ``--maxtasksperchild``

- Limits the number of tasks a worker will process before restarting.

- Example: --maxtasksperchild=100 (worker will restart after processing 100 tasks).

```sh
--maxtasksperchild=100
```

8. ``--queue``

- Specifies which queue the worker will listen to. If your tasks are divided into different queues, use this option to specify a queue.

- Example: ``--queue=high_priority``.

```sh
--queue=high_priority
```

9. ``--without-gossip``

- Disables gossip and communication between workers (can be useful in a high-performance environment).

- Example: ``--without-gossip``

```sh
--without-gossip
```

10. ``--without-mingle``

- Disables the mingling of workers when they start up. This prevents workers from syncing information with each other.

- Example: ``--without-mingle``

```sh
--without-mingle
```

11. ``--disable-rate-limit``

- Disables the rate limit for tasks. If you don’t want to limit task execution rate.

```sh
--disable-rate-limit
```

- Disables the rate limit for tasks. If you don’t want to limit task execution rate.

12. ``--prefetch-multiplier``

- Controls how many tasks are sent to each worker before it sends acknowledgment. Increasing this value can increase throughput.

- Example: ``--prefetch-multiplier=10``.

```sh
prefetch-multiplier=10
```

13. ``--timezone``

- Sets the timezone for the worker. By default, it uses the UTC timezone.

- Example: ``--timezone=America/New_York``

```bash
--timezone=UTC
```

14. ``--beat``

- Enable Celery Beat (for periodic tasks) in the worker. This allows the worker to run periodic tasks.

- Example: ``--beat``


15. ``--max-memory-per-child``

- Limits the memory usage per worker before it’s restarted.

- Example: ``--max-memory-per-child=100000000`` (100 MB).

```bash
--max-memory-per-child=100000000
```
