import datetime
from django.utils import timezone
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.generic import ListView
from .models import Post
from .forms import PostForm, LoginForm
from geopy.geocoders import Nominatim
import django.contrib.auth as auth
import os
from sys import platform

def home(request):
	# TODO: move this token to Django settings from an environment variable
    # found in the Mapbox account settings and getting started instructions
    # see https://www.mapbox.com/account/ under the "Access tokens" section
    mapbox_access_token = 'pk.eyJ1Ijoid2hzYXBwIiwiYSI6ImNrMmVhdG10cDA3bW0zb24wOHN4N3d5cmkifQ._NMZTI2kKSLY5RWfNRYY7A'
    print(os.getcwd());
    context = {
        'mapbox_access_token': mapbox_access_token,'posts': Post.objects.all()
    }
    return render(request, 'whsapp/home.html', context)

class PostListView(ListView):
  model = Post
  template_name = 'whsapp/home.html' # FOLLOW THIS NAMING SCHEME <app>/<model>_<viewtype>.html
  context_object_name = 'posts'
  ordering = ['-created_date']
  def get_ordering(self):
    ordering = self.request.GET.get('ordering','-created_date') #Order live feed events according to closest start date events at the top
    return ordering

def register(request):
    return render(request, 'whsapp/register.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('whsapp-home')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = auth.authenticate(request, username=username, password=raw_password)
            if user is not None:
                auth.login(request, user)
                return redirect('whsapp-home')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', { 'form': form })

def signup(request):
    if request.user.is_authenticated:
        return redirect('whsapp-home')
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user= form.save(commit=False)
                user.active=True
                user.staff=False
                user.admin=False
                user.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password')
                user = auth.authenticate(request, username=username, password=raw_password)
                if user is not None:
                    auth.login(request, user)
                    return redirect('whsapp-home')
                return redirect('login')
        else:
            form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def logout(request):
    auth.logout(request)
    return redirect('whsapp-home')

def test(request):
    return render(request, 'whsapp/test.txt')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'whsapp/post_detail.html', {'post': post})

def post_new(request):
    if not request.user.is_authenticated:
        return redirect('whsapp-home')
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.host_id = request.user.id
            post.save()

            data = Post.objects.all()
            num = data.count()
            counter = 1
            filepath = os.path.dirname(os.getcwd().replace('\\', '/')) + "/whs/whsapp/templates/whsapp/test.txt"
            if platform == "linux" or platform == "linux2":
                filepath = os.path.dirname(os.getcwd().replace('\\', '/')) + "home/evanmrettman/CS321/whs/whsapp/templates/whsapp/test.txt"
            file = open(filepath,"w")
            file.write('{"features":[')
            geolocator=Nominatim()
            li = ['a']
            for d in data:
                print(d.address)
                location = geolocator.geocode(d.address, timeout=10)
                file.write('{"type": "Feature",')
                file.write('"properties": {')
                file.write('"title": "'+ d.title + '",')
                file.write('"description": "<strong>Hour: </strong>'+ str(d.start_time) + ' - ' + str(d.end_time) + '<br> <strong>From:</strong> ' + str(d.start_date) + ' <strong>To:</strong> ' + str(d.end_date) + '<br><p>' + d.description + '</p>", "Pict":"' + str(d.event_logo) + '"},')
                str1 = location.longitude
                str2 = location.latitude
                if (str(str1) + ',' + str(str2)) not in li:
                    file.write('"geometry": { "coordinates": [ '+ (str(str1) + ',' + str(str2)))
                else:
                    while (str(str1) + ',' + str(str2)) in li:
                        str1 += 0.0000000599
                        str2 += 0.00000599
                    file.write('"geometry": { "coordinates": [ '+ str(str1) + ',' + str(str2))
                li.append(str(str1) + ',' + str(str2))
                file.write('], "type": "Point" } }')
                if counter != num:
                    file.write(',')
                counter += 1
            file.write('], "type": "FeatureCollection"}')
            file.close()

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'whsapp/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = Post.objects.get(pk=pk)
    if post is None:
        return redirect('whsapp-home')
    if not request.user.is_authenticated and not (request.user.is_staff or request.user.id is post.host_id):
        return redirect('post_detail', pk=post.pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.host_id = request.user.id
            post.save()

            data = Post.objects.all()
            num = data.count()
            counter = 1
            filepath = os.path.dirname(os.getcwd().replace('\\', '/')) + "/whs/whsapp/templates/whsapp/test.txt"
            if platform == "linux" or platform == "linux2":
                filepath = os.path.dirname(os.getcwd().replace('\\', '/')) + "home/evanmrettman/CS321/whs/whsapp/templates/whsapp/test.txt"
            file = open(filepath,"w")
            file.write('{"features":[')
            geolocator=Nominatim()
            li = ['a']
            for d in data:
                print(d.address)
                location = geolocator.geocode(d.address, timeout=10)
                file.write('{"type": "Feature",')
                file.write('"properties": {')
                file.write('"title": "'+ d.title + '",')
                file.write('"description": "<strong>Hour: </strong>'+ str(d.start_time) + ' - ' + str(d.end_time) + '<br> <strong>From:</strong> ' + str(d.start_date) + ' <strong>To:</strong> ' + str(d.end_date) + '<br><p>' + d.description + '</p>", "Pict":"' + str(d.event_logo) + '"},')
                str1 = location.longitude
                str2 = location.latitude
                if (str(str1) + ',' + str(str2)) not in li:
                    file.write('"geometry": { "coordinates": [ '+ (str(str1) + ',' + str(str2)))
                else:
                    while (str(str1) + ',' + str(str2)) in li:
                        str1 += 0.0000000599
                        str2 += 0.00000599
                    file.write('"geometry": { "coordinates": [ '+ str(str1) + ',' + str(str2))
                li.append(str(str1) + ',' + str(str2))
                file.write('], "type": "Point" } }')
                if counter != num:
                    file.write(',')
                counter += 1
            file.write('], "type": "FeatureCollection"}')
            file.close()

            return redirect('post_detail', pk=post.pk)
    else:
	    form = PostForm(instance=post)
    return render(request, 'whsapp/post_edit.html', {'form': form})