from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields.related import ManyToManyField

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import has_permissions

from site_settings.models import Testimonial
from site_settings.serializers import TestimonialSerializer, TestimonialListSerializer

from commons.pagination import Pagination
from commons.enums import PermissionEnum
from rest_framework.permissions import AllowAny
import datetime
from django.db.models import Q

from django.http import JsonResponse

from site_settings.utils import normalize_search_query


# Create your views here.

@extend_schema(
    parameters=[
        OpenApiParameter("page"),
        OpenApiParameter("size"),
  ],
    request=TestimonialListSerializer,
    responses=TestimonialListSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_LIST.name])
def getAllTestimonial(request):
    testimonials = Testimonial.objects.all()
    total_elements = testimonials.count()

    search_query = normalize_search_query(request.query_params.get('searchKey', ''))
    if search_query:
        testimonials = Testimonial.objects.filter(
            Q(name__icontains=search_query)
        )
    else:
        total_elements = testimonials.count()


    page = request.query_params.get('page')
    size = request.query_params.get('size')

    # Pagination
    pagination = Pagination()
    pagination.page = page
    pagination.size = size
    testimonials = pagination.paginate_data(testimonials)

    serializer = TestimonialListSerializer(testimonials, many=True)

    response = {
        'testimonials': serializer.data,
        'page': pagination.page,
        'size': pagination.size,
        'total_pages': pagination.total_pages,
        'total_elements': total_elements,
    }

    return Response(response, status=status.HTTP_200_OK)







@extend_schema(request=TestimonialSerializer, responses=TestimonialSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_DETAILS.name])
def getATestimonial(request, pk):
    try:
        testimonial = Testimonial.objects.get(pk=pk)
        serializer = TestimonialSerializer(testimonial)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'detail': f"Testimonial id - {pk} does't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=TestimonialSerializer, responses=TestimonialSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_CREATE.name])
def createTestimonial(request):
    data = request.data
    print('data: ', data)
    print('content_type: ', request.content_type)

    filtered_data = {}

    for key, value in data.items():
        if value != '' and value != '0':
            filtered_data[key] = value
    
    print('filtered_data: ', filtered_data)
    
    serializer = TestimonialSerializer(data=filtered_data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)




@extend_schema(request=TestimonialSerializer, responses=TestimonialSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_UPDATE.name])
def updateTestimonial(request, pk):
    data = request.data
    filtered_data = {}

    try:
        testimonial_obj = Testimonial.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response({'detail': f"Testimonial id - {pk} doesn't exists"})

    for key, value in data.items():
        if value != '' and value != '0':
            filtered_data[key] = value

    print('filtered_data: ', filtered_data)

    image = filtered_data.get('image', None)

    if image is not None and type(image) == str:
        popped_image = filtered_data.pop('image')
    
    serializer = TestimonialSerializer(testimonial_obj, data=filtered_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors)
    




@extend_schema(request=TestimonialSerializer, responses=TestimonialSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_DELETE.name])
def deleteTestimonial(request, pk):
    try:
        testimonial = Testimonial.objects.get(pk=pk)
        testimonial.delete()
        return Response({'detail': f'Testimonial id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'detail': f"Testimonial id - {pk} does't exists"}, status=status.HTTP_400_BAD_REQUEST)


