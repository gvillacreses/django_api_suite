from django.shortcuts import render


# Importación de módulos necesarios
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import firebase_admin
from firebase_admin import db
import datetime

# Inicialización de Firebase Admin SDK (asegúrate de que tu configuración esté correcta)
if not firebase_admin._apps:
    firebase_admin.initialize_app(options={
        'databaseURL': 'https://tu-base-de-datos.firebaseio.com/'  # Reemplaza con la URL de tu base de datos
    })

class LandingAPI(APIView):
    # Atributos de la clase
    name = "Landing API"
    collection_name = "appointments"  # Nombre de la colección en Firebase Realtime Database

    def get(self, request):

        # Referencia a la colección
        ref = db.reference(f'{self.collection_name}')

        # get: Obtiene todos los elementos de la col ección
        data = ref.get()

        # Devuelve un arreglo JSON
        return Response(data, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data

        # Referencia a la colección
        ref = db.reference(f'{self.collection_name}')

        current_time  = datetime.now()
        custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
        data.update({"timestamp": custom_format })

        # push: Guarda el objeto en la colección
        new_resource = ref.push(data)

        # Devuelve el id del objeto guardado
        return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """
        Método para actualizar datos en la colección de Firebase.
        """
        try:
            ref = db.reference(self.collection_name)
            item_id = kwargs.get('item_id')
            data_to_update = request.data
            item_ref = ref.child(item_id)
            item_ref.update(data_to_update)
            return Response({"message": "Data successfully updated."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        """
        Método para eliminar datos de la colección en Firebase.
        """
        try:
            ref = db.reference(self.collection_name)
            item_id = kwargs.get('item_id')
            item_ref = ref.child(item_id)
            item_ref.delete()
            return Response({"message": "Data successfully deleted."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

