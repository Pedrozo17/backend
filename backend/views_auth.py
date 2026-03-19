import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth, firestore
from config.firebase_config import get_firestore_client

db = get_firestore_client()

class RegistroAPIView(APIView):
    #endoint para registrar usuarios con email y contraseña

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email y contraseña son requeridos"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # crear el usuario en firebase
            user = auth.create_user(email=email, password=password)

            #crear perfil en firestore
            db.collection('perfil').document(user.uid).set({
                "email": email,
                'rol': 'aprendiz',
                'fecha_registro' : firestore.SERVER_TIMESTAMP
            })

            return Response({
                "mensaje": "Usuario registrado exitosamente",
                "uid": user.uid   
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class LoginAPIView(APIView):
    #endpoint publico que valida las credenciales y obtiene el JWT de firebase
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        api_key = os.getenv("FIREBASE_API_WEB_KEY")
        if not email or not password:
            return Response({"error": "Email y contraseña son requeridos"}, status=status.HTTP_400_BAD_REQUEST)
        
        #endpoint publicode google para hacer la validacion
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        try:
            response = requests.post(url, json=payload)
            data = response.json()

            if response.status_code == 200:
                return Response({
                    "mensaje": "Login exitoso",
                    "token": data['idToken'],
                    "uid":data['localId']
                }, status=status.HTTP_200_OK)
            else: 
                error_msg = data.get('error', {}).get('message', 'Error desconocido')
                return Response ({"error" : "error de conexion"} , status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

                
