from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Cart, OrderPlaced, Customer
from .forms import CustumerRegistrationForm, CustomerProfilForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProductView(View):
    def get(self, request):
        totalitem = 0
        topmobile = Product.objects.filter(category="M")
        topcomputer = Product.objects.filter(category="PC")
        topipate = Product.objects.filter(category="IP")
        topaccesoire = Product.objects.filter(category="AC")
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        return render(request, 'app/home.html', {"topmobile": topmobile,
                      "topcomputer": topcomputer, "topipate": topipate, "topaccesoire": topaccesoire, "totalitem": totalitem})


class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {"product": product, "item_already_in_cart": item_already_in_cart, "totalitem": totalitem})

        # def home(request):
        #   return render(request, 'app/home.html')
        # def product_detail(request):
        #    return render(request, 'app/productdetail.html')


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
      #  print(cart)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount_price)
                amount += tempamount
                total_amount = amount + shipping_amount

            return render(request, 'app/addtocart.html', {'carts': cart, 'total_amount': total_amount, 'amount': amount, "totalitem": totalitem})
        else:
            return render(request, 'app/emptycart.html')
    # else:
        # return render(request, 'app/emptycart.html')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
    for p in cart_product:

        tempamount = (p.quantity * p.product.discount_price)
        amount += tempamount

    data = {
        'quantity': c.quantity,
        'amount': amount,
        'total_amount': amount + shipping_amount
    }
    return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
    for p in cart_product:

        tempamount = (p.quantity * p.product.discount_price)
        amount += tempamount

    data = {
        'quantity': c.quantity,
        'amount': amount,
        'total_amount': amount + shipping_amount
    }
    return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
    for p in cart_product:

        tempamount = (p.quantity * p.product.discount_price)
        amount += tempamount

    data = {

        'amount': amount,
        'total_amount': amount + shipping_amount
    }
    return JsonResponse(data)


def buy_now(request):
    return render(request, 'app/buynow.html')


# def profile(request):
 #   return render(request, 'app/profile.html')

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {"add": add, 'active': 'btn-primary'})


@login_required
def orders(request):

    op = OrderPlaced.objects.filter(user=request.user)

    return render(request, 'app/orders.html', {'order_placed': op})


def change_password(request):
    return render(request, 'app/changepassword.html')


def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category="M")
    elif data == 'ITEL' or data == 'HUAWEI':
        mobiles = Product.objects.filter(category="M").filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(
            category="M").filter(discount_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(
            category="M").filter(discount_price__gt=10000)

    return render(request, 'app/mobile.html', {'mobiles': mobiles})


def login(request):
    return render(request, 'app/login.html')


# def customerregistration(request):
#    return render(request, 'app/customerregistration.html')


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustumerRegistrationForm()
        return render(request, 'app/customerregistration.html', {"form": form})

    def post(self, request):
        form = CustumerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(
                request, "Congratulation !, registereg successfully")
            form.save()
        return render(request, 'app/customerregistration.html', {"form": form})


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0

    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:

        for p in cart_product:

            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
            total_amount = amount + shipping_amount

    return render(request, 'app/checkout.html', {'add': add, 'cart_items': cart_items, 'total_amount': total_amount})


@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer,
                    product=c.product, quantity=c.quantity).save()
        c.delete()
        return redirect('orders')


@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    def get(self, request):
        form = CustomerProfilForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfilForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            lacality = form.cleaned_data['lacality']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']
            reg = Customer(user=usr, name=name, lacality=lacality,
                           city=city, zipcode=zipcode, state=state,)
            reg.save()
            messages.success(
                request, "Gragratulations, Profil update successfully")
            return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
