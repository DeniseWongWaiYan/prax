from django.shortcuts import render

from studentmemberships.models import StudentMembership
from .models import Tutors
# Create your views here.
def tutor_profile(request, slug):
	tutor = Tutors.objects.get(slug=slug)

	context = {
		'tutor': tutor,
		'students': StudentMembership.objects.filter(englishtutor=tutor).all()

	}

	return render(request, "tutors/profile.html", context)