from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User, auth
from .form import RegistrationForm
from .models import *
import json
from django.contrib import messages

from django.http import JsonResponse
# Create your views here.
from .form import ShippingAddressForm

import datetime

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items' : 0, 'get_cart_total' : 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart1.html', context)
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)




def category_view(request, category):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']

    products = Product.objects.filter(category=category)
    return render(request, 'store/category.html', {'products': products, 'category': category, 'cartItems': cartItems})


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('productId:', productId)
    print('action:', action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        if orderItem.quantity == 0:
            orderItem.quantity += 1
        else:
            pass
        # OrderItem.quantity = (orderItem.quantity+1)
    elif action == 'remove':
        if orderItem.quantity > 0:

            orderItem.quantity -= 1
        #OrderItem.quantity = (orderItem.quantity-1)


    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item added', safe=False)


def register(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']

        user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )

        user.save();

        customer = Customer.objects.create(
                user = user,
                name = user.username,
                email = user.email,
                phone = phone
            )
        customer.save();
        # login(request, user)
        return redirect('/login')
    else:
        return render(request, 'store/register.html')

def login1(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else :
            messages.info(request, 'Invalid Credentials')
            return redirect('/login')

    context = {}
    return render(request, 'store/login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('/')

def product_detail(request, product_id):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']


    context = {'cartItems': cartItems}

    product = Product.objects.get(id=product_id)

    return render(request, 'store/product_detail.html', {'product' : product})

def processOrder(request):
    print('data:', request.body)
    data=json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()


    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total=data['shipping']['total']
        order.transaction_id=transaction_id
        order.complete = True
        order.save()


        '''if total == order.get_cart_total:
            order.complete=True
        order.save() '''


        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
                country=data['shipping']['country'],
                phone=data['shipping']['phone']
            )


    else :
        print('user not logged in')

    items = order.orderitem_set.all()
    cartItems = order.get_cart_items

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return JsonResponse('payment completed', safe=False)




def make_payment(request, order_id):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.order = Order.objects.get(id=order_id)
            shipping_address.save()


    return render(request, 'store/checkout.html', {'form': ShippingAddressForm()})

def myorders(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        #shipping_address = order.shippingaddress_set.first()
        shipping_address = ShippingAddress.objects.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items' : 0, 'get_cart_total' : 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems,'shipping_address': shipping_address}
    return render(request, 'store/orders.html',context)
'''
def completed_orders(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        completed_orders = Order.objects.filter(customer=customer, complete=True)

        order_details = []
        for order in completed_orders:
            items = OrderItem.objects.filter(order=order)
            shipping_address = ShippingAddress.objects.filter(order=order).first()

            order_detail = {
                'order_id': order.id,
                'date_ordered': order.date_ordered,
                'customer_name': request.user.username if order.customer else "Guest",
                'items': [{'name': item.product.name, 'category': item.product.category,
                           'price': item.product.price, 'image': item.product.image.url}
                          for item in items],
                'shipping_address': {
                    'address': shipping_address.address,
                    'city': shipping_address.city,
                    'state': shipping_address.state,
                    'zipcode': shipping_address.zipcode,
                    'country': shipping_address.country,
                    'phone': shipping_address.phone,
                } if shipping_address else None,
            }

            order_details.append(order_detail)

        context = {'order_details': order_details}
        return render(request, 'store/orders.html', context)
    else:
        return render(request, 'store/error_page.html', {'error_message': 'User not logged in'})
    
 '''


# views.py

def completed_orders(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        completed_orders = Order.objects.filter(customer=customer, complete=True)

        order_details = []
        for order in completed_orders:
            items = OrderItem.objects.filter(order=order)

            order_detail = {
                'order_id': order.id,
                'date_ordered': order.date_ordered,
                'customer_name': request.user.username if order.customer else "Guest",
                'items': [{'name': item.product.name, 'category': item.product.category,
                           'price': item.product.price, 'image': item.product.image.url,
                           'shipping_address': item.order.shippingaddress_set.first()}
                          for item in items],
            }

            order_details.append(order_detail)

        context = {'order_details': order_details}
        return render(request, 'store/orders.html', context)
    else:
        return render(request, 'store/error_page.html', {'error_message': 'User not logged in'})
