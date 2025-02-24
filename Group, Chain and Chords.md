# Group, Chain and Chords

## 1. Group

Group is used when a task is to be executed parallely.

```sh
task = group(
    add.s(a, b),
    subtract.s(a, b),
    multiply.s(a, b),
    divide.s(a, b)
)
task.apply_async()
```

```
                  Start
                    |
                    |
                    |
   -----------------------------------------------
    |           |               |               |
  add(a,b)  subtract(a,b)  multiply(a, b)   divide(a,b)
```

Here, all the task runs parallely and are independent of each other.

## 2. Chain

- Used when a task is to be executed after finishing previous task.

task = chain(
    add.s(a, b),
    subtract.s(b),
)
task.apply_async()
```

Also equivalent to using pipe operator.

```
task = (
        add.s(a, b) | 
        subtract.s(c)
) 
task.apply_async()
```

```
      Start
        |
        |
        |
     add.s(a,b) => a + b = z
        |
        |
    subtract.s(c) => z - c (z passed automatically as output from 1st task in chain)
```

Definition for subtract would look like below:

```python
@shared_task
def subtract(z, c):
    return z - c
```

## Chords

- Used in a reduce workflow as a part of map, reduce.

- Allows perform a group of tasks in parallel and then execute a callback task once all tasks in the group have finished.

```
task = chord(
    group(
        add.s(a, b),
        subtract.s(c, d),
        multiply.s(e, f)
    ),
    sum_results.s()
)
```

Also written as

```sh
task = chord(
    group(
        add.s(a, b),
        subtract.s(c, d),
        multiply.s(e, f)
    )
)(sum_results.s())
```

```sh
    ----------------------------------------------------
        |                  |                   |   
    add(a,b) => x   subtract(c, d) => y  multiple(e,f) => z
        |                  |                   |
    ---------------------------------------------------- => After finishing all
                           |
                      sum_result => x + y + z 
```