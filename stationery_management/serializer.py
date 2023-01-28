from rest_framework import serializers
from stationery_management.models import Cost


class CostSerializer(serializers.ModelSerializer):
    class Meta:
          model = Cost
          fields = ['print_cost', 'stationery_id']