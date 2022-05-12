from django.conf                                      import settings
from django.db.models.query import EmptyQuerySet
from django.http                                      import request
from rest_framework                                   import generics, status
from rest_framework.response                          import Response
from rest_framework.permissions                       import IsAuthenticated
from rest_framework_simplejwt.backends                import TokenBackend
from quotationSystemApp.models.quotation                 import Quotation
from quotationSystemApp.serializers.quotationSerializer   import QuotationSerializer

class QuotationCreateView(generics.CreateAPIView):
    queryset           = Quotation.objects.all()
    serializer_class   = QuotationSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        token        = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        serializer = QuotationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class QuotationDetailView(generics.RetrieveAPIView):
    queryset           = Quotation.objects.all()
    serializer_class   = QuotationSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        token        = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        return super().get_object()

class QuotationListView(generics.ListAPIView):
    serializer_class   = QuotationSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        token        = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        
        queryset = Quotation.objects.all()
        return queryset.order_by('id')

class QuotationUpdateView(generics.UpdateAPIView):
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer
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
        return super().put(request, *args, **kwargs)

class QuotationDeleteView(generics.DestroyAPIView):
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token, verify=False)

        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail': 'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        try:
            quot = Quotation.objects.get(id=kwargs['pk'])
            quot.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Quotation.DoesNotExist:
            stringResponse = {'detail': 'cotizacion no existe'}
            return Response(stringResponse, status=status.HTTP_404_NOT_FOUND)        