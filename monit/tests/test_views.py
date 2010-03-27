from django.test import TestCase
from monit.models import *

class ServersViewTest(TestCase):
    def setUp(self):
        server = Server.objects.create(monitid='1',
                                       localhostname='raspberry')

        Process.objects.create(server=server, name='sshd')
        Process.objects.create(server=server, name='nginx')
        
        Server.objects.create(monitid='2',
                              localhostname='blueberry')
        
    def test_servers_list(self):
        response = self.client.get('/monit/servers/')
        self.assertContains(response, 'blueberry')
        self.assertContains(response, 'raspberry')

    def test_server_detail(self):
        response = self.client.get('/monit/servers/raspberry/')
        self.assertContains(response, 'raspberry')
        self.assertContains(response, 'sshd')
        self.assertContains(response, 'nginx')

    def test_process_detail(self):
        response = self.client.get('/monit/servers/raspberry/processes/sshd/')
        self.assertContains(response, 'raspberry')
        self.assertContains(response, 'sshd')
