from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .authentication import FirebaseAuthentication
from config.firebase_config import get_firestore_client

db = get_firestore_client()

class ChatHistorialAPIView(APIView):
    
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        try: 
            mensaje_ref = db.collection('api_chat_mensajes')\
                            .order_by('timestamp', direction='DESCENDING')\
                            .limit(20)\
                            .stream()
            historial = []        
            
            for doc in mensaje_ref:
                data = doc.to_dict()
                historial.append({
                    "id" : doc.id,
                    "usuario" : data.get("usuario", "anonimo"),
                    "mensaje" : data.get("mensaje", ""),
                    "timestap" : data.get("timestamp")
                })
            
            historial.reverse()
            
            return Response(historial, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
