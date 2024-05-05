from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.


class BaseModel(models.Model):
    title = models.CharField(max_length=180,unique=True)
    slug = models.SlugField(unique=True,)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Category(BaseModel):
    class Meta:
        ordering = ('title',)

    def save(self, *args, **kwargs):
        # Auto-generate slug from the title
        if not self.slug:
            self.slug = slugify(self.title)

        super(Category,self).save(*args, **kwargs)


    def get_absolute_url(self):
        return f'{self.slug}'
    


class ArticleManager(models.Manager):
    def get_published_Articles(self):
        return self.filter(status=Article.StatusOptions.PUBLISHED)

    def get_drafts(self):
        return self.filter(status=Article.StatusOptions.DRAFTED)

    def get_hidden_Articles(self):
        return self.filter(status=Article.StatusOptions.HIDEN)

    def get_latest_Articles(self):
        # Get the current time
        now = timezone.now()

        # Calculate the timestamp 24 hours ago
        twentyfour_hrs = now - timezone.timedelta(hours=24)

        # Filter Articles created within the last 24 hours
        return self.filter(status=Article.StatusOptions.PUBLISHED, created_at__gte=twentyfour_hrs)

    def get_image_link(self):
        return self.image.url

class Article(AtrributesAbstract):
    class StatusOptions(models.TextChoices):
        DRAFTED = "D", ("Draft")
        PUBLISHED = "P", ("Publish")
        HIDEN = "H", ("Hide")

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    co_author = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True, related_name='co_authors')
    category = models.ForeignKey(Category,related_name='articles', on_delete=models.CASCADE)
    content = models.TextField()
    status = models.CharField(max_length=1,choices=StatusOptions.choices, default=StatusOptions.DRAFTED)
    related_Articles = models.ManyToManyField('self',blank=True)
    tags = TaggableManager(blank=True)
    image = models.ImageField(upload_to='images/',null=True, blank=True)
    raw_file = models.FileField(upload_to='raw/', null=True, blank=True, storage=RawMediaCloudinaryStorage())
    video = models.FileField(upload_to='videos/',null=True, blank=True, storage=VideoMediaCloudinaryStorage(),validators=[validate_video])
    # custom_field = models.JSONField(default=dict)

    objects = ArticleManager()

    class Meta:
        ordering = ('title','-created_at','-updated_at')

    def save(self, *args, **kwargs):
        # Auto-generate slug from the title and append created_at
        if not self.slug:
            date_suffix = self.created_at.strftime("%m%d%S")
            self.slug = f"{slugify(self.title)}-{date_suffix}"

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f'{self.slug}'
