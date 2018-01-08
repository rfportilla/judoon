'''
Judoon is a validation tool for network switches.  It uses preconfigured tests
to ensure that the script has been properly setup.  You can use the test
templates, but you should ultimately copy them and customize them.  Set an
environment variable, "JUDOON_CONFIG_FOLDER", to the location of the
configuration files.
'''

from shellui.shellui import ShellUI
import netaudit.audit as audit
import netaudit.config as config
#import netaudit.test as auditTests

TEST_TEMPLATE = '/repos/judoon/configs/tests3.yaml'

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
                          'test.'}
                        ],
            [['testGroup'], {'help': 'Required: The name of a preconfigured test'
                             'group.'}],
            [['-f', '--fromfile'], {'help': 'Treat switch name as file path to switch '
                      'configuration.', 'action': 'store_true'}],
        ]
    }

    def roTroNo(self):
        if getattr(self.args, 'fromfile'):
            conf = config.ConfigFile(self.args.switch)
            tests = audit.TestFile()
            tests.load(TEST_TEMPLATE)
            
            auditor = audit.AuditTests(config=conf, tests=tests,
                                                test_group=self.args.testGroup)
            auditor.run()
            for test in auditor.last_results:
                result = 'OK' if test.result else 'FAIL'
                print('%s: %s' % (test.name, result))






if __name__ == '__main__':
    clitool = Judoon()
    clitool.roTroNo()
