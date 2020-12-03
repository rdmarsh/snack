#!/usr/bin/env python3

#    snack SNow Agile Cli Kludge
#    Copyright (C) 2020 David Marsh
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
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
__appname__ = 'create_story'
__appdesc__ = 'Creates one or more stories, optionally for the supplied sprint'
__version__ = '0.1'
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

@click.option('-s', '--sprint',
              help='sprint to assign story to')

@click.option('-a', '--assign', 'assigned_to', metavar='OWNER',
              help="""user to assign story to,
              defaults to the user creating the story""")

@click.option('-g', '--group', 'assignment_group', metavar='GROUP',
              help='group to assign story to, defaults to the group sprint is assigned to')

@click.option('-t', '--title', 'short_description',
              default='title to be added', show_default=True,
              help='title to use for story')

@click.option('-d', '--description', 'description',
              default='description to be added', show_default=True,
              help='description to use for story')

@click.option('-c', '--comment', 'comments',
              help='comments to add to the story')

@click.option('-b', '--blocked', 'blocked_reason',
              metavar='REASON',
              help='create task as blocked and supply a reason')

@click.option('-q', '--quantity',
              type=int,
              default=1, show_default=True,
              help="""quantity of stories to create. Creates multiples of
                      exactly the same story. Useful for adding stories in
                      bulk that can be updated later """)

@click.option('-N', '--noprompt',
              is_flag=True,
              help='create task without prompting the user')

@click.option('-v', '--verbose',
              count=True,
              help='Be more verbose, -v is INFO, -vv is DEBUG')

@click.version_option(version=__version__)

def create_story(instance, user, password, assigned_to, assignment_group,
                short_description, description, comments, sprint,
                blocked_reason, quantity, noprompt, verbose):
    """Creates one or more stories, optionally for the supplied sprint"""

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

    # if supplied a blocked_reason, set blocked to True, else False
    blocked = bool(blocked_reason)

    snow_client = pysnow.Client(instance=instance, user=user, password=password)
    logging.debug('snow_client: %s', snow_client)

    if not assignment_group and not sprint:
        click.secho('error: sprint or group not supplied via cli or in config file',
                    fg='red', err=True)
        click.secho('default config file: ' + click.format_filename(config_file),
                    fg='red', err=True)
        sys.exit(1)

    if assignment_group:
        # check the assignment_group supplied exists, save sys_id, name and type for later
        group_fields = ['sys_id', 'name', 'type']
        logging.debug('group_fields: %s', group_fields)

        group_query = {'name': assignment_group}
        logging.debug('group_query: %s', group_query)

        group_resource = snow_client.resource(api_path='/table/sys_user_group')
        logging.debug('group_resource: %s', group_resource)

        group_response = group_resource.get(
            fields=group_fields,
            query=group_query,
            display_value=False,
            exclude_reference_link=True,
            )
        logging.debug('group_response: %s', group_response)

        try:
            group_response_one = group_response.one()
        except:
            click.secho('error: group ' + assignment_group + ', stopping', fg='red', err=True)
            raise
        logging.debug('group_response_one: %s', group_response_one)

        group_sys_id = group_response_one['sys_id']
        logging.info('group: %s', assignment_group)
        logging.info('group_sys_id: %s', group_sys_id)

    if sprint:
        # check the sprint supplied exists, save sys_id, assigned_to, assignment_group and state for later
        sprint_fields = ['sys_id', 'assigned_to', 'assignment_group', 'state']
        logging.debug('sprint_fields: %s', sprint_fields)

        sprint_query = {'number': sprint}
        logging.debug('sprint_query: %s', sprint_query)

        sprint_resource = snow_client.resource(api_path='/table/rm_sprint')
        logging.debug('sprint_resource: %s', sprint_resource)

        sprint_response = sprint_resource.get(
            fields=sprint_fields,
            query=sprint_query,
            display_value=False,
            exclude_reference_link=True,
            )
        logging.debug('sprint_response: %s', sprint_response)

        try:
            sprint_response_one = sprint_response.one()
        except:
            click.secho('error: sprint ' + sprint + ', stopping', fg='red', err=True)
            raise
        logging.debug('sprint_response_one: %s', sprint_response_one)

        sprint_sys_id = sprint_response_one['sys_id']
        logging.info('sprint: %s', sprint)
        logging.info('sprint_sys_id: %s', sprint_sys_id)

    # find owner if none supplied
    if not assigned_to:
        assigned_to = user
    logging.info('assigned_to: %s', assigned_to)

    # find group if none supplied
    if not assignment_group:
        assignment_group = sprint_response_one['assignment_group']
    logging.info('assignment_group: %s', assignment_group)

    # set sprint_sys_id to none if sprint not supplied
    if not sprint:
        sprint_sys_id = None

    logging.info('short_description: %s', short_description)
    logging.info('description: %s', description)
    logging.info('comments: %s', comments)
    logging.info('blocked: %s', blocked)
    logging.info('blocked_reason: %s', blocked_reason)
    logging.info('quantity: %s', quantity)
    logging.info('noprompt: %s', noprompt)

    # make story plural if more than one
    ess = 'stories' if quantity > 1 else 'story'

    if sprint:
        click.secho("Creating {} {} for sprint {}".format(quantity, ess, sprint),
                    fg='blue', err=False)
    else:
        click.secho("Creating {} {} for {} backlog".format(quantity, ess, assignment_group),
                    fg='blue', err=False)

    if not noprompt:
        click.confirm("Do you want to continue?", abort=True)

    story_resource = snow_client.resource(api_path='/table/rm_story')
    logging.debug('story_resource: %s', story_resource)

    for _ in range(quantity):
        new_story_payload = {
            "assigned_to": assigned_to,
            "assignment_group": assignment_group,
            "short_description": short_description,
            "sprint": sprint_sys_id,
            "description": description,
            "comments": comments,
            "blocked": blocked,
            "blocked_reason": blocked_reason,
        }
        logging.debug('new_story_payload: %s', new_story_payload)

        try:
            createstory_response = story_resource.create(
                payload=new_story_payload,
            )
            logging.debug('createstory_response: %s', createstory_response)
        except:
            click.secho('error: create story failed, stopping',
                        fg='red', err=True)
            raise

        try:
            createstory_response_one = createstory_response.one()
            logging.debug('createstory_response_one: %s', createstory_response_one)
        except:
            click.secho('error: create story failed, stopping',
                        fg='red', err=True)
            raise

        story = createstory_response_one['number']
        click.secho("success: created story {}".format(story),
                    fg='green', err=False)


if __name__ == '__main__':
    create_story() # pylint: disable=no-value-for-parameter
