from django.db import models
from lxml import etree

import logging

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
    return Server.parse(xml)
   

class Server(models.Model):
    monitid = models.CharField(max_length=32, unique=True)
    localhostname = models.TextField(unique=True) # possibly unique?
    uptime = models.PositiveIntegerField(null=True)
    version = models.TextField(null=True)

    @property
    def name(self):
        return self.localhostname

    @models.permalink
    def get_absolute_url(self):
        return ('server_detail', [self.name]) 

    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ('can_post_data', 'Can post status data'),
        )
   
    @classmethod
    def parse(cls, xml):
        monitid = find(xml, 'server/id')

        server, created = cls.objects.get_or_create(monitid=monitid,
                                                    defaults={'localhostname': find(xml, 'server/localhostname')})
        
        server.uptime = find(xml, 'server/uptime')
        server.version = find(xml, 'server/version')

        # save so we can get an ID for the childrens' ForeignKeys
        server.save()
        
        for service_xml in xml.findall('service'):
            service_type = find(service_xml, attr='type')
            try:
                service_cls = Service.cls_from_type(service_type)
                service = service_cls.parse(server, service_xml)
                service.save()
            except Service.ServiceTypeNotFound:
                logging.warn('Unknown Service Type, %s' % service_type)

        for event_xml in xml.findall('event'):
            Event.parse(server, event_xml).save()

        return server


class Platform(models.Model):
    server = models.OneToOneField('Server')
    name = models.TextField()
    version = models.TextField()
    machine = models.TextField()
    cpu = models.PositiveIntegerField()
    memory = models.PositiveIntegerField()

STATUS_CHOICES = ((0, 'running'),
                  (512, 'does not exist'),
                  )

class Service(models.Model):
    name = models.TextField(db_index=True)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, null=True)

    # collected_time = 

    class ServiceTypeNotFound(Exception): pass
        
    @classmethod
    def cls_from_type(cls, service_type_code):
        # TODO consider using Python's abc
        for sub in cls.__subclasses__():
            if sub.service_type == int(service_type_code):
                return sub
        raise Service.ServiceTypeNotFound()

    
    @classmethod
    def parse(cls, server, xml):
        name = find(xml, 'name')

        service, created = cls.objects.get_or_create(server=server,
                                                     name=name)

        service.status = find(xml, 'status')

        return service

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
        unique_together = (('server', 'name'),)

class Process(Service):
    server = models.ForeignKey('Server')
    uptime = models.PositiveIntegerField(null=True, blank=True)
    
    # monit type code for processes
    service_type = 3

    @models.permalink
    def get_absolute_url(self):
        return ('process_detail', [self.server.name, self.name]) 

    @classmethod
    def parse(cls, server, xml):
        service = super(Process, cls).parse(server, xml)
        service.uptime = find(xml, 'uptime')
        return service
        

class System(Service):
    server = models.OneToOneField('Server')
    
    # monit type code for systems
    service_type = 5

class Event(models.Model):
    server = models.ForeignKey('Server')
    service = models.TextField()
    state = models.PositiveIntegerField()
    action = models.PositiveIntegerField()
    message = models.TextField()    

    @classmethod
    def parse(cls, server, xml):
        event = cls.objects.create(server=server,
                                   service=find(xml, 'service'),
                                   state=find(xml, 'state'),
                                   action=find(xml, 'action'),
                                   message=find(xml, 'message'))
        return event
