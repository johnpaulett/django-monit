from django.db import models
from lxml import etree

class Server(models.Model):
    monitid = models.CharField(max_length=32, db_index=True)
    localhostname = models.TextField()
    uptime = models.PositiveIntegerField()
    version = models.TextField()
   
    def process(self, xml):
        self.uptime = find(xml, 'server/uptime')
        self.version = find(xml, 'server/version')
        
        self.save()
        
        for service_elem in xml.findall('service'):
            name = find(service_elem, 'name')

            try:
                service = Service.objects.get(server=self, name=name)
            except Service.DoesNotExist:
                service = Service(server=self, name=name)

            service.process(service_elem)                

    def __unicode__(self):
        return self.localhostname
        
class Platform(models.Model):
    server = models.ForeignKey('Server')
    name = models.TextField()
    version = models.TextField()
    machine = models.TextField()
    cpu = models.PositiveIntegerField()
    memory = models.PositiveIntegerField()

STATUS_CHOICES = ((0, 'running'),
                  (512, 'does not exist'),
                  )

SERVICE_TYPE_CHOICES = ((3, 'Process'),
                        (5, 'System')
                        )

class Service(models.Model):
    server = models.ForeignKey('Server')
    name = models.TextField()
    status = models.PositiveIntegerField(choices=STATUS_CHOICES)
    uptime = models.PositiveIntegerField(null=True, blank=True)
    service_type = models.PositiveIntegerField(choices=SERVICE_TYPE_CHOICES)

    def process(self, xml):
        self.service_type = find(xml, attr='type') # this should not change unless monit is reconfigured and reuses the name
        self.status = find(xml, 'status')
        self.uptime = find(xml, 'uptime')

        self.save()

    def __unicode__(self):
        return self.name
            
class Event(models.Model):
    server = models.ForeignKey('Server')
    service = models.TextField()
    state = models.PositiveIntegerField()
    action = models.PositiveIntegerField()
    message = models.TextField()    

def find(xml, path=None, attr=None):
    if path is None:
        elem = xml
    else:
        elem = xml.find(path)

    if elem is None:
        return None
    
    if attr is not None:
        return elem.get(attr)
    return elem.text

def collect(data):
    xml = etree.fromstring(data)
    monitid = find(xml, 'server/id')
    try:
        server = Server.objects.get(monitid=monitid)
    except Server.DoesNotExist:
        server = Server(monitid=monitid,
                        localhostname=find(xml, 'server/localhostname'))
        
    server.process(xml)
    return server   

