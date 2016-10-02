from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from ..new_login.models import User
from .models import Quotes, QuoteManager

# Create your views here.
def index(request):
    this_user = User.objects.get(id=request.session['id'])
    all_quotes = Quotes.objects.all().order_by('-date_added')
    my_favs = Quotes.objects.filter(fav_quotes=request.session['id'] ).order_by('date_added')

    context={
        'this_user': this_user,
        'all_quotes': all_quotes,
        'my_favs': my_favs
    }
    return render(request, 'matt_app/index.html', context)

def add_quote(request):
    if request.method == 'POST':
        user_id = request.session['id']
        new_quote = Quotes.objects.add_quote(request.POST, user_id)
        if new_quote['created']:
            quote = new_quote['quote']
            messages.success(request, "New Quote successfully Added!")
            return redirect(reverse('quotes:index'))
        else:
            for error in new_quote['errors']:
                messages.error(request, error)
            return redirect(reverse('quotes:index'))

def add_to_favs(request, id):
    if request.method=='POST':
        get_quote = Quotes.objects.get(id=id)
        user_id = request.session['id']
        fav_quote = Quotes.objects.add_favorite(get_quote, user_id)

        if fav_quote['added']:
            messages.success(request, "Added to Favorites")
            fav = fav_quote['quote']
    return redirect(reverse('quotes:index'))


def remove_from_favs(request, id):
    if request.method=='POST':
        get_quote = Quotes.objects.get(id=id)
        user_id = request.session['id']
        remove_quote = Quotes.objects.remove_favorite(get_quote, user_id)
        if remove_quote['removed']:
            messages.success(request, "Removed from List")
        return redirect(reverse('quotes:index'))

def show_user(request, id):
    this_user = User.objects.get(id=id)
    quotes = Quotes.objects.filter(added_by=id)
    context = {
        'this_user': this_user,
        'quotes_added': quotes
    }
    return render(request, 'matt_app/user_quotes.html', context)


def logOut(request):
    request.session.clear()
    return redirect(reverse('users:index'))
