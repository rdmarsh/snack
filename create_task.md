```
Usage: create_task.py [OPTIONS]

  Creates one or more tasks for the supplied story

Options:
  --config FILE             Read configuration from FILE.
  -i, --instance INSTANCE   snow instance
  -u, --user USER           snow username
  -p, --password PASSWORD   snow password
  -s, --story TEXT          story to assign task to  [required]
  -a, --assign OWNER        user to assign task to, defaults to the user story
                            is assigned to

  -g, --group GROUP         group to assign task to, defaults to the group
                            story is assigned to

  -t, --title TEXT          title to use for task  [default: title to be
                            added]

  -d, --description TEXT    description to use for task  [default: description
                            to be added]

  -c, --comment TEXT        comments to add to the task
  -S, --state [0|1|2|3|4]   state of task:
                            
                            0 - Draft
                            1 - Ready
                            2 - Work in progress
                            3 - Complete
                            4 - Cancelled  [default: 0]

  -T, --type [1|2|3|4]      type of task:
                            
                            1 - Analysis
                            2 - Coding
                            3 - Documentation
                            4 - Testing  [default: 1]

  -P, --priority [1|2|3|4]  priority of task:
                            
                            1 - Critical
                            2 - High
                            3 - Moderate
                            4 - Low  [default: 4]

  -h, --hours INTEGER       planned hours of task  [default: 1]
  -b, --blocked REASON      create task as blocked and supply a reason
  -q, --quantity INTEGER    quantity of tasks to create. Creates multiples of
                            exactly the same task. Useful for adding tasks in
                            bulk that can be updated later   [default: 1]

  -N, --noprompt            create task without prompting the user
  -v, --verbose             Be more verbose, -v is INFO, -vv is DEBUG
  --version                 Show the version and exit.
  --help                    Show this message and exit.

  default config file: ~/.snack/config.ini
```
