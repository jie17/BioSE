from mongoengine import *
import datetime

connect('biose')

class Author(Document):
    name = StringField()

class Journal(Document):
    name = StringField()
    impact_factor = FloatField()
    eigenfactor_score = FloatField()

class Paper(Document):
    title = StringField()
    authors = ListField(ReferenceField(Author))
    abstract = StringField()
    journal = StringField()
    date = DateTimeField()
    url = StringField()
    subscriptions = ListField(ReferenceField('SubscriptionItem'))

    def serialize(self):
        return(
            {
                'Title': self.title,
                'Abstract': self.abstract,
                'URL': self.url,
                'Date': self.date,
                'Journal': self.journal,
                'Authors': [author.name for author in self.authors],
                'DBID': str(self.id)
            }
        )

class SubscriptionItem(Document):
    keyword = StringField()
    papers = ListField(ReferenceField(Paper))

class User(Document):
    username = StringField()
    password = StringField()
    email = StringField()
    subscriptions = ListField(ReferenceField(SubscriptionItem))

class SearchItem(Document):
    keyword = StringField()
    count = IntField(default=0)
    model = BinaryField()
    papers = ListField(ReferenceField(Paper))

class SearchHistory(Document):
    item = ReferenceField(SearchItem)
    user = ReferenceField(User)
    papers = ListField(ReferenceField(Paper))
    created_at = DateTimeField(default=datetime.datetime.now)

class ClickHistory(Document):
    search_item = ReferenceField(SearchItem)
    paper = ReferenceField(Paper)
    count = IntField(default=0)