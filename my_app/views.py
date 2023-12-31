from django.db import IntegrityError
from django.db.models.aggregates import Avg, Count, Max, Min, Sum
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, HttpResponse
from django.http import HttpRequest, JsonResponse, QueryDict, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
import json

from .models import *
from .serializers import LogInSerializer, UserSerializer, TokenObtainPairSerializer
# Create your views here.


def main(request: HttpRequest):

    if request.method == "POST" and request.FILES["image_file"]:
        image_file = request.FILES["image_file"]
        fs = FileSystemStorage()

        filename = fs.save(image_file.name, image_file)
        image_url = fs.url(filename)
        print(image_url)
        return render(request, "book.html", {
            "image_url": image_url
        })
    return render(request, "book.html")


@csrf_exempt
def register(request: HttpRequest):
    if request.method == 'POST':
        ''
    return HttpResponse('register')


@login_required
def profile(request: HttpRequest):
    ''


class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class LogInView(TokenObtainPairView):
    serializer_class = LogInSerializer


@csrf_exempt
def books(request: HttpRequest):
    """Handling the book endpoint"""
    if (request.method == 'GET'):
        print('get books')
        print(User.objects.all().values())

        # books = Book.objects.all().values()
        # books = Book.objects.filter(title='Thinking Minds')
        # books = Book.objects.filter(price__gt=20)
        # dessending and limit by 2
        # books = Book.objects.order_by('-title')[:2]
        # pagginate
        offset = 0
        limit = 10
        # books = Book.objects.order_by('-title')[offset:limit]
        # Selecting

        books = Book.objects.values('title', 'author', 'price')
        # Read the inner joins or related
        # values('collection__id') => returns the {} dictionary
        # values_list('collection__id') => returns the tuple ('2','Thinking Minds')
        books = Book.objects.values('title', 'author', 'price')
        # return a json - a list of all books
        # status = 200 is the default value
        # return JsonResponse(list(books), safe=False)
        return render(request, 'books.html', {'books': list(books), 'title': "Books"})
    elif request.method == 'POST':
        # for data send as json
        req_body = json.loads(request.body)

        # for Content-Type: application/x-www-form-urlencoded
        # req_body = QueryDict(request.body)

        # for form data - use directly request.POST.get()

        print(req_body)

        title = request.POST.get('title') or req_body.get('title')
        author = request.POST.get('author') or req_body.get('author')
        price = request.POST.get('price') or req_body.get('price')
        inventory = request.POST.get('inventory') or req_body.get('inventory')

        # make entry
        book = Book(title=title, author=author,
                    price=price, inventory=inventory)
        print(title)
        # return JsonResponse(json.loads(request.body))

       # save the entry into db
        try:
            book.save()
        except IntegrityError:
            # 400 - request data is missing
            return JsonResponse({"error": True, "message": "Required fields missing"}, status=400)
        except ValidationError:
            return JsonResponse({"error": True, "message": "invalid values"}, status=400)

        return JsonResponse(model_to_dict(book), status=201)


@csrf_exempt
def book(request: HttpRequest, pk: int):
    """Handling the book endpoint"""
    # find the book element from the db if not exist return 404
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:

        return JsonResponse({"error": True, "message": "Book does not exists"}, status=404)
        # raise Http404('This book does not exist')
    else:
        match request.method:
            case 'GET':  # Get a single book
                return JsonResponse(model_to_dict(book), status=200)
            case 'PUT':  # Update completly

                req_body = QueryDict(request.body)

                title = request.POST.get('title') or req_body.get('title')
                author = request.POST.get('author') or req_body.get('author')
                price = request.POST.get('price') or req_body.get('price')
                inventory = request.POST.get(
                    'inventory') or req_body.get('inventory')

                book.title = title
                book.author = author
                book.price = price
                book.inventory = inventory
                try:
                    book.save()
                except IntegrityError:
                    return JsonResponse({"error": True, "message": "Required fields missing"}, status=400)
                except ValidationError:
                    return JsonResponse({"error": True, "message": "invalid field values"}, status=400)
                return JsonResponse({"message": "updated success", "status": 200, "data": model_to_dict(book)}, status=204)

            case 'DELETE':
                book.delete()
                return JsonResponse({'status': 'The book has been deleted successfully', "status": 200}, status=204)
            case _:
                pass
                return JsonResponse({'error': True, 'message': 'Method Not Allowed - Bad request'}, status=400)
