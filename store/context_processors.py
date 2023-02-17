from .models import Cart, Category
from company.models import AddressBook


def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return {"cart": cart}
    else:
        cart = Cart.objects.all()
        return {"cart": cart}


def category(request):
    categories = Category.objects.filter(is_active=True)
    return {"categories": categories}


def addressbook(request):
    if request.user.is_authenticated:
        addressbook = AddressBook.objects.filter(user=request.user)
        return {"addressbook": addressbook}
    else:
        addressbook = AddressBook.objects.all()
        return {"addressbook": addressbook}
