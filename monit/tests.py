from django.test import TestCase
from monit.models import *

class CollectTest(TestCase):
    def test_node_startup(self):
        collect(STARTUP_MESSAGE)

        server = Server.objects.get()
        self.assertEqual('4d545e009c94b0697f3a17ee62a9b311', server.monitid)
        self.assertEqual('blueberry', server.localhostname)
        self.assertEqual('5.0.3', server.version)
        self.assertEqual(0, server.uptime)
        self.assertEqual(0, server.service_set.count())
        
    def test_initial_update(self):
        collect(STARTUP_MESSAGE)
        collect(UPDATE_MESSAGE)

        server = Server.objects.get()
        self.assertEqual('4d545e009c94b0697f3a17ee62a9b311', server.monitid)      
        self.assertEqual(1080, server.uptime)
        self.assertEqual(5, server.service_set.count())

        ssh = server.service_set.get(name='sshd')
        self.assertEqual(363503, ssh.uptime)
        self.assertEqual(0, ssh.status)
        self.assertEqual(3, ssh.service_type)

        tomcat = server.service_set.get(name='tomcat')
        self.assertTrue(tomcat.uptime is None)
        self.assertEqual(512, tomcat.status)
        self.assertEqual(3, tomcat.service_type)

        comp = server.service_set.get(name='blueberry')
        self.assertTrue(comp.uptime is None)
        self.assertEqual(0, comp.status)
        self.assertEqual(5, comp.service_type)
        
class CollectorViewTest(TestCase):
    def test_simple_post(self):
        response = self.client.post('/monit/collector',
                                    STARTUP_MESSAGE,
                                    content_type='text/xml')
        self.assertEqual(200, response.status_code)

        server = Server.objects.get()
        self.assertEqual('4d545e009c94b0697f3a17ee62a9b311', server.monitid)      

STARTUP_MESSAGE = """<?xml version="1.0" encoding="ISO-8859-1"?>   
<monit>
        <server>
                <id>4d545e009c94b0697f3a17ee62a9b311</id>
                <incarnation>1269021772</incarnation>
                <version>5.0.3</version>
                <uptime>0</uptime>
                <poll>120</poll>
                <startdelay>0</startdelay>
                <localhostname>blueberry</localhostname>
                <controlfile>/etc/monit/monitrc</controlfile>
                <httpd>
                        <address>localhost</address>
                        <port>2812</port>
                        <ssl>0</ssl>
                </httpd>
        </server>
        <platform>
                <name>Linux</name>
                <release>2.6.31-20-generic</release>
                <version>#57-Ubuntu SMP Mon Feb 8 09:02:26 UTC 2010</version>
                <machine>x86_64</machine>
                <cpu>4</cpu>
                <memory>3926756</memory>
        </platform>
        <event>
                <collected_sec>1269021772</collected_sec>
                <collected_usec>183118</collected_usec>
                <service>Monit</service>
                <type>5</type>
                <group></group>
                <id>65536</id>
                <state>2</state>
                <action>6</action>
                <message>Monit started</message>
        </event>
</monit>"""

UPDATE_MESSAGE = """<?xml version="1.0" encoding="ISO-8859-1"?>
<monit>
        <server>
                <id>4d545e009c94b0697f3a17ee62a9b311</id>
                <incarnation>1269021772</incarnation>
                <version>5.0.3</version>
                <uptime>1080</uptime>
                <poll>120</poll>
                <startdelay>0</startdelay>
                <localhostname>blueberry</localhostname>
                <controlfile>/etc/monit/monitrc</controlfile>
                <httpd>
                        <address>localhost</address>
                        <port>2812</port>
                        <ssl>0</ssl>
                </httpd>
        </server>
        <platform>
                <name>Linux</name>
                <release>2.6.31-20-generic</release>
                <version>#57-Ubuntu SMP Mon Feb 8 09:02:26 UTC 2010</version>
                <machine>x86_64</machine>
                <cpu>4</cpu>
                <memory>3926756</memory>
        </platform>
        <service type="3">
                <collected_sec>1269022852</collected_sec>
                <collected_usec>845730</collected_usec>
                <name>sshd</name>
                <status>0</status>
                <status_hint>0</status_hint>
                <monitor>1</monitor>
                <monitormode>0</monitormode>
                <pendingaction>0</pendingaction>
                <group></group>
                <pid>1417</pid>
                <ppid>1</ppid>
                <uptime>363503</uptime>
                <children>0</children>
                <memory>
                        <percent>0.0</percent>
                        <percenttotal>0.0</percenttotal>
                        <kilobyte>348</kilobyte>
                        <kilobytetotal>348</kilobytetotal>
                </memory>
                <cpu>
                        <percent>0.0</percent>
                        <percenttotal>0.0</percenttotal>
                </cpu>
                <port>
                        <hostname>localhost</hostname>
                        <portnumber>22</portnumber>
                        <request></request>
                        <protocol>SSH</protocol>
                        <type>TCP</type>
                        <responsetime>0.004</responsetime>
                </port>
        </service>
        <service type="3">
                <collected_sec>1269022852</collected_sec>
                <collected_usec>845844</collected_usec>
                <name>postgresql</name>
                <status>0</status>
                <status_hint>0</status_hint>
                <monitor>1</monitor>
                <monitormode>0</monitormode>
                <pendingaction>0</pendingaction>
                <group></group>
                <pid>1561</pid>
                <ppid>1</ppid>
                <uptime>363498</uptime>
                <children>4</children>
                <memory>
                        <percent>0.0</percent>
                        <percenttotal>0.1</percenttotal>
                        <kilobyte>908</kilobyte>
                        <kilobytetotal>5148</kilobytetotal>
                </memory>
                <cpu>
                        <percent>0.0</percent>
                        <percenttotal>0.0</percenttotal>
                </cpu>
                <port>
                        <hostname>127.0.0.1</hostname>
                        <portnumber>5432</portnumber>
                        <request></request>
                        <protocol>DEFAULT</protocol>
                        <type>TCP</type>
                        <responsetime>0.000</responsetime>
                </port>
        </service>
        <service type="3">
                <collected_sec>1269022852</collected_sec>
                <collected_usec>845898</collected_usec>
                <name>tomcat</name>
                <status>512</status>
                <status_hint>0</status_hint>
                <monitor>1</monitor>
                <monitormode>0</monitormode>
                <pendingaction>0</pendingaction>
                <group></group>
                <status_message>process is not running</status_message>
        </service>
        <service type="3">
                <collected_sec>1269022852</collected_sec>
                <collected_usec>847302</collected_usec>
                <name>nginx</name>
                <status>0</status>
                <status_hint>0</status_hint>
                <monitor>1</monitor>
                <monitormode>0</monitormode>
                <pendingaction>0</pendingaction>
                <group></group>
                <pid>30139</pid>
                <ppid>1</ppid>
                <uptime>335774</uptime>
                <children>1</children>
                <memory>
                        <percent>0.0</percent>
                        <percenttotal>0.1</percenttotal>
                        <kilobyte>1676</kilobyte>
                        <kilobytetotal>4828</kilobytetotal>
                </memory>
                <cpu>
                        <percent>0.0</percent>
                        <percenttotal>0.0</percenttotal>
                </cpu>
                <port>
                        <hostname>localhost</hostname>
                        <portnumber>80</portnumber>
                        <request>/</request>
                        <protocol>HTTP</protocol>
                        <type>TCP</type>
                        <responsetime>0.001</responsetime>
                </port>
        </service>
        <service type="5">
                <collected_sec>1269022852</collected_sec>
                <collected_usec>872175</collected_usec>
                <name>blueberry</name>
                <status>0</status>
                <status_hint>0</status_hint>
                <monitor>1</monitor>
                <monitormode>0</monitormode>
                <pendingaction>0</pendingaction>
                <group></group>
                <system>
                        <load>
                                <avg01>0.74</avg01>
                                <avg05>0.28</avg05>
                                <avg15>0.29</avg15>
                        </load>
                        <cpu>   
                                <user>4.4</user>
                                <system>1.4</system>
                                <wait>1.0</wait>
                        </cpu>
                        <memory>
                                <percent>65.6</percent>
                                <kilobyte>2578256</kilobyte>
                        </memory>
                </system>
        </service>
</monit>"""
        


