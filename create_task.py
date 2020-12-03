#!/usr/bin/env python3

#    snack SNow Agile Cli Kludge
#    Copyright (C) 2020 David Marsh
#
#    This program is free software: you can redistribute it and/or modify
#    iti under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
snack SNow Agile Cli Kludge
"""

__project__ = 'snack'
__appname__ = 'create_task'
__appdesc__ = 'Creates one or more tasks for the supplied story'
__version__ = '0.3'
__author__ = 'David Marsh'
__license__ = 'GPLv3'
__copyright__ = 'Copyright 2020 David Marsh'
__url__ = 'https://github.com/rdmarsh/snack'

import os
import sys
import logging
import click
import click_config_file
import pysnow

root_logger = logging.getLogger()
config_file = os.path.join(click.get_app_dir(__project__, force_posix=True), 'config.ini')

@click.command(epilog='default config file: ' + click.format_filename(config_file))
@click_config_file.configuration_option(config_file_name=config_file)

@click.option('-i', '--instance', metavar='INSTANCE',
              help='snow instance')

@click.option('-u', '--user', metavar='USER',
              help='snow username')

@click.option('-p', '--password', metavar='PASSWORD',
              prompt=True, hide_input=True,
              help='snow password')

@click.option('-s', '--story',
              required=True,
              help='story to assign task to')

@click.option('-a', '--assign', 'assigned_to', metavar='OWNER',
              help="""user to assign task to,
              defaults to the user story is assigned to""")

@click.option('-g', '--group', 'assignment_group', metavar='GROUP',
              help='group to assign task to, defaults to the group story is assigned to')

@click.option('-t', '--title', 'short_description',
              default='title to be added', show_default=True,
              help='title to use for task')

@click.option('-d', '--description', 'description',
              default='description to be added', show_default=True,
              help='description to use for task')

@click.option('-c', '--comment', 'comments',
              help='comments to add to the task')

@click.option('-S', '--state',
              type=click.Choice(['0', '1', '2', '3', '4']),
              default='0', show_default=True,
              help="""state of task:

                   \b
                   0 - Draft
                   1 - Ready
                   2 - Work in progress
                   3 - Complete
                   4 - Cancelled
                   """)

@click.option('-T', '--type', 'type_',
              type=click.Choice(['1', '2', '3', '4']),
              default='1', show_default=True,
              help="""type of task:

                   \b
                   1 - Analysis
                   2 - Coding
                   3 - Documentation
                   4 - Testing
                   """)

@click.option('-P', '--priority',
              type=click.Choice(['1', '2', '3', '4']),
              default='4', show_default=True,
              help="""priority of task:

                   \b
                   1 - Critical
                   2 - High
                   3 - Moderate
                   4 - Low
                   """)

@click.option('-h', '--hours', 'planned_hours',
              type=int,
              default=1, show_default=True,
              help='planned hours of task')

@click.option('-b', '--blocked', 'blocked_reason',
              metavar='REASON',
              help='create task as blocked and supply a reason')

@click.option('-q', '--quantity',
              type=int,
              default=1, show_default=True,
              help="""quantity of tasks to create. Creates multiples of
                      exactly the same task. Useful for creating tasks in
                      bulk that can be updated later """)

@click.option('-N', '--noprompt',
              is_flag=True,
              help='create task without prompting the user')

@click.option('-v', '--verbose',
              count=True,
              help='Be more verbose, -v is INFO, -vv is DEBUG')

@click.version_option(version=__version__)

def create_task(instance, user, password, assigned_to, assignment_group,
                short_description, description, comments, story, state,
                type_, priority, planned_hours, blocked_reason, quantity,
                noprompt, verbose):
    """Creates one or more tasks for the supplied story"""

    if verbose >= 2:
        root_logger.setLevel(logging.DEBUG)
    elif verbose == 1:
        root_logger.setLevel(logging.INFO)
    else:
        root_logger.setLevel(logging.WARNING)

    if not instance or not user or not password:
        click.secho('error: snow instance, user or password not set via cli or in config file',
                    fg='red', err=True)
        click.secho('default config file: ' + click.format_filename(config_file),
                    fg='red', err=True)
        sys.exit(1)

    logging.info('instance: %s', instance)
    logging.info('user: %s', user)
    logging.info('password: %s', '[REDACTED]')

    # change DRAFT state back to '-6', because asking a user to enter a negative number is ugly
    if state == 0:
        state = -6

    # if supplied a blocked_reason, set blocked to True, else False
    blocked = bool(blocked_reason)

    snow_client = pysnow.Client(instance=instance, user=user, password=password)
    logging.debug('snow_client: %s', snow_client)

    # check the story supplied exists, save sys_id, user and group for later
    story_fields = ['sys_id', 'assigned_to', 'assignment_group']
    logging.debug('story_fields: %s', story_fields)

    story_query = {'number': story}
    logging.debug('story_query: %s', story_query)

    story_resource = snow_client.resource(api_path='/table/rm_story')
    logging.debug('story_resource: %s', story_resource)

    story_response = story_resource.get(
        fields=story_fields,
        query=story_query,
        display_value=False,
        exclude_reference_link=True,
        )
    logging.debug('story_response: %s', story_response)

    try:
        story_response_one = story_response.one()
    except:
        click.secho('error: story ' + story + ', stopping', fg='red', err=True)
        raise
    logging.debug('story_response_one: %s', story_response_one)

    story_sys_id = story_response_one['sys_id']
    logging.info('story: %s', story)
    logging.info('story_sys_id: %s', story_sys_id)

    # find owner if none supplied
    if not assigned_to:
        assigned_to = story_response_one['assigned_to']
    logging.info('assigned_to: %s', assigned_to)

    # find group if none supplied
    if not assignment_group:
        assignment_group = story_response_one['assignment_group']
    logging.info('assignment_group: %s', assignment_group)

    logging.info('short_description: %s', short_description)
    logging.info('description: %s', description)
    logging.info('comments: %s', comments)
    logging.info('state: %s', state)
    logging.info('type_: %s', type_)
    logging.info('priority: %s', priority)
    logging.info('planned_hours: %s', planned_hours)
    logging.info('blocked: %s', blocked)
    logging.info('blocked_reason: %s', blocked_reason)
    logging.info('quantity: %s', quantity)
    logging.info('noprompt: %s', noprompt)

    # make task plural if more than one
    ess = 's' if quantity > 1 else ''

    click.secho("Creating {} task{} to story {}".format(quantity, ess, story),
                fg='blue', err=False)

    if not noprompt:
        click.confirm("Do you want to continue?", abort=True)

    task_resource = snow_client.resource(api_path='/table/rm_scrum_task')
    logging.debug('task_resource: %s', task_resource)

    for _ in range(quantity):
        new_task_payload = {
            "assigned_to": assigned_to,
            "assignment_group": assignment_group,
            "short_description": short_description,
            "description": description,
            "comments": comments,
            "state": state,
            "type": type_,
            "priority": priority,
            "planned_hours": planned_hours,
            "blocked": blocked,
            "blocked_reason": blocked_reason,
            "parent": story_sys_id,
        }
        logging.debug('new_task_payload: %s', new_task_payload)

        try:
            createtask_response = task_resource.create(
                payload=new_task_payload,
            )
            logging.debug('createtask_response: %s', createtask_response)
        except:
            click.secho('error: create task failed for story ' + story + ', stopping',
                        fg='red', err=True)
            raise

        try:
            createtask_response_one = createtask_response.one()
            logging.debug('createtask_response_one: %s', createtask_response_one)
        except:
            click.secho('error: create task failed for story ' + story + ', stopping',
                        fg='red', err=True)
            raise

        task = createtask_response_one['number']
        click.secho("success: for story {}; created task {}".format(story, task),
                    fg='green', err=False)


if __name__ == '__main__':
    create_task() # pylint: disable=no-value-for-parameter
