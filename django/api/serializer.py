from rest_framework import serializers
import re
from collections import OrderedDict

from .models import *


class RatingSerializer(serializers.ModelSerializer):
    rater = serializers.HiddenField(default=serializers.CurrentUserDefault())
    ratee_name = serializers.SerializerMethodField()

    def get_ratee_name(self, obj):
        return obj.ratee.username

    def validate(self, data):
        if data["rater"] == data["ratee"]:
            raise serializers.ValidationError("You can\'t rate yourself")
        if data["rater"].type == "teacher":
            raise serializers.ValidationError("Teacher can\'t rate")
        if data["ratee"].type == "student":
            raise serializers.ValidationError("Student can\'t be rate")
        if Rating.check_duplicate(rater=data["rater"], ratee=data["ratee"]):
            raise serializers.ValidationError("You can\'t rate more than once")
        if data["sum"] != data["understandability"] + data["usefulness"] + data["fun"]:
            raise serializers.ValidationError("The value of 'sum' is illegal")
        return data

    class Meta:
        model = Rating
        fields = ("id", "understandability", "usefulness", "fun", "sum", "ratee", "ratee_name", "rater", "date_rated")


class TagSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    def validate_name(self, name):
        return re.sub("\s", "", name)

    def get_users(self, obj):
        users_content = UserIDSerializer(CustomUser.objects.all().filter(tags__name__icontains=obj.name), many=True).data
        return users_content

    class Meta:
        model = Tag
        fields = ("name", "users")


class UserIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", )


class UserSerializer(serializers.ModelSerializer):
    understandability = serializers.FloatField()
    usefulness = serializers.FloatField()
    fun = serializers.FloatField()
    understandability_dist = serializers.SerializerMethodField()
    usefulness_dist = serializers.SerializerMethodField()
    fun_dist = serializers.SerializerMethodField()
    sum = serializers.FloatField()
    count = serializers.IntegerField()

    def get_understandability_dist(self, obj):
        understandability_dist_content = OrderedDict()
        for i in range(5, 0, -1):
            understandability_dist_content[i] = Rating.objects.filter(ratee__id=obj.id, understandability=i).count()
        return understandability_dist_content

    def get_usefulness_dist(self, obj):
        usefulness_dist_content = OrderedDict()
        for i in range(5, 0, -1):
            usefulness_dist_content[i] = Rating.objects.filter(ratee__id=obj.id, usefulness=i).count()
        return usefulness_dist_content

    def get_fun_dist(self, obj):
        fun_dist_content = OrderedDict()
        for i in range(5, 0, -1):
            fun_dist_content[i] = Rating.objects.filter(ratee__id=obj.id, fun=i).count()
        return fun_dist_content

    class Meta:
        model = CustomUser
        fields = ("id", "username", "introduction", "type", "content", "icon", "url", "tags", "ordered_tags", "subjects", "understandability", "usefulness", "fun", "understandability_dist", "usefulness_dist", "fun_dist", "sum", "count", "date_joined")


class MeSerializer(serializers.ModelSerializer):
    ratings = serializers.SerializerMethodField()
    rated = serializers.SerializerMethodField()
    tags = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)
    type = serializers.SerializerMethodField()

    def validate_ordered_tags(self, ordered_tags):
        result = []
        for n in ordered_tags:
            name = re.sub("\s", "", n)
            if name not in result:
                result.append(name)

        return result

    def validate_subjects(self, subjects):
        result = []
        for subject in subjects:
            if subject not in result:
                result.append(subject)

        return result

    def update(self, instance, validated_data):
        user = super().update(instance=instance, validated_data=validated_data)

        if "ordered_tags" in validated_data:
            tags = []
            tag_names = validated_data.pop("ordered_tags")
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(name=re.sub("\s", "", name))
                tags.append(tag)
            user.tags.set(tags)

        return user

    def get_ratings(self, obj):
        ratings_content = RatingSerializer(Rating.objects.all().filter(ratee=CustomUser.objects.get(id=obj.id)), many=True).data
        return ratings_content

    def get_rated(self, obj):
        rated_content = RatingSerializer(Rating.objects.all().filter(rater=CustomUser.objects.get(id=obj.id)), many=True).data
        return rated_content

    def get_type(self, obj):
        return obj.type

    class Meta:
        model = CustomUser
        fields = ("id", "email", "username", "introduction", "type", "content", "icon", "url", "tags", "ordered_tags", "subjects", "ratings", "rated")
