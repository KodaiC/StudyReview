from django.db.models import Count, Avg
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rules.contrib.rest_framework import AutoPermissionViewSetMixin
from django.db.models import F
import isodate

from .serializer import *


class RatingViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    http_method_names = ["get", "post", "head", "delete"]


class TagFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="contains")

    class Meta:
        model = Tag
        fields = ["name"]


class TagViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_class = TagFilter
    http_method_names = ["get", "post", "head"]


class M2MFilter(filters.Filter):
    def filter(self, qs, value):
        if not value:
            return qs

        values = value.split(',')
        for v in values:
            qs = qs.filter(tags=v)
        return qs


class CharArrayFilter(filters.BaseCSVFilter, filters.CharFilter):
    pass


class UserFilter(filters.FilterSet):
    tags = M2MFilter(field_name="tags")
    content = filters.MultipleChoiceFilter(choices=CustomUser.CONTENT_SET)
    subjects = CharArrayFilter(field_name="subjects", lookup_expr="contains")
    understandability = filters.NumberFilter(lookup_expr="gte")
    usefulness = filters.NumberFilter(lookup_expr="gte")
    fun = filters.NumberFilter(lookup_expr="gte")
    count = filters.NumberFilter(lookup_expr="gte")

    class Meta:
        model = CustomUser
        fields = ["tags", "understandability", "usefulness", "fun", "count"]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.none()
    serializer_class = UserSerializer
    filter_class = UserFilter

    def get_queryset(self):
        queryset = CustomUser.objects.filter(is_active=True, is_admin=False)

        if "date_rated" in self.request.query_params:
            offset = isodate.parse_duration(self.request.query_params["date_rated"])
            date = timezone.now() - offset
            queryset = queryset.filter(ratee__date_rated__gte=date)

        queryset = queryset.annotate(
            understandability=Avg("ratee__understandability"),
            usefulness=Avg("ratee__usefulness"),
            fun=Avg("ratee__fun"),
            sum=Avg("ratee__sum"),
            count=Count("ratee")
        ).filter(type="teacher")

        if "random" in self.request.query_params:
            if self.request.query_params["random"]:
                queryset = queryset.order_by("?")

        if "sort" in self.request.query_params:
            sort = self.request.query_params["sort"]
            desc = sort[:1] == "-"
            if desc:
                sort = sort[1:]

            if sort == "understandability" or sort == "usefulness" or sort == "fun" or sort == "sum" or sort == "count" or "date_joined":
                if desc:
                    queryset = queryset.order_by(F(sort).desc(nulls_last=True))
                else:
                    queryset = queryset.order_by(F(sort).asc(nulls_last=True))

        return queryset
