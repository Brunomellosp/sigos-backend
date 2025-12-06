from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.services.dashboard_service import get_overview


class DashboardOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = get_overview()
        return Response(data)
