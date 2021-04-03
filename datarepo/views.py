from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Category
from django.db import IntegrityError


# Create your views here.
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def product(request):
    if request.method == 'GET':
        product_id = request.GET.get('product_id', None)
        if product_id is None:
            content = {
                'message': 'product_id is mandatory'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                product_info = Product.objects.get(id=product_id)
                content = {
                    'name': product_info.name,
                    'price': product_info.price,
                    'image': product_info.image.url,
                    'category_id': product_info.category_id,
                    'category_name': product_info.category.name,
                    'description': product_info.description,
                    'rating': product_info.rating,

                }
                return Response(content, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                content = {
                    'message': 'product_id is invalid'
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                content = {
                    'message': 'product_id should be integer'
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        category_id = request.POST.get('category_id', None)
        name = request.POST.get('name', None)
        price = request.POST.get('price', None)
        image = request.FILES.get('image', None)
        description = request.POST.get('description', None)
        rating = request.POST.get('rating', None)
        if category_id is None or name is None or price is None:
            content = {
                'message': 'category_id or name or price or image description or rating fields are mandatory'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if name.lstrip() == ' ' is None or category_id is None or price is None or image is None or description is None or rating is None:
            content = {
                'message': 'name  or category_id or price or image or description or rating cannot be empty'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            new_product = Product.objects.create(
                category_id=category_id,
                name=name,
                price=price,
                image=image,
                description=description,
                rating=rating,
            )
            new_product.save()
            content = {
                'data': {
                    'message': 'product has been created',
                    'product_id': new_product.id,
                    'name': new_product.name,
                    'price': new_product.price,
                    'image': new_product.image.url,
                    'description': new_product.description,
                    'rating': new_product.rating,
                    'category_id': new_product.category_id,
                    'category_name': new_product.category.name,
                }
            }
            return Response(content, status=status.HTTP_200_OK)
        except ValueError:
            content = {
                'message': 'price has to be float'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            content = {
                'message': 'invalid category_id'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        new_name = request.POST.get('name', None)
        new_price = request.POST.get('price', None)
        new_category_id = request.POST.get('category_id', None)
        product_id = request.POST.get('product_id', None)
        new_image = request.FILES.get('image', None)
        new_description = request.POST.get('description', None)
        new_rating = request.POST.get('rating', None)
        if product_id is None:
            content = {
                'message': 'product_id is mandatory'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            if new_name is not None and new_name.lstrip() == '':
                content = {
                    'message': 'name cannot be empty'
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            product_info = Product.objects.get(id=product_id)
            product_info.name = new_name if new_name is not None else product_info.name
            product_info.price = new_price if new_price is not None else product_info.price
            product_info.category_id = new_category_id if new_category_id is not None else product_info.category_id
            product_info.image = new_image if new_image is not None else product_info.image
            product_info.description = new_description if new_description is not None else product_info.description
            product_info.rating = new_rating if new_rating is not None else product_info.rating
            product_info.save()
            content = {
                'message': 'product has been updated',
                'data': {
                    'product_id': product_info.id,
                    'name': product_info.name,
                    'price': product_info.price,
                    'image': product_info.image.url,
                    'description': product_info.description,
                    'rating': product_info.rating,
                    'category_id': product_info.category_id,
                    'category_name': product_info.category.name

                }
            }
            return Response(content, status=status.HTTP_201_CREATED)
        except IntegrityError:
            content = {
                'message': 'invalid category id'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            content = {
                'message': 'invalid product id'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            content = {
                'message': str(e)
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        product_id = request.POST.get('product_id', None)
        if product_id is None:
            content = {
                'message': 'product_id is mandatory'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            product_info = Product.objects.get(id=product_id)
            product_info.delete()
            content = {
                'message': 'product has been deleted'
            }
            return Response(content, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            content = {
                'message': 'invalid product id'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            content = {
                'message': 'product id must be an integer'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def products(request):
    print(request.GET)
    category_id = request.GET.get('category_id', None)

    page = int(request.POST.get('page', 0))
    limit = int(request.GET.get('limit', 75))
    print(f'page ---> {page}')
    print(f'limit ---> {limit}')
    if category_id is None:
        all_products = Product.objects.all()
    elif category_id is not None:
        try:
            all_products = Product.objects.filter(category_id=category_id)
        except ValueError:
            content = {
                'message': 'invalid category_id'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    final_products = []
    filtered_products = all_products[(page * limit):(page * limit) + limit]
    for temp_product in filtered_products:
        if temp_product.image:
            image_url = temp_product.image.url
        else:
            image_url = None

        temp = {
            'product_id': temp_product.id,
            'product_name': temp_product.name,
            'product_price': temp_product.price,
            'category_id': temp_product.category_id,
            'category_name': temp_product.category.name,
            'image_url': image_url,
            'description': temp_product.description,
            'rating': temp_product.rating,
        }
        final_products.append(temp)
    content = {
        'products': final_products,
        'page': page,
        'limit': limit,
        'count': len(final_products)
    }
    return Response(content, status=status.HTTP_200_OK)


# category
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def category(request):
    if request.method == 'GET':
        category_id = request.GET.get('category_id', None)
        if category_id is None:
            content = {
                'message': 'category_id is mandatory'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                category_info = Category.objects.get(id=category_id)
                if category_info.image:
                    image = category_info.image.url
                else:
                    image = None
                content = {
                    'name': category_info.name,
                    'image': image,

                }
                return Response(content, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                content = {
                    'message': 'category_id is invalid'
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                content = {
                    'message': 'category_id should be integer'
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        name = request.POST.get('name', None)
        image = request.FILES.get('image', None)
        if name is None or image is None:
            content = {
                'message': 'name or image is missing'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if name.isalpha() is not True:
            content = {
                'message': 'name must be a string'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            new_category = Category.objects.create(
                name=name,
                image=image,
            )
            new_category.save()
            if new_category.image:
                image = new_category.image.url
            else:
                image = None
            content = {
                'data': {
                    'message': 'category has been created',
                    'name': new_category.name,
                    'image': image,
                }
            }
            return Response(content, status=status.HTTP_200_OK)
        except ValueError:
            content = {
                'message': 'name has to be string'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            content = {
                'message': 'invalid category_id'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        new_name = request.POST.get('name', None)
        new_image = request.FILES.get('image', None)
        category_id = request.POST.get('category_id', None)
        if category_id is None:
            content = {
                'message': 'category_id is mandatory'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            if new_name is not None and new_name.lstrip() == '':
                content = {
                    'message': 'name cannot be empty'
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            category_info = Category.objects.get(id=category_id)
            category_info.name = new_name if new_name is not None else category_info.name
            category_info.image = new_image if new_image is not None else category_info.image
            category_info.save()
            if category_info.image:
                image = category_info.image.url
            else:
                image = None
            content = {
                'message': 'category has been updated',
                'data': {
                    'category_id': category_info.id,
                    'name': category_info.name,
                    'image': image,
                }
            }
            return Response(content, status=status.HTTP_201_CREATED)
        except IntegrityError:
            content = {
                'message': 'invalid category id'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            content = {
                'message': 'invalid category id'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            content = {
                'message': str(e)
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        category_id = request.POST.get('category_id', None)
        if category_id is None:
            content = {
                'message': 'category_id is mandatory'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            category_info = Category.objects.get(id=category_id)
            category_info.delete()
            content = {
                'message': 'category has been deleted'
            }
            return Response(content, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            content = {
                'message': 'invalid category_id'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            content = {
                'message': 'category_id must be an integer'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def categories(request):
    all_categories = Category.objects.all()
    content = []
    for category_ in all_categories:
        if category_.image:
            image = category_.image.url
        else:
            image = None
        temp = {
            'category_id': category_.id,
            'category_name': category_.name,
            'image': image,
        }
        content.append(temp)
    return Response(content, status=status.HTTP_200_OK)


@api_view(['GET'])
def categories_details(request):
    category_id = request.GET.get('category_id', None)
    if category_id is None:
        all_categories = Category.objects.all()
    elif category_id is not None:
        try:
            all_categories = Category.objects.filter(id=category_id)
        except ValueError:
            content = {
                'message': 'invalid category id'
            }

    content = []
    for category_ in all_categories:
        all_products = Product.objects.filter(category_id=category_.id)
        products = []
        for item_product in all_products:
            if item_product.image:
                image = item_product.image.url
            else:
                image = None
            temp = {
                'product_id': item_product.id,
                'product_name': item_product.name,
                'description': item_product.description,
                'product_price': item_product.price,
                'image': image,
                'rating': item_product.rating,
            }
            products.append(temp)
            if category_.image:
                image = category_.image.url
            else:
                image = None
        temp = {
            'category_id': category_.id,
            'category_name': category_.name,
            'image': image,
            'products': products,
        }
        content.append(temp)
    return Response(content, status=status.HTTP_200_OK)
