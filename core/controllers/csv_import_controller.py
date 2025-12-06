import csv
import io

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from core.serializers.orders import OrderServiceSerializer
from core.services.order_service import create_order


class OrderServiceCSVImportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response(
                {"detail": "Arquivo CSV é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        decoded = file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(decoded))

        created = 0
        errors = []

        for i, row in enumerate(reader, start=1):
            serializer = OrderServiceSerializer(data=row)
            if serializer.is_valid():
                try:
                    create_order(serializer.validated_data, request.user)
                    created += 1
                except Exception as e:
                    errors.append({"line": i, "error": str(e)})
            else:
                errors.append({"line": i, "error": serializer.errors})

        return Response(
            {"created": created, "errors": errors},
            status=status.HTTP_200_OK,
        )
