from datetime import datetime

import os
import random
import string
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from authentication.models import  Notice, Permission



from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter

from authentication.decorators import has_permissions


from authentication.serializers import NoticeListSerializer, NoticeSerializer
from commons.pagination import Pagination



# Create your views here.


@extend_schema(
    parameters=[
        OpenApiParameter("page"),
        OpenApiParameter("size"),
    ],
    request=NoticeListSerializer,
    responses=NoticeListSerializer,
)
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
# @has_permissions([AuthPermEnum.DESIGNATION_LIST.name])
def getAllNotice(request):
    notice = Notice.objects.all()
    total_elements = notice.count()

    page = request.query_params.get("page")
    size = request.query_params.get("size")

    # Pagination
    pagination = Pagination()
    pagination.page = page
    pagination.size = size
    notice = pagination.paginate_data(notice)

    serializer = NoticeListSerializer(notice, many=True)

    response = {
        "notices": serializer.data,
        "page": pagination.page,
        "size": pagination.size,
        "total_pages": pagination.total_pages,
        "total_elements": total_elements,
    }

    return Response(response, status=status.HTTP_200_OK)


@extend_schema(request=NoticeListSerializer, responses=NoticeListSerializer)
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
# @has_permissions([AuthPermEnum.DESIGNATION_LIST.name])
def getAllNoticeWithoutPagination(request):
    notice = Notice.objects.all()
    serializer = NoticeListSerializer(notice, many=True)

    response = {
        "notices": serializer.data,
    }

    return Response(response, status=status.HTTP_200_OK)


@extend_schema(request=NoticeListSerializer, responses=NoticeListSerializer)
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
# @has_permissions([SiteSettingPermEnum.GENERAL_SETTING_UPDATE.name])
def getANotice(request, pk):
    try:
        notice = Notice.objects.get(pk=pk)
        serializer = NoticeListSerializer(notice)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response(
            {"detail": f"notice id - {pk} doesn't exists"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@extend_schema(request=NoticeListSerializer, responses=NoticeListSerializer)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
# @has_permissions([SiteSettingPermEnum.GENERAL_SETTING_UPDATE.name])
def createNotice(request):
    data = request.data
    filtered_data = {}

    for key, value in data.items():
        if value != "" and value != "0":
            filtered_data[key] = value
    file = data.get("file", None)
    title = filtered_data.get("title")
    if not type(file) is str:
        current_date = datetime.now().strftime("%Y%m%d")
        file_extension = os.path.splitext(file.name)[1]  # Get the file extension
        new_filename = f"{title}__{current_date}{file_extension}"
        filtered_data["file"] = file
        filtered_data["file"].name = new_filename
  
    user = request.user
#     permission_obj, created = Permission.objects.get_or_create(
#         name=SiteSettingPermEnum.GENERAL_SETTING_CREATE.name
#     )
    serializer = NoticeSerializer(data=filtered_data)

    if serializer.is_valid():
        serializer.save()
        s_data = serializer.data
        comment = f"id={s_data.get('id')}, user={str(user)} name={title}"
     #    ActivityLog.objects.create(
     #        activity_type=permission_obj, activity_by=user, comment=comment
     #    )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@extend_schema(request=NoticeSerializer, responses=NoticeSerializer)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
# @has_permissions([SiteSettingPermEnum.GENERAL_SETTING_UPDATE.name])
def updateNotice(request, pk):
    try:
        notice = Notice.objects.get(pk=pk)
        data = request.data
        filtered_data = {}
        restricted_values = ("", 0, " ", "undefined", "0")

        for key, value in data.items():
            if key == "file" and type(value) == str:
                continue  # Skip the file field

            if value not in restricted_values:
                filtered_data[key] = value
        title = filtered_data.get("title")
        file = filtered_data.get("file", None)
        if file is not None and not isinstance(file, str):
            # Generate a new filename using the date field and title field
            current_date = datetime.now().strftime("%Y%m%d")
            file_extension = os.path.splitext(file.name)[1]  # Get the file extension
            new_filename = f"{title}__{current_date}{file_extension}"

            filtered_data["file"] = file
            filtered_data["file"].name = new_filename

        user = request.user
     #    permission_obj, created = Permission.objects.get_or_create(
     #        name=SiteSettingPermEnum.GENERAL_SETTING_CREATE.name
     #    )
        serializer = NoticeSerializer(
            notice, data=filtered_data, partial=True
        )  # Use partial=True to allow partial updates
        if serializer.is_valid():
            serializer.save()
            s_data = serializer.data
            comment = f"id={s_data.get('id')}, user={str(user)} "
          #   ActivityLog.objects.create(
          #       activity_type=permission_obj, activity_by=user, comment=comment
          #   )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response(
            {"detail": f"Notice with id - {pk} doesn't exist"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@extend_schema(request=NoticeSerializer, responses=NoticeSerializer)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
# @has_permissions([SiteSettingPermEnum.GENERAL_SETTING_UPDATE.name])
def deleteNotice(request, pk):
    try:
        user = request.user
     #    permission_obj, created = Permission.objects.get_or_create(
     #        name=SiteSettingPermEnum.GENERAL_SETTING_CREATE.name
     #    )
        notice = Notice.objects.get(pk=pk)
        notice.delete()
        serializer = NoticeSerializer(notice)
        s_data = serializer.data
        comment = f"id={s_data.get('id')}, user={str(user)}"
     #    ActivityLog.objects.create(
     #        activity_type=permission_obj, activity_by=user, comment=comment
     #    )
        return Response(
            {"detail": f"notice id - {pk} is deleted successfully"},
            status=status.HTTP_200_OK,
        )
    except ObjectDoesNotExist:
        return Response(
            {"detail": f"notice id - {pk} doesn't exists"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@extend_schema(request=NoticeSerializer, responses=NoticeSerializer)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
# @has_permissions([SiteSettingPermEnum.GENERAL_SETTING_DETAILS.name])
def searchNotice(request):
    keyword = request.query_params.get("key", None)

    print("keyword: ", keyword)

    if keyword:
        notice = Notice.objects.filter(Q(title__icontains=keyword))
    else:
        return Response({"detail": f"Please enter title to search."})

    serializer = NoticeListSerializer(notice, many=True)

    response = {
        "notices": serializer.data,
    }

    if len(notice) > 0:
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(
            {"detail": f"There are no agency matching your search"},
            status=status.HTTP_400_BAD_REQUEST,
        )
