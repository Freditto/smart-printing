from django.shortcuts import render
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from stationery_management.models import Stationery, Cost, Document
from stationery_management.serializer import CostSerializer
from users_management.models import User
from django.db.models import Q


# Create your views here.
@api_view(["GET"])
@permission_classes([AllowAny])
def stationery_list(request):
    stationeries = Stationery.objects.values("id", "name", "logo", "description", "created_by").all()
    response = {
        'data': stationeries
    }
    return Response(response)


def calculate_cost(pages, no_copies, price):
    total_cost = int(price) * int(pages) * int(no_copies)

    return total_cost


@api_view(["POST"])
@permission_classes([AllowAny])
def create_doc(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            pages = request.POST.get('pages')
            file_doc = request.POST.get('file_doc')
            no_copies = request.POST.get('no_copies')
            user_id = User.objects.get(id=request.POST.get('user_id'))
            stationery_id = Stationery.objects.get(id=request.POST.get('stationery_id'))
            price = Cost.objects.values('print_cost').get(Q(stationery_id=stationery_id) and Q(is_active=True))[
                'print_cost']
            total_cost = calculate_cost(pages, no_copies, price)

            document = Document.objects.create(name=name, pages=pages, file_doc=file_doc, no_copies=no_copies,
                                               user_id=user_id, stationery_id=stationery_id, total_cost=total_cost, )
            document.save()
            response = {
                'message': "create successfully"

            }
            return Response(response)
        except Exception as e:
            print(e)
            return Response("Invalid", status=401)


class CostView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = CostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(True)
        return Response(serializer.errors)


@api_view(["POST"])
@permission_classes([AllowAny])
def document_list(request):
    if request.method == 'POST':
        print(request.POST.get('stationery_id'))

        stationery_id = Stationery.objects.get(id=request.POST.get('stationery_id'))
        documents = Document.objects.values('id', 'name', 'pages', 'no_copies', 'total_cost', 'status').filter(
            stationery_id=stationery_id)

    response = {
        'data': documents
    }

    return Response(response)
