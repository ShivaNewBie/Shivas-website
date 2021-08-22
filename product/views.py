from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .forms import ProductForm, RegisterUserForm, CommentForm
# Create your views here.
from .models import *
def home_view(request):
    product = Product.objects.all()
    user = request.user
    context  = {
        'product': product,
        'user':user
    }
    return render(request, 'home.html', context)

@login_required(login_url='product:login-user')
def product_create_view(request):
    form = ProductForm()
    if request.method == 'POST': #If the form has been submitted
        form = ProductForm(request.POST,request.FILES) # A form bound to the POST data
    if form.is_valid():
        instance = form.save(commit=False)
        instance.creator = request.user
        instance.save()
        return redirect('product:user-view')
    context = {
        'form': form
    }
    return render(request, 'product/product_create.html', context )

# def product_comment_view(request):
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         instance = form.save(commit=False)
#         instance.prod = product
#         instance.save()
#         return redirect('product:user-view')
#     context = {
#         'form':form
#     }
#     return render(request,'product/product_comment.html', context)
@login_required(login_url='product:login-user')
def like_post(request):
    user = request.user
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        print(product_id)
        product_instance = Product.objects.get(id=product_id) #get queryset of product id
        print(product_instance)

        if user in product_instance.likes.all():
            product_instance.likes.remove(user)
        else:
            product_instance.likes.add(user)
        like,created = Like.objects.get_or_create(user=user,post_id=product_id)
        print(like)
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()
    return redirect('home-view')
@login_required(login_url='product:login-user')
def product_update_view(request,pk):
    user = request.user
    product = get_object_or_404(Product,id=pk)
    form = ProductForm(request.POST or None,request.FILES or None, instance=product)
    if product.creator != user:
        return HttpResponse('You cannot update this product')
    if request.method == "POST":
        if form.is_valid():
                print(form)
                instance = form.save(commit=False)
                instance.save()
                product = instance
    context = {
        'form': form
    }
    return render(request, "product/product_create.html", context)

def like_view(request, pk):
    return redirect('home-view')

@login_required(login_url='product:login-user')
def product_detail_view(request,pk):
    product = Product.objects.get(id=pk)
    print(product)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.prod = product #save in db or admin
        instance.user = request.user
        instance.save()
        return redirect('.')
    context = {
        'product': product,
        'form':form
    }
    return render(request, 'product/product_detail.html', context)

@login_required(login_url='product:login-user')
def product_delete_view(request, pk):
    user = request.user #get the user anonymous or logged in
    product = get_object_or_404(Product,id=pk)
    if product.creator == user: #if the requested user is == to product.creator
        if request.method == 'POST':
            product.delete()
            return redirect('product:user-view')
    else:
        return HttpResponse('You cannot delete this product')
    context = {
        'product':product
    }
    return render(request, 'product/product_delete.html', context)
@login_required(login_url='product:login-user')
def user_view(request):
    # product = Product.objects.filter(creator__username__startswith='shiva2') this is how you call instance of model with filter. Basically what is happening is we are going to the parent model which is the creator or 'user model' and then go to its object 'username' and find all usernames that startswith the word 'shiva2'
    # product = User.objects.filter(product__prodname='Gun') - give me a user that has a product named gun.
    product = Product.objects.filter(creator=request.user) #looking for id. #creator is the parent table and you are requesting for the user (whether it is anonymous or logged in). because we have login required we will get who is the logged in user with login authentication. Because it is authenticated
    context = {
        'product':product
    }

    return render(request, 'user.html',context)
def register_view(request):
    if request.user.is_authenticated:
        return redirect('product:user-view')
    form = RegisterUserForm()
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('home-view')
    context = {
        'form': form

    }
    return render(request,'product/register.html', context)
def login_user(request):
    if request.user.is_authenticated:
        return redirect('product:user-view')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('product:user-view')
        else:
            messages.info(request,'Username or password is incorrect')
    return render(request,'product/login.html')

def logout_user(request):
    logout(request)
    return redirect('product:login-user')
