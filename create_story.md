```
Usage: create_story.py [OPTIONS]

  Creates one or more stories, optionally for the supplied sprint

Options:
  --config FILE                  Read configuration from FILE.
  -i, --instance INSTANCE        snow instance
  -u, --user USER                snow username
  -p, --password PASSWORD        snow password
  -s, --sprint TEXT              sprint to assign story to
  -a, --assign OWNER             user to assign story to, defaults to the user
                                 creating the story

  -g, --group GROUP              group to assign story to, defaults to the
                                 group sprint is assigned to

  -t, --title TEXT               title to use for story  [default: title to be
                                 added]

  -d, --description TEXT         description to use for story  [default:
                                 description to be added]

  -c, --comment TEXT             comments to add to the story
  -r, --criteria TEXT            acceptance criteria to add to the story
                                 [default: acceptance criteria to be added]

  -O, --product TEXT
  -R, --release TEXT
  -D, --demand TEXT
  -J, --project TEXT
  -M, --theme TEXT
  -E, --epic TEXT
  -S, --state [0|1|2|3|4|5|6|7]  state of task:

                                 0 - Draft
                                 1 - Ready
                                 2 - Work in progress
                                 3 - Complete
                                 4 - Cancelled
                                 5 - Ready for testing
                                 6 - Testing
                                 7 - On hold  [default: 0]

  -T, --type [0|1|2|3]           type of task:

                                 0 - None
                                 1 - Development
                                 2 - Documentation
                                 3 - Spike  [default: 1]

  -P, --priority [1|2|3|4]       priority of task:

                                 1 - Critical
                                 2 - High
                                 3 - Moderate
                                 4 - Low  [default: 4]

  -b, --blocked REASON           create story as blocked and supply a reason
  -q, --quantity INTEGER         quantity of stories to create. Creates
                                 multiples of exactly the same story. Useful
                                 for adding stories in bulk that can be
                                 updated later   [default: 1]

  -N, --noprompt                 create story without prompting the user
  -v, --verbose                  Be more verbose, -v is INFO, -vv is DEBUG
  --version                      Show the version and exit.
  --help                   Show this message and exit.

  default config file: ~/.snack/config.ini
```
