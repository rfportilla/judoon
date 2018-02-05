'''
Judoon is a validation tool for network switches.  It uses preconfigured tests
to ensure that the script has been properly setup.  You can use the test
templates, but you should ultimately copy them and customize them.  Set an
environment variable, "JUDOON_CONFIG_FOLDER", to the location of the
configuration files.
'''

import re

from shellui.shellui import ShellUI
import netaudit.audit as audit
import netaudit.config as config
import netaudit.connect as connect

TEST_TEMPLATE = '../configs/tests4.yaml'
SSH = 'ssh'
TELNET = 'telnet'
CMD_TIMEOUT = 1

class Judoon(ShellUI):
  """
  Shell script utility to audit switch and compare with baseline settings.
  """

  helpattr = {
    'argparseattr': {
      'description': ('This is a validation script to ensure that the '
      'network configuration is correction.')
    },
    'args': [
      [['switch'], {'help': 'Required: The name or IP of the switch to '
                    'test.'}],
      [['testGroup'], {'help': 'Required: The name of a preconfigured test'
        'group.'}],
      [['-f', '--fromfile'], {'help': 'Treat switch name as file path to switch '
        'configuration.', 'action': 'store_true', 'default': False}],
      [['-t', '--type'], {'help': 'Device type of remote connected host.  This '
        'may affect interaction with the host such as authentication over '
        'telnet, etc.', 'choices': ['cisco']}],
      [['-u', '--username'], {'help': 'Optional: Username to connect to remote '
        'host.  Used with ssh or telnet connection.'}],
      [['-p', '--password'], {'help': 'Optional: Password to connect to remote '
        'host.  Used with ssh or telnet connection.'}],
      [['-e', '--elev_password'], {'help': 'Optional: Elevated password, used on '
        'some devices as secondary authentication for privileged access.'}],
    ]
  }

  def roTroNo(self):
    proto_group = self.parser.add_mutually_exclusive_group()
    proto_group.add_argument('--telnet', help='Connect to switch via '
      'telnet.', dest='proto', action='store_const', const=TELNET, default=SSH)
    proto_group.add_argument('--ssh', help='Connect to switch via ssh.',
      dest='proto', action='store_const', const='ssh', default=SSH)
    args = self.args

    #Load test definition
    tests = audit.TestFile()
    tests.load(TEST_TEMPLATE)

    if args.fromfile:
      conf = config.ConfigFile(self.args.switch)
      auditor = audit.AuditTestsConfig(config=conf, tests=tests,
                                       test_group=self.args.testGroup)
    else:
      connect_args = {
        'hostname': args.switch,
        'username': args.username,
        'password': args.password,
      }
      if args.proto == TELNET:
        print('Doing TELNET')
        client = connect.Telnet_Client(**connect_args)
        client.connect()
        if args.type is not None and args.type.lower() == 'cisco':
          if re.search('Password: ', client.last_response):
            client.send_command(args.password)
          client.send_command('term len 0', CMD_TIMEOUT)
          if re.search('>$', client.last_response):
            #Enter enable mode
            client.send_command('enable', CMD_TIMEOUT)
            if re.search('Password', client.last_response):
              client.send_command(args.elev_password, CMD_TIMEOUT)
      elif args.proto == SSH:
        print('Doing SSH')
        client = connect.SSH_Client(**connect_args)
        client.connect()
        if args.type is not None and args.type.lower() == 'cisco':
          client.send_command('term len 0', CMD_TIMEOUT)
          if re.search('>$', client.last_response):
            #Enter enable mode
            client.send_command('enable', CMD_TIMEOUT)
            if re.search('Password', client.last_response):
              client.send_command(args.elev_password, CMD_TIMEOUT)
      auditor = audit.AuditTestsClient(client=client, tests=tests,
                                       test_group=self.args.testGroup)
        
      
      
    auditor.run()
    for test in auditor.last_results:
      if test.result is True:
        result = 'OK'
      elif (test.message is not None
            and re.search('skipped', test.message, re.I)):
        result = 'Skipped'
      else:
        result = 'FAIL'
      print('%s: %s' % (test.name, result))






if __name__ == '__main__':
  clitool = Judoon()
  clitool.roTroNo()
