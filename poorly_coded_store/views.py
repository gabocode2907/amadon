from django.db.models.expressions import Value
from django.db.models.fields import PositiveBigIntegerField
from django.shortcuts import redirect, render
from .models import Order, Product
from django.db.models import Sum


def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def checkout(request):
    quantity_from_form = int(request.POST["quantity"])
    get_product_price = Product.objects.get(id=request.POST["id"])
    price_from_form = float(get_product_price.price)
    total_charge = quantity_from_form * price_from_form
    print("Charging credit card...")
    new_order = Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)
    
    return redirect("/success/"+str(new_order.id))

def success(request,number):
    submitted_order = Order.objects.get(id=number)
    quantity_from_form = submitted_order.quantity_ordered
    total_charge = submitted_order.total_price
    grand_total = Order.objects.aggregate(total_cost=Sum('total_price'))
    context = {
        'b_quantity' : quantity_from_form,
        'b_total' : total_charge,
        'grand_total' : grand_total,
        'total_items' : Order.objects.aggregate(total_items=Sum('quantity_ordered'))
    }
    return render(request, "store/checkout.html",context)