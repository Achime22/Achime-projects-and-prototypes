
from rest_framework import viewsets, permissions
from .models import Agreement, Wallet, Transaction, Mediator
from .serializers import AgreementSerializer, WalletSerializer, TransactionSerializer, MediatorSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class AgreementViewSet(viewsets.ModelViewSet):
    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def finalize(self, request, pk=None):
        agreement = self.get_object()
        if request.user in agreement.parties.all():
            agreement.finalized = True
            agreement.save()
            return Response({'status': 'agreement finalized'})
        return Response({'status': 'not authorized'}, status=status.HTTP_403_FORBIDDEN)

class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

class MediatorViewSet(viewsets.ModelViewSet):
    queryset = Mediator.objects.all()
    serializer_class = MediatorSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
