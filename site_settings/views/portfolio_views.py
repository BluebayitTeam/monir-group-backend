from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields.related import ManyToManyField

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import has_permissions

from site_settings.models import Portfolio
from site_settings.serializers import PortfolioSerializer, PortfolioListSerializer

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
    request=PortfolioListSerializer,
    responses=PortfolioListSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_LIST.name])
def getAllPortfolioForPortfolio(request):

    portfolios = Portfolio.objects.filter(is_portfolio=True).order_by("serial_number")

    total_elements = portfolios.count()

    page = request.query_params.get('page')
    size = request.query_params.get('size')

    # Pagination
    pagination = Pagination()
    pagination.page = page
    pagination.size = size
    portfolios = pagination.paginate_data(portfolios)

    serializer = PortfolioListSerializer(portfolios, many=True)

    response = {
        'portfolios': serializer.data,
        'page': pagination.page,
        'size': pagination.size,
        'total_pages': pagination.total_pages,
        'total_elements': total_elements,
    }

    return Response(response, status=status.HTTP_200_OK)


@extend_schema(
    parameters=[
        OpenApiParameter("page"),
        OpenApiParameter("size"),
  ],
    request=PortfolioListSerializer,
    responses=PortfolioListSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_LIST.name])
def getAllPortfolio(request):
    category_id = request.query_params.get('category')
    portfolios = Portfolio.objects.all().order_by("serial_number")
    
    if category_id:
        portfolios = portfolios.filter(category_id=category_id)
    total_elements = portfolios.count()

    search_query = normalize_search_query(request.query_params.get('searchKey', ''))
    if search_query:
        portfolios = Portfolio.objects.filter(
            Q(title__icontains=search_query)
        )
    else:
        total_elements = portfolios.count()

    page = request.query_params.get('page')
    size = request.query_params.get('size')

    # Pagination
    pagination = Pagination()
    pagination.page = page
    pagination.size = size
    portfolios = pagination.paginate_data(portfolios)

    serializer = PortfolioListSerializer(portfolios, many=True)

    response = {
        'portfolios': serializer.data,
        'page': pagination.page,
        'size': pagination.size,
        'total_pages': pagination.total_pages,
        'total_elements': total_elements,
    }

    return Response(response, status=status.HTTP_200_OK)



@extend_schema(
    parameters=[
        OpenApiParameter("page"),
        OpenApiParameter("size"),
  ],
    request=PortfolioListSerializer,
    responses=PortfolioListSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_LIST.name])
def getAllPortfolioWP(request):

    portfolios = Portfolio.objects.all().order_by("serial_number")
    



    serializer = PortfolioListSerializer(portfolios, many=True)

    response = {
        'portfolios': serializer.data,

    }

    return Response(response, status=status.HTTP_200_OK)





@extend_schema(request=PortfolioSerializer, responses=PortfolioSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_DETAILS.name])
def getAPortfolio(request, pk):
    try:
        portfolio = Portfolio.objects.get(pk=pk)
        serializer = PortfolioSerializer(portfolio)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'detail': f"Portfolio id - {pk} does't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=PortfolioSerializer, responses=PortfolioSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_CREATE.name])
def createPortfolio(request):
    data = request.data
    print('data: ', data)
    print('content_type: ', request.content_type)

    filtered_data = {}

    for key, value in data.items():
        if value != '' and value != '0':
            filtered_data[key] = value
    
    print('filtered_data: ', filtered_data)
    
    serializer = PortfolioSerializer(data=filtered_data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)




@extend_schema(request=PortfolioSerializer, responses=PortfolioSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_UPDATE.name])
def updatePortfolio(request, pk):
    data = request.data
    filtered_data = {}

    try:
        portfolio_obj = Portfolio.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response({'detail': f"Portfolio id - {pk} doesn't exists"})

    for key, value in data.items():
        if value != '' and value != '0':
            filtered_data[key] = value

    print('filtered_data: ', filtered_data)

    image = filtered_data.get('image', None)

    if image is not None and type(image) == str:
        popped_image = filtered_data.pop('image')
    
    serializer = PortfolioSerializer(portfolio_obj, data=filtered_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors)
    




@extend_schema(request=PortfolioSerializer, responses=PortfolioSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_DELETE.name])
def deletePortfolio(request, pk):
    try:
        portfolio = Portfolio.objects.get(pk=pk)
        portfolio.delete()
        return Response({'detail': f'Portfolio id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'detail': f"Portfolio id - {pk} does't exists"}, status=status.HTTP_400_BAD_REQUEST)


