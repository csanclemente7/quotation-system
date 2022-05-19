from django.conf                                             import settings
from django.db.models.query                                  import EmptyQuerySet
from django.http                                             import request
from rest_framework                                          import generics, status
from rest_framework.response                                 import Response
from rest_framework.permissions                              import IsAuthenticated
from rest_framework_simplejwt.backends                       import TokenBackend
from quotationSystemApp.models.item                          import Item
from quotationSystemApp.models.itemsQuotation                import ItemsQuotation
from quotationSystemApp.models.quotation                     import Quotation
from quotationSystemApp.serializers.itemsQuotationSerializer import ItemsQuotationSerializer


class ItemsQuotationCreateView(generics.CreateAPIView):
    queryset           = ItemsQuotation.objects.all()
    serializer_class   = ItemsQuotationSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        token        = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        setTotalItemsQuotation(request.data)

        serializer = ItemsQuotationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        setTotalQuotation(request.data)


        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ItemsQuotationUpdateView(generics.UpdateAPIView):
    queryset = ItemsQuotation.objects.all()
    serializer_class = ItemsQuotationSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        token = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token, verify=False)

        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail': 'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        return super().get_object()

        

    def put(self, request, *args, **kwargs):
        token = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token, verify=False)

        if valid_data['user_id'] != self.kwargs['user']:

            stringResponse = {'detail': 'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        
        setTotalItemsQuotation(request.data)

        super().put(request, *args, **kwargs)

        setTotalQuotation(request.data)
        return super().put(request, *args, **kwargs)


class ItemsQuotationDeleteView(generics.DestroyAPIView):
    queryset           = ItemsQuotation.objects.all()
    serializer_class   = ItemsQuotationSerializer
    permission_classes = (IsAuthenticated,)
    def delete(self, request, *args, **kwargs):
        token        = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)

        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        itemId = kwargs['pk']

        quotationId = ItemsQuotation.objects.get(id=itemId).quotation_id

        requestData = {'quotation':quotationId}
     
        super().delete(request, *args, **kwargs)

        setTotalQuotation(requestData)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ItemsQuotationListView(generics.ListAPIView):
    queryset           = ItemsQuotation.objects.all()
    serializer_class   = ItemsQuotationSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        token        = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)

        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        return super().get(request, *args, **kwargs)


class ItemsQuotationByQuotationListView(generics.ListAPIView):
    queryset           = ItemsQuotation.objects.all()
    serializer_class   = ItemsQuotationSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        token        = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)

        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        quotationId = kwargs['pk']

        queryset = ItemsQuotation.objects.filter(quotation_id=quotationId)

        serializer = ItemsQuotationSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

        
        
        


        # Functions to set the total of the quotation and the total of the items quotation


# calcular total itemsQuotation
def setTotalItemsQuotation(requestData):
        price = requestData['price']
        quantity = requestData['quantity']
        total = int(price) * int(quantity)
        requestData['total'] = total


# calcular total quotation
def setTotalQuotation(requestData):
    quotation = Quotation.objects.get(id= requestData['quotation'])

    iva = quotation.iva
    discount = quotation.discount
    itemsQuotationByQuotation = ItemsQuotation.objects.filter(quotation_id=quotation.id)
    subTotalItemsQuotation = 0
    totalDiscount = 0
    totalIva = 0
    totalItemsQuotation = 0
    for itemQuotation in itemsQuotationByQuotation:
        subTotalItemsQuotation += itemQuotation.total
    totalDiscount = subTotalItemsQuotation * (discount/100)
    totalIva = (subTotalItemsQuotation - totalDiscount) * (iva/100)
    totalItemsQuotation = subTotalItemsQuotation - totalDiscount + totalIva
    quotation.subtotal = subTotalItemsQuotation
    quotation.totalDiscount = totalDiscount
    quotation.totalIva = totalIva
    quotation.total = totalItemsQuotation
    quotation.save()




