from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"
    
    def get(self, request):
        # Filtra la lista para incluir solo los elementos donde 'is_active' es True
        active_items = [item for item in data_list if item.get('is_active', False)]
        return Response(active_items, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data

        # Validación mínima
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        data_list.append(data)

        return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)
    

class DemoRestApiItem(APIView):
    name = "Demo REST API Item"

    def get_object(self, item_id):
        for item in data_list:
            if item['id'] == item_id:
                return item
        return None
    
    def get(self, request, item_id):
        item = self.get_object(item_id)
        if item and item.get('is_active', True):
            return Response(item, status=status.HTTP_200_OK)
        return Response({'error': 'Item no encontrado o inactivo.'}, status=status.HTTP_404_NOT_FOUND)
    
        
    def put(self, request, item_id):
        data = request.data

        if 'id' not in data or data['id'] != item_id:
            return Response(
                {'error': 'El campo "id" es obligatorio y debe coincidir con el ID de la URL.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        for i, item in enumerate(data_list):
            if item['id'] == item_id:
                data['is_active'] = item.get('is_active', True)
                data_list[i] = data
                return Response(
                    {'message': 'Dato reemplazado exitosamente.', 'data': data},
                    status=status.HTTP_200_OK
                )

        return Response({'error': 'Item no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, item_id):
        data = request.data

        for item in data_list:
            if item['id'] == item_id:
                item.update(data)
                return Response(
                    {'message': 'Dato actualizado parcialmente exitosamente.', 'data': item},
                    status=status.HTTP_200_OK
                )

        return Response({'error': 'Item no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, item_id):
        for item in data_list:
            if item['id'] == item_id:
                item['is_active'] = False
                return Response(
                    {'message': 'Dato eliminado lógicamente (inactivado).'},
                    status=status.HTTP_200_OK
                )

        return Response({'error': 'Item no encontrado.'}, status=status.HTTP_404_NOT_FOUND)