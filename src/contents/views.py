from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from contents.models import Content, Author, Tag, ContentTag
from contents.serializers import ContentSerializer, ContentPostSerializer


class ContentAPIView(APIView):

    def get(self, request):
        """
        TODO: Client is complaining about the app performance, the app is loading very slowly, our QA identified that
         this api is slow af. Make the api performant. Need to add pagination. But cannot use rest framework view set.
         As frontend, app team already using this api, do not change the api schema.
         Need to send some additional data as well,
         --------------------------------
         1. Total Engagement = like_count + comment_count + share_count
         2. Engagement Rate = Total Engagement / Views
         Users are complaining these additional data is wrong.
         Need filter support for client side. Add filters for (author_id, author_username, timeframe )
         For timeframe, the content's timestamp must be withing 'x' days.
         Example: api_url?timeframe=7, will get contents that has timestamp now - '7' days
         --------------------------------
         So things to do:
         1. Make the api performant
         2. Fix the additional data point in the schema
            - Total Engagement = like_count + comment_count + share_count
            - Engagement Rate = Total Engagement / Views
            - Tags: List of tags connected with the content
         3. Filter Support for client side
            - author_id: Author's db id
            - author_username: Author's username
            - timeframe: Content that has timestamp: now - 'x' days
            - tag_id: Tag ID
            - title (insensitive match IE: SQL `ilike %text%`)
         4. Must not change the inner api schema
         5. Remove metadata and secret value from schema
         6. Add pagination
            - Should have page number pagination
            - Should have items per page support in query params
            Example: `api_url?items_per_page=10&page=2`
        """
        query_params = request.query_params.dict()
        tag = query_params.get('tag', None)
        if tag:
            queryset = Content.objects.filter(
                contenttag__tag__name=tag
            ).order_by("-id")[:1000]
        else:
            queryset = Content.objects.all()
        data_list = []
        for query in queryset:
            author = Author.objects.get(id=query.author_id)
            data = {
                "content": query,
                "author": author
            }
            data_list.append(data)
        serialized = ContentSerializer(data_list, many=True)
        for serialized_data in serialized.data:
            # Calculating `Total Engagement`
            # Calculating `Engagement Rate`
            like_count = serialized_data.get("like_count", 0)
            comment_count = serialized_data.get("comment_count", 0)
            share_count = serialized_data.get("share_count", 0)
            view_count = serialized_data.get("view_count", 0)
            total_engagement = like_count + comment_count + share_count
            if view_count > 0:
                engagement_rate = total_engagement / view_count
            else:
                engagement_rate = 0
            serialized_data["content"]["engagement_rate"] = engagement_rate
            serialized_data["content"]["total_engagement"] = total_engagement
            tags = list(
                ContentTag.objects.filter(
                    content_id=serialized_data["content"]["id"]
                ).values_list("tag__name", flat=True)
            )
            serialized_data["content"]["tags"] = tags
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, ):
        """
        TODO: This api is very hard to read, and inefficient.
         The users complaining that the contents they are seeing is not being updated.
         Please find out, why the stats are not being updated.
         ------------------
         Things to change:
         1. This api is hard to read, not developer friendly
         2. Support list, make this api accept list of objects and save it
         3. Fix the users complain
        """

        serializer = ContentPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        author = serializer.validated_data.get("author")
        hashtags = serializer.validated_data.get("hashtags")

        try:
            author_object = Author.objects.get(
                unique_id=author["unique_external_id"]
            )
        except Author.DoesNotExist:
            Author.objects.create(
                username=author["unique_name"],
                name=author["full_name"],
                unique_id=author["unique_external_id"],
                url=author["url"],
                title=author["title"],
                big_metadata=author["big_metadata"],
                secret_value=author["secret_value"],
            )
            author_object = Author.objects.get(
                unique_id=author["unique_external_id"]
            )
            print("Author: ", author_object)

        content = serializer.validated_data

        try:
            content_object = Content.objects.get(
                unique_id=content["unq_external_id"]
            )
        except Content.DoesNotExist:

            Content.objects.create(
                unique_id=content["unq_external_id"],
                author=author_object,
                title=content.get("title"),
                big_metadata=content.get("big_metadata"),
                secret_value=content.get("secret_value"),
                thumbnail_url=content.get("thumbnail_view_url"),
                like_count=content["stats"]["likes"],
                comment_count=content["stats"]["comments"],
                share_count=content["stats"]["shares"],
                view_count=content["stats"]["views"],
            )

            content_object = Content.objects.get(
                unique_id=content["unq_external_id"]
            )
            print("Content: ", content_object)

        for tag in hashtags:
            try:
                tag_object = Tag.objects.get(name=tag)
            except Tag.DoesNotExist:
                Tag.objects.create(name=tag)
                tag_object = Tag.objects.get(name=tag)
                print("Tag Object: ", tag_object)

            try:
                content_tag_object = ContentTag.objects.get(
                    tag=tag_object,
                    content=content_object
                )
                print(content_tag_object)
            except ContentTag.DoesNotExist:
                ContentTag.objects.create(
                    tag=tag_object,
                    content=content_object
                )
                content_tag_object = ContentTag.objects.get(
                    tag=tag_object,
                    content=content_object
                )
                print("Content Object: ", content_tag_object)

        return Response(
            ContentSerializer(
                {
                    "content": content_object,
                    "author": content_object.author,
                }
            ).data,
        )


class ContentStatsAPIView(APIView):
    """
    TODO: This api is taking way too much time to resolve.
     Contents that will be fetched using `ContentAPIView`, we need stats for that
     So it must have the same filters as `ContentAPIView`
     Filter Support for client side
            - author_id: Author's db id
            - author_username: Author's username
            - timeframe: Content that has timestamp: now - 'x' days
            - tag_id: Tag ID
            - title (insensitive match IE: SQL `ilike %text%`)
     -------------------------
     Things To do:
     1. Make the api performant
     2. Fix the additional data point (IE: total engagement, total engagement rate)
     3. Filter Support for client side
         - author_id: Author's db id
         - author_id: Author's db id
         - author_username: Author's username
         - timeframe: Content that has timestamp: now - 'x' days
         - tag_id: Tag ID
         - title (insensitive match IE: SQL `ilike %text%`)
     --------------------------
     Bonus: What changes do we need if we want timezone support?
    """
    def get(self, request):
        query_params = request.query_params.dict()
        tag = query_params.get('tag', None)
        data = {
            "total_likes": 0,
            "total_shares": 0,
            "total_views": 0,
            "total_comments": 0,
            "total_engagement": 0,
            "total_engagement_rate": 0,
            "total_contents": 0,
            "total_followers": 0,
        }
        if tag:
            queryset = Content.objects.filter(
                contentag__tag__name=tag
            )
        else:
            queryset = Content.objects.all()
        for query in queryset:
            data["total_likes"] += query.like_count
            data["total_shares"] += query.share_count
            data["total_comments"] += query.comment_count
            data["total_views"] += query.view_count
            data["total_engagement"] += data["total_likes"] + data["total_shares"] + data["total_comments"]
            data["total_followers"] += query.author.followers
            data["total_contents"] += 1

        return Response(data, status=status.HTTP_201_CREATED)
