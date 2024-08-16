from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ['watchlist']


class WatchListSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.CharField(source="platform.name")
    # len_names = serializers.SerializerMethodField()

    # def get_len_names(self, obj):
    #     return len(obj.name)

    class Meta:
        model = WatchList
        fields = "__all__"


class StreamPlatformSerializer(serializers.ModelSerializer):
    # class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    # watchlist = serializers.HyperlinkedRelatedField(
    #     view_name='movie-detail', many=True, read_only=True)
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='stream-detail',
    #     lookup_field='id'
    # )
    watchlist = WatchListSerializer(many=True, read_only=True)
    # serializers.HyperlinkedIdentityField(view_name='')
    # watchlist = serializers.HyperlinkedIdentityField(
    #     view_name='watchlist_app.api:movie-detail')
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='movie-detail'
    # )

    class Meta:
        model = StreamPlatform
        lookup_field = 'id'
        fields = "__all__"

    # def validate_name(self, value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is too short")
    #     return value

    # def validate(self, data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError(
    #             "Name and description cannot be same")
    #     return data

# def my_func(value):
#     if len(value) > 50:
#         raise serializers.ValidationError(
#             "Value must be less than 50 characters")


# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     description = serializers.CharField(validators=[my_func])
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get(
#             'description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance

#     def validate_name(self, value):
#         if len(value) < 2:
#             raise serializers.ValidationError("Name is too short")
#         return value

#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError(
#                 "Name and description cannot be same")
#         return data
