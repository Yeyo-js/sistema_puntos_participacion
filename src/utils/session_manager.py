"""
Gestor de Sesiones y Tokens de Seguridad
Maneja recordar sesión, tokens y PINs
"""
import json
import secrets
from pathlib import Path
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class SessionManager:
    """Gestor de sesiones persistentes"""
    
    def __init__(self):
        # Archivo para guardar sesiones (en data/)
        self.session_file = Path("data/session.json")
        self.session_file.parent.mkdir(exist_ok=True)
    
    def generate_token(self):
        """Generar token seguro aleatorio"""
        return secrets.token_urlsafe(32)
    
    def save_session(self, username, token, remember_me=False, pin=None):
        """
        Guardar sesión del usuario
        Args:
            username: Nombre de usuario
            token: Token de sesión
            remember_me: Si debe recordar la sesión
            pin: PIN de 4 dígitos (opcional)
        """
        try:
            # Calcular fecha de expiración
            if remember_me:
                expires_at = (datetime.now() + timedelta(days=7)).isoformat()
            else:
                expires_at = (datetime.now() + timedelta(hours=1)).isoformat()
            
            session_data = {
                'username': username,
                'token': token,
                'remember_me': remember_me,
                'pin': pin,
                'expires_at': expires_at,
                'created_at': datetime.now().isoformat()
            }
            
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            logger.info(f"Sesión guardada para: {username} (recordar: {remember_me})")
            return True
            
        except Exception as e:
            logger.error(f"Error al guardar sesión: {e}")
            return False
    
    def load_session(self):
        """
        Cargar sesión guardada
        Returns:
            dict con datos de sesión o None
        """
        try:
            if not self.session_file.exists():
                return None
            
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            
            # Verificar si la sesión ha expirado
            expires_at = datetime.fromisoformat(session_data['expires_at'])
            
            if datetime.now() > expires_at:
                logger.info("Sesión expirada")
                self.clear_session()
                return None
            
            logger.info(f"Sesión cargada: {session_data['username']}")
            return session_data
            
        except Exception as e:
            logger.error(f"Error al cargar sesión: {e}")
            return None
    
    def clear_session(self):
        """Eliminar sesión guardada"""
        try:
            if self.session_file.exists():
                self.session_file.unlink()
            logger.info("Sesión eliminada")
            return True
        except Exception as e:
            logger.error(f"Error al eliminar sesión: {e}")
            return False
    
    def verify_token(self, username, token):
        """
        Verificar si el token es válido
        Args:
            username: Nombre de usuario
            token: Token a verificar
        Returns:
            bool: True si es válido
        """
        session = self.load_session()
        
        if not session:
            return False
        
        return (session['username'] == username and 
                session['token'] == token)
    
    def has_pin(self):
        """Verificar si hay un PIN guardado"""
        session = self.load_session()
        return session and session.get('pin') is not None
    
    def verify_pin(self, pin):
        """
        Verificar PIN
        Args:
            pin: PIN de 4 dígitos
        Returns:
            dict con username si es válido, None si no
        """
        session = self.load_session()
        
        if not session or not session.get('pin'):
            return None
        
        if session['pin'] == pin:
            return {'username': session['username']}
        
        return None
    
    def update_pin(self, pin):
        """Actualizar PIN de la sesión actual"""
        try:
            session = self.load_session()
            if not session:
                return False
            
            session['pin'] = pin
            
            with open(self.session_file, 'w') as f:
                json.dump(session, f, indent=2)
            
            logger.info("PIN actualizado")
            return True
            
        except Exception as e:
            logger.error(f"Error al actualizar PIN: {e}")
            return False


# Instancia global
session_manager = SessionManager()
