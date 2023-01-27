from plugin.utils import extract_body_measurements, compare_measurements
from django.core.files.storage import default_storage
from django.shortcuts import render

# Create your views here.
# myapp/views.py

from django.http import HttpResponse
from .models import Customer, Clothing
from .forms import ImageUploadForm


def index(request):
    form = ImageUploadForm()
    return render(request, 'plugin/index.html', {'form': form})


def size_recommendation(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the image to the database
            customer = Customer.objects.create(
                image=form.cleaned_data['image'])
            # Use the machine learning model to extract the body measurements
            body_measurements = extract_body_measurements(customer.image)
            customer.update(body_measurements=body_measurements)

            # Compare the body measurements with the clothing measurements
            clothing_measurements = Clothing.objects.all()
            recommendations = compare_measurements(
                body_measurements, clothing_measurements)

            # Display the recommendations to the user
            return render(request, 'plugin/recommendations.html', {'recommendations': recommendations})
    else:
        form = ImageUploadForm()
    return render(request, 'plugin/index.html', {'form': form})


def image_upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['image']
            # Save the image to the server
            image_path = default_storage.save('customers/' + image.name, image)
            # Extract the body measurements
            body_measurements = extract_body_measurements(image_path)
            # Get the recommendations
            clothing_measurements = Clothing.objects.all()
            recommendations = compare_measurements(
                body_measurements, clothing_measurements)
            # Render the recommendations
            return render(request, 'plugin/recommendations.html', {'recommendations': recommendations})
    else:
        form = ImageUploadForm()
    return render(request, 'plugin/image_upload.html', {'form': form})
