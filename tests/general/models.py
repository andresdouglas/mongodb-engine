from django.db import models
from django.conf import settings
from djangotoolbox.fields import ListField, RawField
from django_mongodb_engine.fields import GridFSField, GridFSString

class Blog(models.Model):
    title = models.CharField(max_length=200, db_index=True)

class Post(models.Model):
    title = models.CharField(max_length=200, db_index=True, unique=True)
    content = models.CharField(max_length=1000)
    date_published = models.DateTimeField(null=True, blank=True)
    blog = models.ForeignKey(Blog, null=True, blank=True)

    class MongoMeta:
        descending_indexes = ['title']

class Person(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    age = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("name", "surname")

class DateModel(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    time = models.TimeField(null=True)
    date = models.DateField(null=True)
    _datelist_default = []
    datelist = ListField(models.DateField(), default=_datelist_default)

class RawFieldModel(models.Model):
    raw = RawField()

class IndexTestModel(models.Model):
    regular_index = models.IntegerField(db_index=True)
    custom_column = models.IntegerField(db_column='foo', db_index=True)
    descending_index = models.IntegerField()
    descending_index_custom_column = models.IntegerField(db_column='bar')
    foreignkey_index = models.ForeignKey(Blog, db_index=True)
    foreignkey_custom_column = models.ForeignKey('Post', db_column='spam')
    sparse_index = models.IntegerField(db_index=True)
    sparse_index_unique = models.IntegerField(db_index=True, unique=True)
    sparse_index_cmp_1 = models.IntegerField(db_index=True)
    sparse_index_cmp_2 = models.IntegerField(db_index=True)

    class MongoMeta:
        sparse_indexes = ["sparse_index", "sparse_index_unique", ('sparse_index_cmp_1', 'sparse_index_cmp_2')]
        descending_indexes = ['descending_index', 'descending_index_custom_column']
        index_together = [{ 'fields' : ['regular_index', 'custom_column']},
                          { 'fields' : ('sparse_index_cmp_1', 'sparse_index_cmp_2')}]

class IndexTestModel2(models.Model):
    a = models.IntegerField(db_index=True)
    b = models.IntegerField(db_index=True)

    class MongoMeta:
        index_together = ['a', ('b', -1)]

class GridFSFieldTestModel(models.Model):
    gridfile = GridFSField()
    gridfile_versioned = GridFSField(versioning=True)
    gridfile_nodelete = GridFSField(delete=False)
    gridstring = GridFSString()
