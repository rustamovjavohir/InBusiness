from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, filters
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, GenericAPIView, get_object_or_404, \
    RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Skills, Specialization
from .serializers import UserSerializers, SkillsSerializers, SpecializationSerializers
from .utils import UserPagination


def get_tokens_tor_users(user):
    refresh = RefreshToken.for_user(user=user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


class BlacklistRefreshView(APIView):
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Success", status=status.HTTP_200_OK)


class SingUpView(CreateAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(operation_summary="Ro'yhatdan o'tish",)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    filter_backends = (filters.SearchFilter,)
    # permission_classes = [AllowAny, ]
    permission_classes = [IsAdminUser, ]
    authentication_classes = [JWTAuthentication, ]
    pagination_class = UserPagination
    parser_classes = [JSONParser, ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Barcha foydalanuvchilar ro'yhatini ko'rish")
    def get(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    filter_backends = (filters.SearchFilter,)
    # permission_classes = [AllowAny, ]
    permission_classes = [IsAdminUser, ]
    authentication_classes = [JWTAuthentication, ]
    pagination_class = UserPagination
    parser_classes = [JSONParser, ]

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(operation_summary="Foydalanuvchini ro'yhatdan ochirish")
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserBlockView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    filter_backends = (filters.SearchFilter,)
    permission_classes = [IsAdminUser, ]
    authentication_classes = [JWTAuthentication, ]
    pagination_class = UserPagination
    parser_classes = [JSONParser, ]

    @transaction.atomic
    @swagger_auto_schema(operation_summary="Foydalanuvchini qora ro'yhatga qo'shish")
    def post(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=request.data.get('user_id'))
        obj.is_active = False
        obj.save()
        return Response(data={"message": f"{obj.username} is blocked"}, status=status.HTTP_200_OK)


class UserRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    filter_backends = (filters.SearchFilter,)
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]
    pagination_class = UserPagination
    parser_classes = [JSONParser, ]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.id == request.user.id or request.user.is_superuser:
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data={"This is not your account"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Foydalanuvchi ma'lumotlarini ko'rish")
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Foydalanuvchi ma'lumotlarini qisman yangilash")
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.id == request.user.id or request.user.is_superuser:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data={"This is not your account"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Foydalanuvchi ma'lumotlarini yangilash")
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class SkillsViewSet(ModelViewSet):
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializers
    filter_backends = (filters.SearchFilter,)
    permission_classes = [IsAdminUser, ]
    authentication_classes = [JWTAuthentication, ]
    pagination_class = UserPagination
    parser_classes = [MultiPartParser, ]

    @swagger_auto_schema(operation_summary="Mutaxasislar royhatini ko'rish")
    def list(self, request, *args, **kwargs):
        return super(SkillsViewSet, self).list(self, request, *args, **kwargs)

    @transaction.atomic
    @swagger_auto_schema(operation_summary="Yangi Mutaxasis kiritish")
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @transaction.atomic
    @swagger_auto_schema(operation_summary="Mutaxasislar malumotlarini yangilash")
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @transaction.atomic
    @swagger_auto_schema(operation_summary="Mutaxasislar malumotlarini qisman yangilash")
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Mutaxasislar malumotlarini o'chirish")
    def destroy(self, request, *args, **kwargs):
        return super(SkillsViewSet, self).destroy(self, request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Mutaxasislik haqidagi malumotlarini chop etish (retrieve)")
    def retrieve(self, request, *args, **kwargs):
        return super(SkillsViewSet, self).retrieve(self, request, *args, **kwargs)


class SpecializationListCreateView(ListCreateAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializers
    filter_backends = (filters.SearchFilter,)
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]
    pagination_class = UserPagination
    parser_classes = [JSONParser, ]

    # def list(self, request, *args, **kwargs):
    #     return super(SpecializationListCreateView, self).list(self, request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Mutaxasislik royhatini ko'rish")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @transaction.atomic
    @swagger_auto_schema(operation_summary="Yangi Mutaxasislik kirish")
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SpecializationDeleteView(DestroyAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializers
    permission_classes = [IsAdminUser, ]
    authentication_classes = [JWTAuthentication, ]
    pagination_class = UserPagination
    parser_classes = [JSONParser, ]

    @transaction.atomic
    @swagger_auto_schema(operation_summary="Mutaxasislikni o'chirish")
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
