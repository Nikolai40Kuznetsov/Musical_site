from djongo import models
from django.contrib.auth.models import User

class Song(models.Model):
    _id = models.ObjectIdField(primary_key=True, db_column='_id')
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)
    release_year = models.IntegerField()
    lyrics = models.TextField()
    is_single = models.BooleanField(default=True)
    album_name = models.CharField(max_length=200, null=True, blank=True)
    
    rating = models.FloatField(default=0.0)
    total_votes = models.IntegerField(default=0)
    votes = models.JSONField(default=dict)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'songs'
        ordering = ['-rating', '-total_votes']

    def __str__(self):
        return f"{self.title} - {self.artist}"

    def get_rating_display(self):
        return f"{self.rating:.1f}/10"

    def get_star_rating(self):
        return int(round(self.rating))

    def user_has_voted(self, user_id):
        return str(user_id) in self.votes

    def add_vote(self, user_id, rating_value):
        if str(user_id) in self.votes:
            return False
        self.votes[str(user_id)] = float(rating_value)
        self.total_votes = len(self.votes)
        if self.total_votes > 0:
            self.rating = sum(self.votes.values()) / self.total_votes
        self.save()
        return True
@property
def pk(self):
    return str(self._id)    