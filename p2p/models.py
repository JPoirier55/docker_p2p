from django.db import models

# Create your models here.


class FileManager(models.Manager):
    def create_file(self, name, location):
        file = self.create(name=name, location=location)
        return file


class File(models.Model):
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
    id = models.IntegerField(primary_key=True)
    hostname = models.CharField(max_length=256)
    ip_address = models.GenericIPAddressField(protocol='IPv4')
    port = models.IntegerField(default=8000)

    class Meta:
        unique_together = ('ip_address', 'port')

    def __str__(self):
        return '{0}-{1}-{2}'.format(str(self.id), self.hostname, self.ip_address)

