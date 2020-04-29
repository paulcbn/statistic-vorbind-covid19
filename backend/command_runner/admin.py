import io
import json
import sys

from django.conf.urls import url
from django.contrib import admin
from django.core.management import call_command, get_commands, load_command_class
from django.template.response import TemplateResponse

from command_runner.models import ManagementCommand


@admin.register(ManagementCommand)
class ManagementCommandsAdmin(admin.ModelAdmin):
    """
    Allows an admin to execute management commands.
    The page will automatically display all management commands in a table.
    """

    class Meta:
        app_label = 'command_runner'
        model_name = "ManagementCommand"

    # modules that should not be displayed
    ignore_modules = ['django.core', 'django.contrib.staticfiles', 'django.contrib.sessions',
                      'django.contrib.contenttypes', 'django.contrib.auth', 'simple_history', "django_extensions",
                      'raven.contrib.django', 'django-rest-framework']

    # commands that should not de displayed
    ignore_commands = []

    def get_urls(self):
        return [url(r'^run/execute/',
                    self.admin_site.admin_view(self.management_execute)),
                url(r'^run/',
                    self.admin_site.admin_view(self.management_view),
                    name="command_runner_managementcommand_changelist"),
                ]

    def management_view(self, request, *args, **kwargs):
        class DummyParser:
            def __init__(self, cmd):
                if cmd is None:
                    return
                self.arguments = []
                cmd.add_arguments(self)

            def add_argument(self, name, nargs='*', type=str, help='',  # pylint:disable=redefined-builtin
                             action=None, default=None, metavar=None, dest=None, choices=None,
                             add_mutually_exclusive_group=None):
                self.arguments.append(
                    {'name': name,
                     'nargs': nargs,
                     'type': type.__name__,
                     'help': help
                     })

            def get_arguments(self):
                return self.arguments

        raw_commands = get_commands()

        commands = []
        modules = []
        for key in raw_commands.keys():
            if raw_commands[key] not in self.ignore_modules:
                module = raw_commands[key]
                name = key

                command = load_command_class(module, name)

                parser = DummyParser(command)
                if module not in modules:
                    modules.append(module)

                if name not in self.ignore_commands:
                    commands.append({
                        'module': module,
                        'command': name,
                        'help': command.help,
                        'arguments': parser.get_arguments(),
                        'css_order': len(commands) % 2 + 1
                    })
        context = {'test': 'test',
                   'opts': self.Meta,
                   'change': False,
                   'is_popup': False,
                   'save_as': False,
                   'has_delete_permission': False,
                   'has_add_permission': False,
                   'has_change_permission': False,
                   'commands': commands,
                   'modules': modules,
                   'results': kwargs.get('results', None),
                   'errors': kwargs.get('errors', None)
                   }

        return TemplateResponse(request, template="admin/management_admin.html", context=context)

    def management_execute(self, request, *args, **kwargs):
        errors = None
        results = ''

        args = tuple()
        kwargs = {}

        if request.method == 'POST':
            raw_json = request.POST.get('json', False)
            if raw_json:
                try:
                    json_dict = json.loads(raw_json)

                    command = json_dict['command']
                    module = json_dict['module']
                    args = json_dict.get('args', [])
                    kwargs = json_dict.get('kwargs', {})

                    if not command:
                        errors = "So...what command should I execute again? (Command not provided)"

                    if module in self.ignore_modules:
                        errors = "You're not allowed to run commands from this module."

                except (json.decoder.JSONDecodeError, KeyError):
                    errors = "Wtf are u doing my dud? Post a [VALID] json ffs."
            else:
                errors = "Wtf are u doing my dud? Post a json ffs."

            if not errors:
                sysout = sys.stdout
                try:
                    sys.stdout = io.StringIO()

                    call_command(command, *args, **kwargs)
                    results = sys.stdout.getvalue() + '\n\rCommand finished execution.'
                    # errors = stderr.getvalue()

                except Exception as e:  # pylint:disable=broad-except
                    errors = f"Exception occurred\n{e}"
                finally:
                    sys.stdout = sysout

        else:
            errors = f'{request.method} not allowed.'
        return self.management_view(request, results=results, errors=errors)
