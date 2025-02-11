from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from blog import models
from .models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required




def signup(request):
    if request.method == 'POST':
        name = request.POST.get('uname')
        email= request.POST.get('uemail')
        password = request.POST.get('upassword')
        newUser = User.objects.create_user(username=name, email=email, password=password)
        newUser.save()
        return redirect('login-page')
    return render(request, 'blog/signup.html')




def loginn(request):
    if request.method == 'POST':
        name = request.POST.get('uname')
        password = request.POST.get('upassword')
        userr = authenticate(request, username=name, password=password)
        if userr is not None:
            login(request, userr)
            return redirect('/home')
        else:
            return redirect('/login')
    
    if request.user.is_authenticated:
        name = request.user.username
    else:
        name = None

     
    return render(request, 'blog/login.html', {'name': name})




def home(request):
    context = {
        'posts': Post.objects.all(),
        'name': request.user.username if request.user.is_authenticated else None
    }
    return render(request, 'blog/home.html', context)


@login_required
def newPost(request):
    if request.method == 'POST':
        # Get title and content
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        # Get the image file from the request
        image = request.FILES.get('image')  # 'image' is the name of the file input in the form
        
        # Create a new post with the provided data
        npost = models.Post(title=title, content=content, author=request.user, image=image)
        
        # Save the post to the database
        npost.save()
        
        # Redirect to the home page after saving
        return redirect('/home')
    
    return render(request, 'blog/newpost.html')




@login_required
def myPost(request):
    context = {
        'posts': Post.objects.filter(author= request.user)
    }
    return render(request, 'blog/mypost.html', context)



def signout(request):
    logout(request)
    return redirect('login-page')


@login_required
def edit_post(request, id):
    post = get_object_or_404(models.Post, id=id)
    
    if request.method == 'POST':
        # Get updated title and content
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        # Get the new image if provided
        image = request.FILES.get('image')  # 'image' is the name of the input field
        
        # Update the post instance
        post.title = title
        post.content = content
        
        # If a new image is provided, update the image field
        if image:
            post.image = image
        
        # Save the changes to the database
        post.save()
        
        return redirect('/home')  # Redirect after saving

    # Render the edit post form with the current post data
    return render(request, 'blog/edit_post.html', {'post': post})


# Delete post view
@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    
    if request.method == 'POST':
        post.delete()
        return redirect('my-post')  # Redirect to the My Posts page
    
    return render(request, 'blog/delete_post.html', {'post': post})


def read_post(request, id):
    # Get the post by ID or return a 404 if not found
    post = get_object_or_404(Post, id=id)
    
    # Pass the post to the template for rendering
    return render(request, 'blog/read_post.html', {'post': post})
