import uuid
from django.db import models

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
        ('organization', 'Organization'),
        ('committee', 'Committee'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None

class Project(models.Model):
    PROJECT_TYPE_CHOICES = [
        ('website', 'Website'),
        ('web-development', 'Website Development'),
        ('competition', 'Competition'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    project_type = models.CharField(
        max_length=30,
        choices=PROJECT_TYPE_CHOICES,
    )
    thumbnail = models.URLField(blank=True, null=True)
    tag1 = models.CharField(max_length=50, blank=True) #dijadiin max 4 tag aja per project
    tag2 = models.CharField(max_length=50, blank=True)
    tag3 = models.CharField(max_length=50, blank=True)
    tag4 = models.CharField(max_length=50, blank=True)
    detail_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title