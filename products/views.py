from django.shortcuts import render
from .models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
# Create your views here.

class pc_products(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        products = Product.objects.filter(section='Pc', status='active')
        product_list = []
        for product in products:
            product_data = {
                'id': product.id,
                'title': product.title,
                'section': product.section,
                'image': request.build_absolute_uri(product.image.url),
                'desc': product.desc,
                'price': str(product.price),
                'avgreview': product.avgreview,
            }
            product_list.append(product_data)
        return Response(product_list, status=status.HTTP_200_OK)
    
class laptop_products(APIView):
    def get(self, request):
        products = Product.objects.filter(section='Laptop', status='active')
        product_list = []
        for product in products:
            product_data = {
                'id': product.id,
                'title': product.title,
                'section': product.section,
                'image': request.build_absolute_uri(product.image.url),
                'desc': product.desc,
                'price': str(product.price),
                'avgreview': product.avgreview,
            }
            product_list.append(product_data)
        return Response(product_list, status=status.HTTP_200_OK)
    
    
class parts_products(APIView):
    def get(self, request):
        products = Product.objects.filter(section='Pc Part', status='active')
        product_list = []
        for product in products:
            product_data = {
                'id': product.id,
                'title': product.title,
                'section': product.section,
                'image': request.build_absolute_uri(product.image.url),
                'desc': product.desc,
                'price': str(product.price),
                'avgreview': product.avgreview,
            }
            product_list.append(product_data)
        return Response(product_list, status=status.HTTP_200_OK)
    
class product_detail(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, status='active')
            product_data = {
                'id': product.id,
                'title': product.title,
                'section': product.section,
                'image': request.build_absolute_uri(product.image.url),
                'desc': product.desc,
                'price': str(product.price),
                'avgreview': product.avgreview,
            }
            return Response(product_data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        

    
class admin_all_products(APIView):
    def get(self, request):
        products = Product.objects.all()
        product_list = []
        for product in products:
            product_data = {
                'id': product.id,
                'title': product.title,
                'section': product.section,
                'image': request.build_absolute_uri(product.image.url),
                'desc': product.desc,
                'price': str(product.price),
                'avgreview': product.avgreview,
                'status': product.status,
            }
            product_list.append(product_data)
        return Response(product_list, status=status.HTTP_200_OK)
    
        
    def post(self, request):
        data = request.data
        title = data.get('title')
        section = data.get('section')
        desc = data.get('desc')
        price = data.get('price')
        status_field = data.get('status', 'active')
        image = request.FILES.get('image')
        
        product = Product.objects.create(
            title=title,
            section=section,
            desc=desc,
            price=price,
            status=status_field,
            image=image
        )
        return Response({'message': 'Product created successfully', 'id': product.id}, status=status.HTTP_201_CREATED)
   
   
class admin_product_detail(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product_data = {
                'id': product.id,
                'title': product.title,
                'section': product.section,
                'image': request.build_absolute_uri(product.image.url),
                'desc': product.desc,
                'price': str(product.price),
                'avgreview': product.avgreview,
                'status': product.status,
                'timestamp':product.created_at,
            }
            return Response(product_data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response({'message': 'Product deleted successfully'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            data = request.data
            product.title = data.get('title', product.title)
            product.section = data.get('section', product.section)
            product.desc = data.get('desc', product.desc)
            product.price = data.get('price', product.price)
            product.status = data.get('status', product.status)
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            product.save()
            return Response({'message': 'Product updated successfully'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
