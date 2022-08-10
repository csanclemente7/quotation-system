from django.conf                                      import settings
from django.db.models.query import EmptyQuerySet
from django.http                                      import request
from rest_framework                                   import generics, status
from rest_framework.response                          import Response
from rest_framework.permissions                       import IsAuthenticated
from rest_framework_simplejwt.backends                import TokenBackend
from quotationSystemApp.models.billingStatement                 import BillingStatement
from quotationSystemApp.serializers.billingStatementSerializer   import BillingStatementSerializer

class BillingStatementCreateView(generics.CreateAPIView):
    queryset           = BillingStatement.objects.all()
    serializer_class   = BillingStatementSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        token        = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        serializer = BillingStatementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BillingStatementDetailView(generics.RetrieveAPIView):
    queryset           = BillingStatement.objects.all()
    serializer_class   = BillingStatementSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        token        = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        return super().get_object()

class BillingStatementListView(generics.ListAPIView):
    serializer_class   = BillingStatementSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        token        = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        
        queryset = BillingStatement.objects.all()
        return queryset.order_by('id')

        

class BillingStatementDeleteView(generics.DestroyAPIView):
    queryset = BillingStatement.objects.all()
    serializer_class = BillingStatementSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token, verify=False)

        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail': 'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        try:
            quot = BillingStatement.objects.get(id=kwargs['pk'])
            quot.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BillingStatement.DoesNotExist:
            stringResponse = {'detail': 'cotizacion no existe'}
            return Response(stringResponse, status=status.HTTP_404_NOT_FOUND)        