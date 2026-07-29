from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from site_settings.models import SisterConcern, SisterConcernImage
from site_settings.serializers import SisterConcernSerializer, SisterConcernListSerializer
from commons.pagination import Pagination
from commons.enums import PermissionEnum
from authentication.decorators import has_permissions
from django.db.models import Q

from site_settings.utils import normalize_search_query


@extend_schema(
    parameters=[
        OpenApiParameter("page"),
        OpenApiParameter("size"),
    ],
    request=SisterConcernListSerializer,
    responses=SisterConcernListSerializer,
)
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_LIST.name])
def getAllSisterConcern(request):
    sister_concerns = SisterConcern.objects.all().order_by("-id")
    total_elements = sister_concerns.count()

    search_query = normalize_search_query(request.query_params.get('searchKey', ''))
    if search_query:
        sister_concerns = SisterConcern.objects.filter(
            Q(title__icontains=search_query)
        )
    else:
        total_elements = sister_concerns.count()
    page = request.query_params.get("page")
    size = request.query_params.get("size")

    # Pagination
    pagination = Pagination()
    pagination.page = page
    pagination.size = size
    sister_concerns = pagination.paginate_data(sister_concerns)

    serializer = SisterConcernSerializer(sister_concerns, many=True)

    response = {
        "sister_concerns": serializer.data,
        "page": pagination.page,
        "size": pagination.size,
        "total_pages": pagination.total_pages,
        "total_elements": total_elements,
    }

    return Response(response, status=status.HTTP_200_OK)


@extend_schema(request=SisterConcernSerializer, responses=SisterConcernSerializer)
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_DETAILS.name])
def getASisterConcern(request, pk):
    try:
        sister_concern = SisterConcern.objects.get(pk=pk)
        serializer = SisterConcernListSerializer(sister_concern)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response(
            {"detail": f"SisterConcern id - {pk} doesn't exist"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@extend_schema(request=SisterConcernSerializer, responses=SisterConcernSerializer)
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_CREATE.name])
def createSisterConcern(request):
    data = request.data.copy()
    print("data: ", data)
    print("content_type: ", request.content_type)

    filtered_data = {}
    filtered_data["images"] = []

    for key, value in data.items():
        if value != '' and value != 0 and value != '0' and value != 'undefined':
            filtered_data[key] = value
        if key.startswith('images'):
            filtered_data.pop(key)
            filtered_data["images"].append(value)
    print("filtered_data", filtered_data)

    serializer = SisterConcernSerializer(data=filtered_data)
    if serializer.is_valid():
        sister_concern = serializer.save(created_by=request.user)
        return Response(
            SisterConcernSerializer(sister_concern).data,
            status=status.HTTP_201_CREATED,
        )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(request=SisterConcernSerializer, responses=SisterConcernSerializer)
@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def updateSisterConcern(request, pk):
    try:
        sister_concern_obj = SisterConcern.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response(
            {"detail": f"SisterConcern id - {pk} doesn't exist"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    data = request.data.copy()

    # Keep all fields except empty strings/0/undefined
    filtered_data = {}
    for key, value in data.items():
        if value not in ['', 0, '0', 'undefined']:
            filtered_data[key] = value

    # Handle image separately
    if 'image' in request.FILES:
        filtered_data['image'] = request.FILES['image']
    else:
        # If no new image uploaded, keep the old one
        filtered_data['image'] = sister_concern_obj.image

    serializer = SisterConcernSerializer(
        sister_concern_obj, data=filtered_data, partial=True
    )

    if serializer.is_valid():
        sister_concern = serializer.save(updated_by=request.user)
        return Response(SisterConcernSerializer(sister_concern).data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@extend_schema(request=None, responses=None)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.ATTRIBUTE_DELETE.name])
def deleteSisterConcern(request, pk):
    try:
        sister_concern = SisterConcern.objects.get(pk=pk)
        SisterConcernImage.objects.filter(sister_concern=sister_concern).delete()
        sister_concern.delete()
        return Response(
            {"detail": f"SisterConcern id - {pk} deleted successfully"},
            status=status.HTTP_200_OK,
        )
    except ObjectDoesNotExist:
        return Response(
            {"detail": f"SisterConcern id - {pk} doesn't exist"},
            status=status.HTTP_400_BAD_REQUEST,
        )
