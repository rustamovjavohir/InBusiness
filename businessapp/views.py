from django.db import transaction
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Projects
from .serializers import ProjectsSerializers
from .utils import ProjectPagination


class ProjectListView(ListAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializers
    filter_backends = (filters.SearchFilter,)
    pagination_class = ProjectPagination
    parser_classes = [JSONParser, ]

    @swagger_auto_schema(operation_summary="Loyihalar ro'yhatini ko'rish",)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProjectUpdateDeleteView(GenericAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializers
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]
    parser_classes = [JSONParser, ]

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.created_by == request.user or request.user.is_superuser:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        return Response(data={"This is not your project"}, status=status.HTTP_403_FORBIDDEN)

    @swagger_auto_schema(operation_summary="Loyiha ma'lumotlarini yangilash",)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Loyiha ma'lumotlarini qisman yangilash",)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.created_by == request.user or request.user.is_superuser:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data={"This is not your project"}, status=status.HTTP_403_FORBIDDEN)

    @swagger_auto_schema(operation_summary="Loyihani o'chirish",)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProjectRetrieveView(RetrieveAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializers
    parser_classes = [JSONParser, ]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(operation_summary="Loyiha haqidagi to'liq ma'lumotni ko'rish", )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ProjectCreateView(CreateAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializers
    pagination_class = ProjectPagination
    parser_classes = [MultiPartParser, ]
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        # kwargs.update({"created_by": request.user.id})
        return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data
        data["created_by"] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(operation_summary="Yangi loyiha kiritish",)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

