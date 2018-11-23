from main import models
from main import serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from main.constants import CLIENT, MASTER, PARTNER, USER_TYPES

class IsBasePartner(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'partner' and request.user.partner == view.get_object()

class IsBaseClient(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'client' and request.user.client == view.get_object()

class IsClient(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'client'


class ClientList(generics.ListAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
    # permission_classes = (IsAdminUser, )


            
        
class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
    # permission_classes = (IsAdminUser, IsBaseClient)

    def destroy(self, request, *args, **kwargs):
        request.user.is_active = False
        request.user.save()
        return super().destroy(request, *args, **kwargs)

    

class PartnerList(generics.ListAPIView):
    queryset = models.Partner.objects.all()
    serializer_class = serializers.PartnerSerializer
    # permission_classes = (IsAdminUser, )
        
class PartnerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Partner.objects.all()
    serializer_class = serializers.PartnerSerializer
    # permission_classes = (IsBasePartner, )

    def destroy(self, request, *args, **kwargs):
        request.user.is_active = False
        request.user.save()
        return super().destroy(request, *args, **kwargs)


class SalonList(generics.ListCreateAPIView):
    queryset = models.Salon.objects.all()
    serializer_class = serializers.SalonSerializer
    # permission_classes = (IsBasePartner|IsClient)
    def get_queryset(self):
        queryset = models.Salon.objects.all()
        if 'partner_id' in self.kwargs:
            partner_id = int(self.kwargs['partner_id'])
            partner = models.Partner.objects.get(pk=partner_id)
            queryset = partner.salons.all()
        
        return queryset


    def perform_create(self, serializer):
        serializer.save(partner=self.request.user.partner)

class SalonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Salon.objects.all()
    serializer_class = serializers.SalonSerializer


class ServiceList(generics.ListCreateAPIView):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer
    lookup_field = 'salon_id'


    def list(self, request, *args, **kwargs):
        salon = models.Salon.objects.get(pk=self.kwargs[self.lookup_field])
        queryset = salon.salon_services.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        salon = models.Salon.objects.get(pk=self.kwargs[self.lookup_field])
        name = request.data.get('name')
        service = models.Service(salon=salon, name=name)
        if service:
            service.save()
            data = {
                'salon': serializers.SalonSerializer(salon)
            }
            serializer = serializers.ServiceSerializer(service)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({'error': 'Invalid data' }, status=status.HTTP_400_BAD_REQUEST)



class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer




class MasterList(generics.ListCreateAPIView):
    queryset = models.Master.objects.all()
    serializer_class = serializers.MasterSerializer
    lookup_field = 'salon_id'

    def list(self, request, *args, **kwargs):
        salon = models.Salon.objects.get(pk=self.kwargs[self.lookup_field])
        queryset = salon.masters.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        request.user.is_active = False
        request.user.save()
        return super().destroy(request, *args, **kwargs)

class MasterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Master.objects.all()
    serializer_class = serializers.MasterSerializer


class MasterServiceList(generics.ListCreateAPIView):
    queryset = models.MasterService.objects.all()
    serializer_class = serializers.MasterServiceSerializer
    lookup_field = 'salon_id'
 
    def post(self, request, *args, **kwargs):
        master_id = int(request.data.pop('master_id'))
        service_id = int(request.data.pop('service_id'))
        price = int(request.data.pop('price'))
        name = request.data.pop('name')
        master = models.Master.objects.get(pk=master_id)
        service = models.Service.objects.get(pk=service_id)
        salon = models.Salon.objects.get(pk=self.kwargs[self.lookup_field])
        master_service = models.MasterService(price=price, master=master, service=service, salon=salon, name=name)
        if master_service:
            master_service.save()
            serializer = serializers.MasterServiceSerializer(master_service)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({'error': 'Invalid data' }, status=status.HTTP_400_BAD_REQUEST)
        

class MasterServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.MasterService.objects.all()
    serializer_class = serializers.MasterServiceSerializer
    permission_classes = (IsAuthenticated, )

class CustomMasterServiceList(generics.ListAPIView):
    serializer_class = serializers.MasterServiceSerializer
    queryset = models.MasterService.objects.all()

    def get_queryset(self):
        if 'service_id' in self.kwargs:
            service_id = int(self.kwargs['service_id'])
            service = models.Service.objects.get(pk=service_id)
            master_services = models.MasterService.objects.filter(service=service)
            queryset = master_services
        elif 'master_id' in self.kwargs:
            master_id = int(self.kwargs['master_id'])
            master = models.Master.objects.get(pk=master_id)
            master_services = models.MasterService.objects.filter(master=master)
            queryset = master_services
        
        return queryset

class OrderCreate(generics.CreateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    
    def post(self, request, *args, **kwargs):
        master_service_id = int(request.data.pop('master_service_id'))
        master_service = models.MasterService.objects.get(pk=master_service_id)
        serializer = serializers.OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save(client=self.request.user.client, master_service=master_service, 
                                    partner=master_service.salon.partner,)
            order.save()
            order_ser = serializers.OrderSerializer(order)
            headers = self.get_success_headers(serializer.data)
            return Response(order_ser.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer


class OrderList(generics.ListAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        queryset = models.Order.objects.all()
        if 'master_id' in self.kwargs:
            master_id = int(self.kwargs['master_id'])
            master = models.Master.objects.get(pk=master_id)
            master_services = models.MasterService.objects.filter(master=master)
            orders =  models.Order.objects.none()
            for ms in master_services:
                orders = orders | ms.order_price.all()
            queryset = orders
        elif 'client_id' in self.kwargs:
            client_id = int(self.kwargs['client_id'])
            client = models.Client.objects.get(pk=client_id)
            orders = client.client_orders.all()
            queryset = orders
        elif 'partner_id' in self.kwargs:
            partner_id = int(self.kwargs['partner_id'])
            partner = models.Partner.objects.get(pk=partner_id)
            orders = partner.partner_orders.all()
            queryset = orders
        elif 'salon_id' in self.kwargs:
            salon_id = int(self.kwargs['salon_id'])
            salon = models.Salon.objects.get(pk=salon_id)
            master_services = models.MasterService.objects.filter(salon=salon)
            orders = models.Order.objects.none()
            for ms in master_services:
                orders = orders | ms.order_price.all()
            queryset = orders
        
        
        return queryset



@api_view(['POST'])
def filter(request):
    if 'salon_name' in request.data:
        salon_name = request.data.pop('salon_name')
        service_name = request.data.pop('service_name')
        salon = models.Salon.objects.none()
        service = models.Service.objects.none()
        try:
            salon = models.Salon.objects.get(name=salon_name)
            service = models.Service.objects.get(name=service_name)
        except Exception:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        master_services = salon.salon_master_services.filter(service=service)
        masters = []
        for ms in master_services:
            masters.append(ms.master)
        
        master_ser = serializers.MasterSerializer(masters, many=True)
        if masters and salon and master_ser:
            return Response(master_ser.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_200_OK)
    elif 'time' in request.data:
        service_name = request.data.pop('service_name')
        time = request.data.pop('time')
        date = request.data.pop('date')
        service = models.Service.objects.none()
        try:
            service = models.Service.objects.get(name=service_name)
        except Exception:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        master_services = service.master_services.all()
        print(master_services)
        salons = []
        for ms in master_services:
            for order in ms.order_price.all(): 
                print(order)
                if order.date != date and order.time != time:
                    salons.append(ms.salon)
        
        salons = set(salons)
        salon_ser = serializers.SalonSerializer(salons, many=True)
        if service and salons and salon_ser:
            return Response(salon_ser.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_404_NOT_FOUND)
    elif 'master_name' in request.data:
        master_name = request.data.pop('master_name')
        masters = models.CustomUser.objects.get_masters(master_name=master_name)
        master_ser = serializers.MasterSerializer(masters, many=True)
        if masters:
            return Response(master_ser.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_404_NOT_FOUND)

class CommentList(generics.ListCreateAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    lookup_field = 'salon_id'

    def perform_create(self, serializer):
        owner = self.request.user        
        salon = models.Salon.objects.get(pk=self.kwargs[self.lookup_field])
        return serializer.save(owner=owner, salon=salon)

    def get_queryset(self):
        salon = models.Salon.objects.get(pk=self.kwargs[self.lookup_field])
        queryset = salon.salon_comments.all()
        return queryset

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer


class SetClientRating(generics.CreateAPIView):
    queryset = models.ClientRating.objects.all()
    serializers_class = serializers.ClientRatingSerializer

    def create(self, request, *args, **kwargs):
        client = models.Client.objects.get(pk=self.kwargs[self.lookup_field])
        rate = int(request.data.get('rate'))
        serializer = serializers.ClientRatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating = models.ClientRating(client=client, rate=rate, owner = request.user)
        rating.save()
        client.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class SetMasterRating(generics.CreateAPIView):
    queryset = models.MasterRating.objects.all()
    serializers_class = serializers.MasterRatingSerializer

    def create(self, request, *args, **kwargs):
        master = models.Master.objects.get(pk=self.kwargs[self.lookup_field])
        rate = int(request.data.get('rate'))
        serializer = serializers.MasterRatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating = models.MasterRating(master=master, rate=rate, owner = request.user)
        rating.save()
        master.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class SetSalonRating(generics.CreateAPIView):
    queryset = models.SalonRating.objects.all()
    serializers_class = serializers.SalonRatingSerializer

    def create(self, request, *args, **kwargs):
        salon = models.Salon.objects.get(pk=self.kwargs[self.lookup_field])
        rate = int(request.data.get('rate'))
        serializer = serializers.SalonRatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating = models.SalonRating(salon=salon, rate=rate, owner = request.user)
        rating.save()
        salon.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
