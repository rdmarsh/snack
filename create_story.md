```
Usage: create_story.py [OPTIONS]

  Creates one or more stories, optionally for the supplied sprint

Options:
  --config FILE            Read configuration from FILE.
  -i, --instance INSTANCE  snow instance
  -u, --user USER          snow username
  -p, --password PASSWORD  snow password
  -s, --sprint TEXT        sprint to assign story to
  -a, --assign OWNER       user to assign story to, defaults to the user
                           creating the story

  -g, --group GROUP        group to assign story to, defaults to the group
                           sprint is assigned to

  -t, --title TEXT         title to use for story  [default: title to be
                           added]

  -d, --description TEXT   description to use for story  [default: description
                           to be added]

  -c, --comment TEXT       comments to add to the story
  -r, --criteria TEXT      acceptance criteria to add to the story  [default:
                           acceptance criteria to be added]

  -b, --blocked REASON     create story as blocked and supply a reason
  -q, --quantity INTEGER   quantity of stories to create. Creates multiples of
                           exactly the same story. Useful for adding stories
                           in bulk that can be updated later   [default: 1]

  -N, --noprompt           create story without prompting the user
  -v, --verbose            Be more verbose, -v is INFO, -vv is DEBUG
  --version                Show the version and exit.
  --help                   Show this message and exit.

  default config file: ~/.snack/config.ini
```
