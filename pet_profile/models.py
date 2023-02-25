from django.db import models
from django.utils.crypto import get_random_string
import uuid
from django.urls import reverse

ANIMALTYPE_CHOICES = (
    ('the one that barks','dog'),
    ('the one that meows', 'cat'),
    ('the one that eats crickets','lizard'),
    ('the one that slithers','snake'),
    ('the one that hops','rabbit/bunny'),
    ('the one that flaps','bird'),
    ('the one that swims','fish'),
    ('the one that croaks','frog'),
)

class Pet(models.Model):
    slug = models.SlugField(max_length = 5, primary_key = True, blank = True, null=False)
    name = models.CharField(max_length = 255, unique = False)
    id = models.CharField(max_length = 261, unique = True, default = uuid.uuid1)
    animaltype = models.CharField(choices = ANIMALTYPE_CHOICES, max_length = 255, default="the one that barks")
    age = models.PositiveIntegerField()
    porofile_photo = models.ImageField(blank = True)

    def save(self, *args, **kwargs):  # new
        slug_save(self)
        get_ID(self)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PetOwner(models.Model):
    slug = models.SlugField(max_length = 5, primary_key = True, blank = True, null=False)
    name = models.CharField(max_length = 255)
    id = models.CharField(max_length = 261, unique = True, default=uuid.uuid1)
    age = models.PositiveIntegerField()
    location = models.CharField(max_length = 255)
    profile_photo = models.ImageField(blank = True)
    pets = models.ManyToManyField(Pet, related_name = "Owners")

    def get_absolute_url(self):
        return reverse("owner_profile", kwargs={"slug": self.slug})  

    def save(self, *args, **kwargs):  # new
        slug_save(self)
        get_ID(self)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

def slug_save(obj):
    """ A function to generate a 5 character slug and see if it has been used and contains naughty words."""
    if not obj.slug: # if there isn't a slug
        obj.slug = get_random_string(5) # create one
        slug_is_wrong = True  
        while slug_is_wrong: # keep checking until we have a valid slug
            slug_is_wrong = False
            other_objs_with_slug = type(obj).objects.filter(slug=obj.slug)
            if len(other_objs_with_slug) > 0:
                # if any other objects have current slug
                slug_is_wrong = True
            #if predict(obj.slug):
            #    slug_is_wrong = True
            if slug_is_wrong:
                # create another slug and check it again
                obj.slug = get_random_string(5)

def get_ID(obj):
    obj.id = obj.name + '-' + obj.slug



class PetPhoto(models.Model):
    url = models.URLField(max_length = 10, primary_key = True, null = False, blank = True, unique = True)
    title = models.CharField(max_length = 255)
    pet = models.ManyToManyField(Pet)
    photo = models.ImageField(blank = True)

    def __str__(self):
        return self.title


class PetStory(models.Model):
    url = models.URLField(max_length = 10, primary_key = True, null = False, blank = True, unique = True)
    title = models.CharField(max_length = 255)
    content = models.TextField(max_length = 1000)
    pet = models.ManyToManyField(Pet)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "PetStories"