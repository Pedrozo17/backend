import cloudinary
import cloudinary.uploader
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .authentication import FirebaseAuthentication
from config.firebase_config import get_firestore_client

class PerfilAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        print(user.__dict__)
        return Response({
            "uid": user.uid,
            "email": user.email,
            "rol": getattr(user, "rol", ""),
            "foto": getattr(user, "foto_url", None),
        })
db = get_firestore_client()

class PerfilImagenAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file_to_upload = request.FILES.get('imagen')

        if not file_to_upload:
            return Response(
                {"error": "no se envio la imagen"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            uid = request.user.uid  # ✅ CORRECTO

            upload_result = cloudinary.uploader.upload(
                file_to_upload,
                folder=f"adso/perfiles/{uid}/",
                public_id="foto_principal",
                overwrite=True
            )

            url_imagen = upload_result.get('secure_url')

            db.collection('perfil').document(uid).set({
                'foto_url': url_imagen
            }, merge=True)

            return Response({
                "mensaje": "foto actualizada correctamente",
                "url": url_imagen
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )