from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields.related import ManyToManyField

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import has_permissions

from site_settings.models import ServiceSlider
from site_settings.serializers import ServiceSliderSerializer, ServiceSliderListSerializer

from commons.pagination import Pagination
from commons.enums import PermissionEnum
from rest_framework.permissions import AllowAny
import datetime

from django.http import JsonResponse

from site_settings.utils import normalize_search_query
from django.db.models import Q


# Create your views here.

@extend_schema(
    parameters=[
        OpenApiParameter("page"),
        OpenApiParameter("size"),
  ],
    request=ServiceSliderListSerializer,
    responses=ServiceSliderListSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_LIST.name])
def getAllServiceSlider(request):
    service_sliders = ServiceSlider.objects.all()
    total_elements = service_sliders.count()


    search_query = normalize_search_query(request.query_params.get('searchKey', ''))
    if search_query:
        service_sliders = ServiceSlider.objects.filter(
            Q(title__icontains=search_query)
        )
    else:
        total_elements = service_sliders.count()

    page = request.query_params.get('page')
    size = request.query_params.get('size')

    # Pagination
    pagination = Pagination()
    pagination.page = page
    pagination.size = size
    service_sliders = pagination.paginate_data(service_sliders)

    serializer = ServiceSliderListSerializer(service_sliders, many=True)

    response = {
        'service_sliders': serializer.data,
        'page': pagination.page,
        'size': pagination.size,
        'total_pages': pagination.total_pages,
        'total_elements': total_elements,
    }

    return Response(response, status=status.HTTP_200_OK)







@extend_schema(request=ServiceSliderSerializer, responses=ServiceSliderSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_DETAILS.name])
def getAServiceSlider(request, pk):
    try:
        service_slider = ServiceSlider.objects.get(pk=pk)
        serializer = ServiceSliderSerializer(service_slider)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'detail': f"ServiceSlider id - {pk} does't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ServiceSliderSerializer, responses=ServiceSliderSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_CREATE.name])
def createServiceSlider(request):
    data = request.data
    print('data: ', data)
    print('content_type: ', request.content_type)

    filtered_data = {}

    for key, value in data.items():
        if value != '' and value != '0':
            filtered_data[key] = value
    
    print('filtered_data: ', filtered_data)
    
    serializer = ServiceSliderSerializer(data=filtered_data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)




@extend_schema(request=ServiceSliderSerializer, responses=ServiceSliderSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_UPDATE.name])
def updateServiceSlider(request, pk):
    data = request.data
    filtered_data = {}

    try:
        service_slider_obj = ServiceSlider.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response({'detail': f"ServiceSlider id - {pk} doesn't exists"})

    for key, value in data.items():
        if value != '' and value != '0':
            filtered_data[key] = value

    print('filtered_data: ', filtered_data)

    image = filtered_data.get('image', None)

    if image is not None and type(image) == str:
        popped_image = filtered_data.pop('image')
    
    serializer = ServiceSliderSerializer(service_slider_obj, data=filtered_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors)
    




@extend_schema(request=ServiceSliderSerializer, responses=ServiceSliderSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_DELETE.name])
def deleteServiceSlider(request, pk):
    try:
        service_slider = ServiceSlider.objects.get(pk=pk)
        service_slider.delete()
        return Response({'detail': f'ServiceSlider id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'detail': f"ServiceSlider id - {pk} does't exists"}, status=status.HTTP_400_BAD_REQUEST)


