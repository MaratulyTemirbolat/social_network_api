from typing import (
    Optional,
    Tuple,
    Any,
    Dict,
    List,
)

from django.db.models import (
    QuerySet,
    Prefetch,
)
from django.http.request import QueryDict
from django.utils.text import slugify

from rest_framework.viewsets import ViewSet
from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.decorators import action

from abstracts.handlers import (
    NoneDataHandler,
    DRFResponseHandler,
)
from abstracts.paginators import AbstractPageNumberPaginator
from locations.models import (
    Country,
    City,
)
from locations.serializers import (
    CountryBaseModelSerializer,
    CountryDetailModelSerializer,
    CityBaseModelSerializer,
    CityDetailedSerializer,
)


class CountryViewSet(NoneDataHandler, DRFResponseHandler, ViewSet):
    """CountryViewSet."""

    queryset: QuerySet[Country] = \
        Country.objects.all()
    serializer_class: CountryBaseModelSerializer = CountryBaseModelSerializer
    permission_classes: Tuple[Any] = (
        AllowAny,
    )
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator

    def get_instance(
        self,
        pk: int = 0,
        is_deleted: bool = False
    ) -> Optional[Country]:
        """Obtain the class instance by primary key."""
        country: Optional[Country] = None
        try:
            country = self.get_queryset().prefetch_related(
                Prefetch(
                    lookup="attached_cities",
                    queryset=City.objects.get_not_deleted()
                )
            ).get(id=pk)
            return country
        except Country.DoesNotExist:
            return None

    def get_queryset(self) -> QuerySet:
        """Queryset method for ORM requests."""
        return self.queryset.get_not_deleted()

    def list(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request for all."""
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
        """Handle GET-request with specified PK."""
        country: Optional[Country] = self.get_instance(pk=pk)

        response: DRF_Response = self.get_none_response(
            object=country,
            message=f"Не нашел Страну с ID: {pk}",
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        response = self.get_drf_response(
            request=request,
            data=country,
            serializer_class=CountryDetailModelSerializer,
            many=False
        )

        return response

    def create(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request for country."""
        data_copy: QueryDict = request.data.copy()
        if data_copy.get("name", None):
            data_copy.setdefault(
                "slug",
                slugify(data_copy["name"])
            )
        serializer: CountryBaseModelSerializer = self.serializer_class(
            data=data_copy
        )
        valid: bool = serializer.is_valid()
        if valid:
            new_country: Country = serializer.save()
            message: str = "Новая страна успешно создана"
            cities: Optional[List[dict[str, Any]]] = data_copy.get(
                "cities",
                None
            )
            response: DRF_Response = self.get_drf_response(
                request=request,
                data=new_country,
                serializer_class=CountryDetailModelSerializer,
                many=False
            )

            if cities:
                response = self.create_cities(
                    request=request,
                    country=new_country,
                    cities=cities,
                    *args,
                    *kwargs
                )

            return response
        return DRF_Response(
            {'response': 'Объект не создан'}
        )

    def create_cities(
        self,
        request: DRF_Request,
        country: Country,
        cities: List[dict[str, Any]],
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Create cities with provided names."""
        city: dict[str, Any]
        for city in cities:
            name: Optional[str] = city.get("name", None)
            is_capital: bool = city.get("is_capital", False)
            if name:
                City.objects.create(
                    name=name,
                    country=country,
                    is_capital=is_capital
                )
        return self.retrieve(
            request=request,
            pk=country.id,
            args=args,
            kwargs=kwargs
        )

    @action(
        methods=["post"],
        detail=True,
        url_path="create_cities",
        permission_classes=(
            AllowAny,
        )
    )
    def create_country_cities(
        self,
        request: DRF_Request,
        pk: Optional[int] = None,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request for city creation."""
        country: Optional[Country] = self.get_instance(
            pk=pk
        )

        response: DRF_Response = self.get_none_response(
            object=country,
            message=f"Не нашел Страну с ID: {pk}",
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        cities: Optional[List[dict[str, Any]]] = request.data.get(
            "cities",
            None
        )
        if not cities or not isinstance(cities, list):
            return DRF_Response(
                data="Необходимо предоставить города в правильном формате",
                status=status.HTTP_400_BAD_REQUEST
            )

        return self.create_cities(
            request=request,
            country=country,
            cities=cities,
            args=args,
            kwargs=kwargs
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

        instance: Optional[Country] = self.get_instance(pk=pk)
        response: Optional[DRF_Response] = self.get_none_response(
            object=instance,
            message=f'Не нашел такую страну с ID: {pk}',
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        serializer: CountryBaseModelSerializer = CountryBaseModelSerializer(
            instance=instance,
            data=request.data,
            partial=is_partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return DRF_Response(
            data=serializer.data,
            status=status.HTTP_202_ACCEPTED
        )

    def partial_update(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle PATCH method with provided id."""
        kwargs['is_partial'] = True
        return self.update(request, *args, **kwargs)


class CityViewSet(NoneDataHandler, DRFResponseHandler, ViewSet):
    """CityViewSet."""

    queryset: QuerySet[City] = \
        City.objects.all()
    serializer_class: CityBaseModelSerializer = CityBaseModelSerializer
    permission_classes: Tuple[Any] = (
        AllowAny,
    )
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator

    def get_instance(
        self,
        pk: int = 0,
        is_deleted: bool = False
    ) -> Optional[City]:
        """Obtain the class instance by primary key."""
        city: Optional[City] = None
        try:
            city = self.get_queryset().get(pk=pk)
            return city
        except City.DoesNotExist:
            return None

    def get_queryset(self) -> QuerySet:
        """Queryset method for ORM requests."""
        return self.queryset.get_not_deleted().select_related(
            "country"
        )

    def list(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request to provide all cities."""
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.get_queryset(),
            serializer_class=CityDetailedSerializer,
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
        """Handle GET-request with specified PK."""
        city: Optional[City] = self.get_instance(pk=pk)

        response: Optional[DRF_Response] = self.get_none_response(
            object=city,
            message=f"Не нашел Город с ID: {pk}",
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        response = self.get_drf_response(
            request=request,
            data=city,
            serializer_class=CityDetailedSerializer,
            many=False
        )

        return response

    def create(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request for city."""
        data_copy: QueryDict = request.data.copy()

        serializer: CityBaseModelSerializer = self.serializer_class(
            data=data_copy
        )
        valid: bool = serializer.is_valid()
        if valid:
            new_city: City = serializer.save()

            response: DRF_Response = self.get_drf_response(
                request=request,
                data=new_city,
                serializer_class=CityDetailedSerializer,
                many=False
            )
            return response

        return DRF_Response(
            {'response': 'Объект не создан'}
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

        instance: Optional[City] = self.get_instance(pk=pk)
        response: Optional[DRF_Response] = self.get_none_response(
            object=instance,
            message=f'Не нашел такой город с ID: {pk}',
            status=status.HTTP_400_BAD_REQUEST
        )
        if response:
            return response

        serializer: CityBaseModelSerializer = self.serializer_class(
            instance=instance,
            data=request.data,
            partial=is_partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return DRF_Response(
            data=serializer.data,
            status=status.HTTP_202_ACCEPTED
        )

    def partial_update(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle PATCH method with provided id."""
        kwargs['is_partial'] = True
        return self.update(request, *args, **kwargs)
