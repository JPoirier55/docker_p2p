"""
    Docker peer to peer network
    Author: Jake Poirier
    ECE495 Independent study project
    Colorado State University
    November 1, 2016
"""


from django.db import models

# Create your models here.


class FileManager(models.Manager):
    """
        Wrapper to quickly create a file
    """
    def create_file(self, name, location):
        file = self.create(name=name, location=location)
        return file


class SplitFile(models.Model):
    """
        Table to split file into pieces across
        multiple nodes
    """
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    node1 = models.GenericIPAddressField(protocol='IPv4')
    node2 = models.GenericIPAddressField(protocol='IPv4')
    port1 = models.IntegerField(default=65000)
    port2 = models.IntegerField(default=65001)
    objects = FileManager()

    def __str__(self):
        return '{0}-{1}-{2}:{3}-{4}:{5}'.format(str(self.id), self.name, self.node1, self.port1, self.node2, self.port2)


class File(models.Model):
    """
        Table for all file data
    """
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)

    # TODO Add type of file: ex. text/plain, application/s.xml etc

    FICTION = 'Fiction'
    NONFICTION = 'Non-Fiction'
    TECHNICAL = 'Technical'
    BIOGRAPHY = 'Biography'
    SUBJECT = (
        (FICTION, 'Fiction'),
        (NONFICTION, 'Non-Fiction'),
        (TECHNICAL, 'Technical'),
        (BIOGRAPHY, 'Biography')
    )
    category = models.CharField(
        max_length=10,
        choices=SUBJECT,
        default=FICTION,
    )
    location = models.CharField(max_length=256)

    objects = FileManager()

    def __str__(self):
        return '{0}-{1}-{2}-{3}'.format(str(self.id), self.name, self.category, self.location)


class Neighbors(models.Model):
    """
        Table for indexing neighboring nodes to the system
    """
    id = models.IntegerField(primary_key=True)
    hostname = models.CharField(max_length=256)
    ip_address = models.GenericIPAddressField(protocol='IPv4')
    port = models.IntegerField(default=8000)

    class Meta:
        unique_together = ('ip_address', 'port')

    def __str__(self):
        return '{0}-{1}-{2}'.format(str(self.id), self.hostname, self.ip_address)


class FileNodes(models.Model):
    id = models.IntegerField(primary_key=True)
    hostname1 = models.CharField(max_length=256)
    ip_address1 = models.GenericIPAddressField(protocol='IPv4')
    port1 = models.IntegerField(default=8000)
    hostname2 = models.CharField(max_length=256)
    ip_address2 = models.GenericIPAddressField(protocol='IPv4')
    port2 = models.IntegerField(default=8000)

    class Meta:
        unique_together = (('ip_address1', 'port1'),('ip_address2', 'port2'))

    def __str__(self):
        return '{0}-FIRST:{1}-{2}-SECOND:{3}-{4}'.format(str(self.id), self.hostname1, self.ip_address1, self.hostname2, self.ip_address2)