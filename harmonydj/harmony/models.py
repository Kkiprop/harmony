from django.db import models


class Amenity(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	icon = models.CharField(max_length=100, blank=True)

	def __str__(self):
		return self.name


class Project(models.Model):
	title = models.CharField(max_length=200, default='HARMONY')
	location = models.CharField(max_length=200, default='Nyali, Mombasa')
	tagline = models.CharField(max_length=255, blank=True, default='Premium 2 & 3 bedroom ensuite apartments with breathtaking ocean views')
	about = models.TextField(blank=True)
	bedrooms = models.CharField(max_length=50, blank=True)
	size_range = models.CharField(max_length=50, blank=True)
	ensuite = models.CharField(max_length=50, blank=True)
	progress = models.PositiveIntegerField(default=65)
	phone = models.CharField(max_length=50, blank=True)
	email = models.EmailField(blank=True)
	address = models.CharField(max_length=255, blank=True)
	amenities = models.ManyToManyField(Amenity, blank=True)
	slug = models.SlugField(default='harmony-nyali', unique=True)

	def __str__(self):
		return self.title


class Enquiry(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='enquiries', null=True, blank=True)
	name = models.CharField(max_length=200)
	email = models.EmailField()
	phone = models.CharField(max_length=50, blank=True)
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'Enquiry from {self.name}'


class Unit(models.Model):
	UNIT_TYPE_CHOICES = [
		('2bed', '2 Bedroom'),
		('3bed', '3 Bedroom'),
	]

	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True)
	unit_type = models.CharField(max_length=10, choices=UNIT_TYPE_CHOICES, default='2bed')
	bedrooms = models.PositiveSmallIntegerField(default=2)
	bathrooms = models.PositiveSmallIntegerField(default=2)
	size_sqm = models.CharField(max_length=50, blank=True)
	size_sqft = models.CharField(max_length=50, blank=True)
	price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	image = models.CharField(max_length=255, blank=True, help_text='Static path under static/, e.g. harmony/Harmony_2_bedroom_floor.png')
	floor_plan = models.CharField(max_length=255, blank=True, help_text='Static path under static/ for the floor plan image')
	# New upload fields (preferred). Keep the old CharField paths for backwards compatibility.
	image_file = models.ImageField(upload_to='units/images/', blank=True, null=True)
	floor_plan_file = models.ImageField(upload_to='units/floor_plans/', blank=True, null=True)
	features = models.TextField(blank=True, help_text='Comma-separated list of features')
	available = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']

	def features_list(self):
		return [f.strip() for f in (self.features or '').split(',') if f.strip()]

	def __str__(self):
		return self.title


class GalleryItem(models.Model):
	MEDIA_CHOICES = [
		('image', 'Image'),
		('video', 'Video'),
	]

	title = models.CharField(max_length=200, blank=True)
	media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES, default='image')
	image_file = models.ImageField(upload_to='gallery/images/', blank=True, null=True)
	vimeo_url = models.CharField(max_length=255, blank=True, help_text='Vimeo URL or video id')
	featured = models.BooleanField(default=False, help_text='Show in homepage preview')
	order = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['order', '-created_at']

	def vimeo_embed_url(self):
		import re
		url = (self.vimeo_url or '').strip()
		if not url:
			return ''
		if re.fullmatch(r'\d+', url):
			return f'https://player.vimeo.com/video/{url}'
		m = re.search(r'vimeo.com/(?:video/)?(\d+)', url)
		if m:
			return f'https://player.vimeo.com/video/{m.group(1)}'
		if 'player.vimeo.com' in url:
			return url
		return ''

	def thumbnail_url(self):
		if self.image_file:
			return self.image_file.url
		return ''

	def __str__(self):
		return self.title or (self.vimeo_url or '')[:30]
