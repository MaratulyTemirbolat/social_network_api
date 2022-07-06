from typing import (
    Optional,
    Tuple,
    Any,
    Dict,
    List,
    Set,
)

from django.db.models import QuerySet

from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework import status
from rest_framework.decorators import action

from groups.serializers import (
    GroupBaseSerializer,
    GroupDetailSerializer,
)
from groups.models import (
    Group,
)
from abstracts.handlers import (
    DRFResponseHandler,
    NoneDataHandler,
)
from abstracts.paginators import AbstractPageNumberPaginator
from auths.models import CustomUser


class GroupViewSet(NoneDataHandler, DRFResponseHandler, ViewSet):
    """GroupViewSet."""

    queryset: QuerySet[Group] = \
        Group.objects.all()
    serializer_class: GroupBaseSerializer = GroupBaseSerializer
    permission_classes: Tuple[Any] = (
        AllowAny,
    )
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator

    def get_queryset(self) -> QuerySet:
        """Queryset method for ORM requests."""
        return self.queryset.get_not_deleted()

    def get_instance(
        self,
        pk: int = 0,
        is_deleted: bool = False
    ) -> Optional[Group]:
        """Obtain the class instance by primary key."""
        compl_reason: Optional[Group] = None
        try:
            compl_reason = self.get_queryset().\
                prefetch_related(
                    "followers"
                ).prefetch_related(
                    "members_rights"
                ).get(id=pk)
            return compl_reason
        except Group.DoesNotExist:
            return None

    def list(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """List method for non-deleted reasons (GET-request)."""
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.get_queryset(),
            serializer_class=self.serializer_class,
            many=True,
            paginator=self.pagination_class()
        )
        return response

    def retrieve(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request with ID to complain reason."""
        group: Optional[Group] = self.get_instance(pk=pk)
        if not group:
            return DRF_Response(
                {'response': 'Не нашел такой чат'},
                status=status.HTTP_400_BAD_REQUEST
            )

        response: DRF_Response = self.get_drf_response(
            request=request,
            data=group,
            serializer_class=GroupDetailSerializer,
            many=False
        )

        return response

    def create(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request."""
        serializer: GroupDetailSerializer = self.serializer_class(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return DRF_Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def update(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle PUT method with provided id."""
        is_partial: bool = kwargs.pop('is_partial', False)

        pk: Optional[str] = kwargs.get('pk', None)
        response: Optional[DRF_Response] = self.get_none_response(
            object=pk,
            message="Первичный ключ должен быть предоставлен",
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        instance: Optional[Group] = self.get_instance(pk=pk)
        response: Optional[DRF_Response] = self.get_none_response(
            object=instance,
            message=f'Не нашел такую группу с ID: {pk}',
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        serializer: GroupDetailSerializer = GroupDetailSerializer(
            instance=instance,
            data=request.data,
            partial=is_partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return DRF_Response(data=serializer.data)

    def partial_update(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle PATCH method with provided id."""
        kwargs['is_partial'] = True
        return self.update(request, *args, **kwargs)

    @action(
        methods=["post"],
        detail=True,
        url_path="add_followers"
    )
    def add_followers(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Any,
        **kwargs: Any
    ) -> DRF_Response:
        """POST-request for friends adding to the chat."""
        group: Optional[Group] = self.get_instance(pk=pk)
        response: Optional[DRF_Response] = self.get_none_response(
            object=group,
            message=f"Группа с ID {pk} не найдена, либо она удалена",
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        group_followers_id: QuerySet = group.followers.values_list(
            "id",
            flat=True
        )
        required_followers: Optional[List[int]] = request.data.get(
            "members", None
        )
        response = self.get_none_response(
            object=required_followers,
            message="Необходимо предоставить пользователей",
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        member_difference: Set[int] = (
            set(required_followers) - set(group_followers_id)
        )
        resulted_members: QuerySet = CustomUser.objects.get_not_deleted().\
            filter(id__in=member_difference)

        i: int
        for i in range(resulted_members.count()):
            group.followers.add(resulted_members[i])

        response = self.get_drf_response(
            request=request,
            data=group,
            serializer_class=GroupDetailSerializer,
            many=False
        )
        return response

    @action(
        methods=["post"],
        detail=True,
        url_path="remove_members"
    )
    def remove_followers(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Any,
        **kwargs: Any
    ) -> DRF_Response:
        """POST-request to remove friends from chat by id."""
        group: Optional[Group] = self.get_instance(pk=pk)
        response: Optional[DRF_Response] = self.get_none_response(
            object=group,
            message=f"Группа с ID {pk} не найдена, либо она удален",
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        required_followers: Optional[List[int]] = request.data.get(
            "members", None
        )
        response = self.get_none_response(
            object=required_followers,
            message="Необходимо предоставить пользователей",
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        found_people: QuerySet[CustomUser] = group.followers.filter(
            id__in=required_followers
        )

        i: int
        for i in range(found_people.count()):
            group.followers.remove(found_people[i])

        response = self.get_drf_response(
            request=request,
            data=group,
            serializer_class=GroupDetailSerializer,
            many=False
        )

        return response
