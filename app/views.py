
from django.shortcuts import render ,redirect
from django.http import JsonResponse
from django.views import View
import razorpay
from . models import Product, Customer, Cart, OrderPlaced, Payment
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.shortcuts import get_object_or_404



# Create your views here.

def home(request):
    return render(request, "app/home.html")

def about(request):
    return render(request, "app/about.html")

def contact(request):
    return render(request, "app/contact.html")

class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category = val)
        title = Product.objects.filter(category = val).values('title')
        return render(request, 'app/category.html', locals())

class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title = val)
        title = Product.objects.filter(category = product[0].category).values('title')
        return render(request, 'app/category.html', locals())

class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', locals())
        
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html/', locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
           form.save()
           messages.success(request, "Congratulations ! Registration Successfully")
        else:
            messages.warning(request, "Invalid Input data")
        return render(request, 'app/customerregistration.html', locals())

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', locals())
    def post(self, request):
        form= CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']
            reg = Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,zipcode=zipcode,state=state)
            reg.save()
            messages.success(request,'Congratulations! Profile Saved Successfully')
        else:
            messages.warrnig(request,'Invalid Input Data')
        return render(request, 'app/profile.html', locals())

def address(request):
    add = Customer.objects.filter(user = request.user)
    return render(request, 'app/address.html', locals())

class UpdateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/update.html', locals())
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.zipcode = form.cleaned_data['zipcode']
            add.state = form.cleaned_data['state']
            add.save()
            messages.success(request,'Profile Updated Successfully!')
        else:
            messages.warrnig(request,'Invalid Input Data')
        return redirect('address')

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

def showcart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for P in cart:
        value = P.quantity * P.product.discount_price
        amount = amount + value
    totalamount = amount + 40
    return render(request, 'app/addtocart.html', locals())

class Checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for P in cart_items:
            value = P.quantity * P.product.discount_price
            famount = famount + value
        totalamount = famount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_order_status=order_status
            )
            payment.save()
        return render(request, 'app/checkout.html', locals())

def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')

    user = request.user

    # Retrieve customer and payment objects
    customer = Customer.objects.get(id=order_id)
    
    # Create a new Payment object and save payment details
    payment = Payment(
        user=user,
        amount=0,  # You can set the correct amount here
        razorpay_order_id=order_id,
        razorpay_order_status="created",
        razorpay_payment_id=payment_id,
        paid=True
    )
    payment.save()

    # To save order details
    cart_items = Cart.objects.filter(user=user)
    for cart_item in cart_items:
        OrderPlaced.objects.create(
            user=user,
            customer=customer,
            product=cart_item.product,
            quantity=cart_item.quantity,
            payment=payment
        )
        cart_item.delete()

    return redirect("orders")

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user

        # Attempt to retrieve the Cart object or create a new one if it doesn't exist
        c, created = Cart.objects.get_or_create(product_id=prod_id, user=user)

        # Increment the quantity and save the Cart object
        c.quantity += 1
        c.save()

        # Calculate the amount and total amount
        cart = Cart.objects.filter(user=user)
        amount = sum(P.quantity * P.product.discount_price for P in cart)
        totalamount = amount + 40

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user

        # Attempt to retrieve the Cart object or create a new one if it doesn't exist
        c, created = Cart.objects.get_or_create(product_id=prod_id, user=user)

        # Increment the quantity and save the Cart object
        c.quantity -= 1
        c.save()

        # Calculate the amount and total amount
        cart = Cart.objects.filter(user=user)
        amount = sum(P.quantity * P.product.discount_price for P in cart)
        totalamount = amount + 40

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user = user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discount_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)