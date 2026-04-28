from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.template import engines
from django.http import FileResponse, Http404
import os

from .models import Project, Amenity
from .forms import EnquiryForm
from .models import Unit
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required


def _get_or_create_default_project():
	project = Project.objects.first()
	if not project:
		project = Project.objects.create(
			title='HARMONY',
			location='Nyali, Mombasa',
			tagline='Premium 2 & 3 bedroom ensuite apartments with breathtaking ocean views in the heart of Nyali, Mombasa.',
			about='The project blends modern architecture, high-end finishing and breathtaking ocean views to create an unparalleled living experience. Every detail is meticulously crafted to deliver the ultimate in coastal luxury living.',
			bedrooms='2-3',
			size_range='146-235',
			ensuite='100% Ensuites',
			progress=65,
			phone='0727340340',
			email='exquisiteproperties786@gmail.com',
			address='Nyali, Mombasa, Kenya',
			slug='harmony-nyali',
		)
		amenity_names = ['Parking', 'Swimming Pool', 'Baby Pool', 'Equipped Gym', 'Fire Pit', 'Access Control', 'CCTV', 'Air Conditioning', 'Generator', 'Borehole', 'Sea Views', 'Heat Pumps']
		for name in amenity_names:
			amenity, _ = Amenity.objects.get_or_create(name=name)
			project.amenities.add(amenity)
	return project


def home(request):
	project = _get_or_create_default_project()
	from .forms import EnquiryForm
	# Clear cached template loader so template file edits are picked up
	try:
		for loader in engines['django'].engine.template_loaders:
			if hasattr(loader, 'reset'):
				loader.reset()
	except Exception:
		pass

	form = EnquiryForm()
	return render(request, 'harmony/home.html', {'project': project, 'form': form})


def units_list(request):
	units = Unit.objects.filter(available=True)
	return render(request, 'harmony/units_list.html', {'units': units})


def unit_detail(request, slug):
	unit = get_object_or_404(Unit, slug=slug)
	return render(request, 'harmony/unit_detail.html', {'unit': unit})


@staff_member_required
def units_dashboard(request):
	# Simple dashboard view for admin users to get quick stats and links
	total = Unit.objects.count()
	available = Unit.objects.filter(available=True).count()
	unavailable = total - available
	units = Unit.objects.all().order_by('-created_at')[:10]
	return render(request, 'harmony/units_dashboard.html', {
		'total': total,
		'available': available,
		'unavailable': unavailable,
		'units': units,
	})


def enquire(request):
	project = _get_or_create_default_project()
	if request.method == 'POST':
		form = EnquiryForm(request.POST)
		if form.is_valid():
			enquiry = form.save(commit=False)
			enquiry.project = project
			enquiry.save()
			subject = f'New enquiry from {enquiry.name}'
			message = f'Name: {enquiry.name}\nEmail: {enquiry.email}\nPhone: {enquiry.phone}\n\n{enquiry.message}'
			send_mail(subject, message, enquiry.email, [project.email])
			return render(request, 'harmony/enquire_thanks.html', {'project': project, 'enquiry': enquiry})
	else:
		form = EnquiryForm()
	return render(request, 'harmony/enquire.html', {'form': form, 'project': project})


def hero_image(request):
	"""Serve the hero image directly from disk (development only).

	Looks in the project `static/harmony/hero.png` first, then the app static folder.
	"""
	candidates = [
		os.path.join(settings.BASE_DIR, 'static', 'harmony', 'hero.png'),
		os.path.join(os.path.dirname(__file__), 'static', 'harmony', 'hero.png'),
	]
	for path in candidates:
		if os.path.exists(path):
			return FileResponse(open(path, 'rb'), content_type='image/png')
	raise Http404('hero.png not found')
