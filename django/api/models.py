import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import ManyToManyField
from django.utils import timezone
from rules.contrib.models import RulesModel
from django_resized import ResizedImageField


class CustomUserManager(BaseUserManager):
    def _create_user(self, username, email, type, content, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, type=type, content=content, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, type, content, password, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        return self._create_user(username, email, type, content, password, **extra_fields)

    def create_superuser(self, username, email, type, content, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')

        return self._create_user(username, email, type, content, password, **extra_fields)


class Tag(RulesModel):
    name = models.CharField("name", max_length=32, primary_key=True, blank=False, unique=True)

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"
        db_table = "tags"


def get_icon_path(instance, filename):
    return 'icons/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])


class CustomUser(AbstractBaseUser, PermissionsMixin):
    TYPE_TEACHER = "teacher"
    TYPE_STUDENT = "student"
    TYPE_SET = (
        (TYPE_TEACHER, "先生"),
        (TYPE_STUDENT, "生徒")
    )
    CONTENT_YOUTUBE = "youtube"
    CONTENT_VIDEO = "video"
    CONTENT_WEB = "web"
    CONTENT_SET = (
        (CONTENT_YOUTUBE, "YouTube"),
        (CONTENT_VIDEO, "その他動画サイト"),
        (CONTENT_WEB, "ウェブサイト")
    )

    SUBJECT_JAPANESE = "japanese"
    SUBJECT_CONTMP_JP = "contemp_jp"
    SUBJECT_CLASSICS = "classics"

    SUBJECT_ENGLISH = "english"

    SUBJECT_ELEM_MATH = "elem_math"
    SUBJECT_MATH = "math"
    SUBJECT_MATH_1A = "math_1a"
    SUBJECT_MATH_2B = "math_2b"
    SUBJECT_MATH_3 = "math_3"

    SUBJECT_SCIENCE = "science"
    SUBJECT_PHYSICS = "physics"
    SUBJECT_CHEMISTRY = "chemistry"
    SUBJECT_BIOLOGY = "biology"
    SUBJECT_EARTH_SCIENCE = "earth_science"

    SUBJECT_SOCIAL_STUDIES = "social_studies"
    SUBJECT_GEOGRAPHY = "geography"
    SUBJECT_HISTORY = "history"
    SUBJECT_WORLD_HISTORY = "world_history"
    SUBJECT_JP_HISTORY = "jp_history"
    SUBJECT_CIVICS = "civics"
    SUBJECT_CONTMP_SOCIETY = "contmp_society"
    SUBJECT_ETHICS = "ethics"
    SUBJECT_POLITICS_ECONOMY = "politics_economy"

    SUBJECT_ART = "art"
    SUBJECT_HP_EDUCATION = "hp_education"
    SUBJECT_HOME_ECONOMICS = "home_economics"

    SUBJECT_OTHER = "other"

    SUBJECT_SET = (
        (SUBJECT_JAPANESE, "国語"),
        (SUBJECT_CONTMP_JP, "現代文"),
        (SUBJECT_CLASSICS, "古典"),

        (SUBJECT_ENGLISH, "英語"),

        (SUBJECT_ELEM_MATH, "算数"),
        (SUBJECT_MATH, "数学"),
        (SUBJECT_MATH_1A, "数学ⅠA"),
        (SUBJECT_MATH_2B, "数学ⅡB"),
        (SUBJECT_MATH_3, "数学Ⅲ"),

        (SUBJECT_SCIENCE, "理科"),
        (SUBJECT_PHYSICS, "物理"),
        (SUBJECT_CHEMISTRY, "化学"),
        (SUBJECT_BIOLOGY, "生物"),
        (SUBJECT_EARTH_SCIENCE, "地学"),

        (SUBJECT_SOCIAL_STUDIES, "社会"),
        (SUBJECT_GEOGRAPHY, "地理"),
        (SUBJECT_HISTORY, "歴史"),
        (SUBJECT_WORLD_HISTORY, "世界史"),
        (SUBJECT_JP_HISTORY, "日本史"),
        (SUBJECT_CIVICS, "公民"),
        (SUBJECT_CONTMP_SOCIETY, "現代社会"),
        (SUBJECT_ETHICS, "倫理"),
        (SUBJECT_POLITICS_ECONOMY, "政治・経済"),

        (SUBJECT_ART, "芸術"),
        (SUBJECT_HP_EDUCATION, "保健体育"),
        (SUBJECT_HOME_ECONOMICS, "家庭科"),

        (SUBJECT_OTHER, "その他")
    )

    username = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(blank=False, null=False, unique=True)
    introduction = models.CharField(max_length=2048, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    type = models.CharField(choices=TYPE_SET, blank=False, null=False, default=TYPE_STUDENT, max_length=8)
    content = models.CharField(choices=CONTENT_SET, blank=False, null=False, default=CONTENT_YOUTUBE, max_length=16)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    icon = ResizedImageField(upload_to=get_icon_path, null=True, size=[512, 512], crop=["middle", "center"], quality=80, keep_meta=False, force_format="JPEG")
    url = models.URLField(blank=False, null=False)
    tags = ManyToManyField(Tag, related_name="tags", blank=True)
    ordered_tags = ArrayField(models.CharField(max_length=32), blank=True, default=list)
    subjects = ArrayField(models.CharField(choices=SUBJECT_SET, max_length=20), blank=True, default=list)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "type", "content", "url"]

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'users'

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin


class Rating(RulesModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    understandability = models.IntegerField(blank=False, validators=[MinValueValidator(1), MaxValueValidator(5)])
    usefulness = models.IntegerField(blank=False, validators=[MinValueValidator(1), MaxValueValidator(5)])
    fun = models.IntegerField(blank=False, validators=[MinValueValidator(1), MaxValueValidator(5)])
    sum = models.IntegerField(blank=False)
    rater = models.ForeignKey(CustomUser, related_name="rater", blank=False, on_delete=models.CASCADE)
    ratee = models.ForeignKey(CustomUser, related_name="ratee", blank=False, on_delete=models.CASCADE)
    date_rated = models.DateTimeField(default=timezone.now, editable=False)


    class Meta:
        verbose_name = 'rating'
        verbose_name_plural = 'ratings'
        db_table = 'ratings'

    @classmethod
    def check_duplicate(cls, rater, ratee):
        return cls.objects.filter(rater=rater, ratee=ratee).exists()
