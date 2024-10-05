from rest_framework import serializers

from contents.models import Content, Author


# For Reading the data from the DB
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class ContentBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'


class ContentSerializer(serializers.Serializer):
    author = AuthorSerializer(read_only=True)
    content = ContentBaseSerializer(read_only=True)


# For Writing the data from third party api to our database
class StatCountSerializer(serializers.Serializer):
    """
    `likes`    : Content -> like_count
    `comments` : Content -> comment_count
    `views`    : Content -> view_count
    `shares`   : Content -> share_count
    """
    likes = serializers.IntegerField()
    comments = serializers.IntegerField()
    views = serializers.IntegerField()
    shares = serializers.IntegerField()


class AuthorPostSerializer(serializers.Serializer):
    """
    unique_name        : Author -> username
    full_name          : Author -> name
    unique_external_id : Author -> unique_id
    url                : Author -> url
    title              : Author -> title
    big_metadata       : Author -> big_metadata
    secret_value       : Author -> secret_value
    """
    unique_name = serializers.CharField()  # Unique name is username
    full_name = serializers.CharField()  # Full name is name
    unique_external_id = serializers.CharField()  # Unique id
    url = serializers.CharField()  # URL of the author
    title = serializers.CharField()  # Title of the author
    big_metadata = serializers.JSONField()  # Metadata
    secret_value = serializers.JSONField()  # Secret value


class ContentPostSerializer(serializers.Serializer):
    unq_external_id = serializers.CharField(required=True)  # Unique id
    stats = StatCountSerializer(required=True)
    author = AuthorPostSerializer(required=True)
    big_metadata = serializers.JSONField()
    secret_value = serializers.JSONField()
    thumbnail_view_url = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    hashtags = serializers.ListField(child=serializers.CharField())
    timestamp = serializers.DateTimeField(required=True)
