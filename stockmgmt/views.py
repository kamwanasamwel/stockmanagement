from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockCreateForm, StockSearchForm, StockUpdateForm
from django.contrib import messages

from django.http import HttpResponse
import csv
# Create your views here.


def home(request):
    title = 'Welcome: This is the Home Page'
    context = {
        "title": title,
    }
    return render(request, "home.html", context)


def list_item(request):
    title = 'List of Items'
    queryset = Stock.objects.all()
    form = StockSearchForm(request.POST or None)

    if request.method == 'POST':
        queryset = Stock.objects.filter(
            # category__icontains=form['category'].value(),
            item_name__icontains=form['item_name'].value(
            )
        )

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow(
                    [stock.category, stock.item_name, stock.quantity])
            return response
    context = {
        "form": form,
        "title": title,
        "queryset": queryset,
    }

    return render(request, "list_item.html", context)


def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Succesfully Saved")
        return redirect('/list_item')
    context = {
        "form": form,
        "title": "Add Item",
    }
    return render(request, "add_items.html", context)


def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            return redirect('/list_item')

    context = {
        'form': form
    }
    return render(request, 'add_items.html', context)


def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        return redirect('/list_item')
    return render(request, 'delete_items.html')


def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "title": queryset.item_name,
        "queryset": queryset,
    }
    return render(request, "stock_detail.html", context)
