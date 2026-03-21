from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from firebase_admin import auth
from config.firebase_config import get_firestore_client
import firebase_admin

db = get_firestore_client()

class FirebaseAuthentication(BaseAuthentication):
    # leer el token JWT del encabezado, lo va a validar y va a  extraer el UID del usuario
    def authenticate(self, request):
        # extraernos el token
        auth_header = request.META.get(
            'HTTP_AUTHORIZATION') or request.headers.get('Authorization')
        if not auth_header:
            return None  # no hay token

        # el token viene "bearer <token>"
        partes = auth_header.split()
        if len(partes) != 2 or partes[0].lower() != 'bearer':
            return None  # formato de token no valido

        token = partes[1]

        try:
            # firebase va a validar la firma
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token.get('uid')
            email = decoded_token.get('email')
        except Exception as e:
            print(f"❌ Error validando token Firebase: {e}")  # 👈 agrega esto
            raise AuthenticationFailed('Token no válido o expirado')
        try:
            user_profile = db.collection('perfil').document(uid).get()
            foto_url = user_profile.to_dict().get("foto_url", "sin foto") if user_profile.exists else "sin foto"
            rol = user_profile.to_dict().get('rol', 'aprendiz').strip() if user_profile.exists else 'aprendiz'
            # usuario
        except Exception as e:
         print(f"❌ Error consultando Firestore: {e}")  # 👈 y esto
         foto_url = "sin foto"  # fallback en vez de romper todo
         rol = "aprendiz"
        try:
            class FirebaseUser:
                def __init__(self,uid):
                    self.uid = uid
                    self.rol = rol
                    self.email = email
                    self.foto_url = foto_url
                    self.is_authenticated = True

            return (FirebaseUser(uid), decoded_token)

        except Exception as e:
            raise AuthenticationFailed('Token no válido o esta expirado')
