from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields.related import ManyToManyField

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import has_permissions

from site_settings.models import OurCompanyMessage
from site_settings.serializers import OurCompanyMessageSerializer, OurCompanyMessagetListSerializer

from commons.pagination import Pagination
from commons.enums import PermissionEnum
from rest_framework.permissions import AllowAny
import datetime

from django.http import JsonResponse


# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=OurCompanyMessagetListSerializer,
	responses=OurCompanyMessagetListSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_LIST.name])
def getAllOurCompanyMessage(request):
	company_messages = OurCompanyMessage.objects.all()
	total_elements = company_messages.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	company_messages = pagination.paginate_data(company_messages)

	serializer = OurCompanyMessagetListSerializer(company_messages, many=True)

	response = {
		'company_messages': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	return Response(response, status=status.HTTP_200_OK)







@extend_schema(request=OurCompanyMessageSerializer, responses=OurCompanyMessageSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_DETAILS.name])
def getAOurCompanyMessage(request, pk):
	try:
		company_message = OurCompanyMessage.objects.get(pk=pk)
		serializer = OurCompanyMessageSerializer(company_message)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"OurCompanyMessage id - {pk} does't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=OurCompanyMessageSerializer, responses=OurCompanyMessageSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_CREATE.name])
def createOurCompanyMessage(request):
	data = request.data
	print('data: ', data)
	print('content_type: ', request.content_type)

	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != '0':
			filtered_data[key] = value
	
	print('filtered_data: ', filtered_data)
	
	serializer = OurCompanyMessageSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data)
	else:
		return Response(serializer.errors)




@extend_schema(request=OurCompanyMessageSerializer, responses=OurCompanyMessageSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_UPDATE.name])
def updateOurCompanyMessage(request, pk):
	data = request.data
	filtered_data = {}

	try:
		company_message_obj = OurCompanyMessage.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return Response({'detail': f"OurCompanyMessage id - {pk} doesn't exists"})

	for key, value in data.items():
		if value != '' and value != '0':
			filtered_data[key] = value

	print('filtered_data: ', filtered_data)

	image = filtered_data.get('image', None)

	if image is not None and type(image) == str:
		popped_image = filtered_data.pop('image')
	
	serializer = OurCompanyMessageSerializer(company_message_obj, data=filtered_data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors)
	




@extend_schema(request=OurCompanyMessageSerializer, responses=OurCompanyMessageSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_DELETE.name])
def deleteOurCompanyMessage(request, pk):
	try:
		company_message = OurCompanyMessage.objects.get(pk=pk)
		company_message.delete()
		return Response({'detail': f'OurCompanyMessage id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"OurCompanyMessage id - {pk} does't exists"}, status=status.HTTP_400_BAD_REQUEST)


