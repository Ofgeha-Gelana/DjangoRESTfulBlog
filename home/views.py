from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import BlogSerializer
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Blog
from django.db.models import Q



from django.db.models import Q

from django.db.models import Q

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        try:
            # Filter by user
            blogs = Blog.objects.filter(user=request.user)
            
            # Apply search query if provided
            search_query = request.GET.get('search')
            if search_query:
                search_query = search_query.strip()  # Trim whitespace
                print("Search query:", search_query)  # Debugging
                # Perform case-insensitive search on title and blog_text
                blogs = blogs.filter(Q(title__icontains=search_query) | Q(blog_text__icontains=search_query))
                
            serializer = BlogSerializer(blogs, many=True)
            
            if serializer.data:  # Check if any data is returned
                return Response({
                    'data': serializer.data,
                    'message': 'Blogs retrieved successfully'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'data': [],
                    'message': 'No blogs found matching the search criteria'
                }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            print("Error:", e)
            return Response({
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
    
    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id
            serializer = BlogSerializer(data=data)
            
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong'
                }, status = status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
             
            return Response({
                'data': serializer.data,
                'message': 'Blog created successfully'
            }, status = status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid=data.get('uid'))
            
            if not blog.exists():
                return Response({
                    'data': {},
                    'message': 'Invalid blog uid'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            if request.user != blog[0].user:
                return Response({
                    'data': {},
                    'message': 'You are not the owner of this blog'
                }, status=status.HTTP_400_BAD_REQUEST)
                
                
            serializer = BlogSerializer(blog[0], data=data, partial=True)
            
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong'
                }, status = status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
             
            return Response({
                'data': serializer.data,
                'message': 'Blog updated successfully'
            }, status = status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)
            
            
    def delete(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid = data.get('uid'))
            
            if not blog.exists():
                return Response({
                    'data': {},
                    'message': 'Invalid blog uid'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            if request.user != blog[0].user:
                return Response({
                    'data': {},
                    'message': 'You are not the owner of this blog'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            blog[0].delete()
            
            return Response({
                'data': {},
                'message': 'Blog deleted successfully'
            }, status = status.HTTP_200_OK)
            
        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)