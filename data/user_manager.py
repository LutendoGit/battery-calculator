"""
User management functions for creating, updating, and tracking users.
"""
import sqlite3
from datetime import datetime, timedelta
from data.database import get_db
import bcrypt
import secrets


class UserManager:
    """Handles all user-related database operations."""
    
    @staticmethod
    def create_user(username, email, password, full_name=None):
        """Create a new user with hashed password."""
        try:
            # Hash password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (username, email, password_hash, full_name)
                    VALUES (?, ?, ?, ?)
                ''', (username, email, password_hash, full_name))
                conn.commit()
                return {"success": True, "user_id": cursor.lastrowid}
        except sqlite3.IntegrityError:
            return {"success": False, "error": "Username or email already exists"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_user_by_id(user_id):
        """Retrieve user by ID."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, username, email, full_name, created_at, is_active
                FROM users WHERE id = ? AND is_active = 1
            ''', (user_id,))
            user = cursor.fetchone()
            return dict(user) if user else None
    
    @staticmethod
    def get_user_by_username(username):
        """Retrieve user by username."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM users WHERE username = ? AND is_active = 1
            ''', (username,))
            user = cursor.fetchone()
            return dict(user) if user else None
    
    @staticmethod
    def get_user_by_email(email):
        """Retrieve user by email."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM users WHERE email = ? AND is_active = 1
            ''', (email,))
            user = cursor.fetchone()
            return dict(user) if user else None
    
    @staticmethod
    def authenticate_user(username, password):
        """Authenticate user and return user data if successful."""
        user = UserManager.get_user_by_username(username)
        if not user:
            return None
        
        # Verify password
        if bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
            return {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'full_name': user['full_name']
            }
        return None
    
    @staticmethod
    def update_user(user_id, **kwargs):
        """Update user information."""
        allowed_fields = {'username', 'email', 'full_name'}
        fields_to_update = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not fields_to_update:
            return {"success": False, "error": "No valid fields to update"}
        
        try:
            fields_to_update['updated_at'] = datetime.now()
            set_clause = ', '.join(f"{k} = ?" for k in fields_to_update.keys())
            values = list(fields_to_update.values()) + [user_id]
            
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(f'''
                    UPDATE users SET {set_clause} WHERE id = ?
                ''', values)
                conn.commit()
                return {"success": True}
        except sqlite3.IntegrityError:
            return {"success": False, "error": "Username or email already exists"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def delete_user(user_id, soft_delete=True):
        """Delete user (soft delete by default)."""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                if soft_delete:
                    cursor.execute('''
                        UPDATE users SET is_active = 0 WHERE id = ?
                    ''', (user_id,))
                else:
                    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
                conn.commit()
                return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_all_users(limit=100, offset=0):
        """Get all active users."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, username, email, full_name, created_at, is_active
                FROM users WHERE is_active = 1
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            users = cursor.fetchall()
            return [dict(user) for user in users]


class SessionManager:
    """Handles user session and token management."""
    
    @staticmethod
    def create_session(user_id, expires_in_days=7):
        """Create a new session token for a user."""
        try:
            token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(days=expires_in_days)
            
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO user_sessions (user_id, token, expires_at)
                    VALUES (?, ?, ?)
                ''', (user_id, token, expires_at))
                conn.commit()
                return {"success": True, "token": token}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def verify_token(token):
        """Verify token and return user_id if valid."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT user_id FROM user_sessions
                WHERE token = ? AND expires_at > datetime('now')
            ''', (token,))
            session = cursor.fetchone()
            return session['user_id'] if session else None
    
    @staticmethod
    def revoke_token(token):
        """Revoke a session token."""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM user_sessions WHERE token = ?', (token,))
                conn.commit()
                return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def cleanup_expired_sessions():
        """Remove expired session tokens."""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    DELETE FROM user_sessions WHERE expires_at <= datetime('now')
                ''')
                conn.commit()
                return {"success": True, "deleted": cursor.rowcount}
        except Exception as e:
            return {"success": False, "error": str(e)}


class ActivityLogger:
    """Handles user activity tracking."""
    
    @staticmethod
    def log_activity(user_id, action, details=None, ip_address=None):
        """Log a user action."""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO user_activity (user_id, action, details, ip_address)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, action, details, ip_address))
                conn.commit()
                return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_user_activity(user_id, limit=100):
        """Get activity log for a user."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM user_activity
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (user_id, limit))
            activities = cursor.fetchall()
            return [dict(activity) for activity in activities]
    
    @staticmethod
    def get_recent_activity(limit=100):
        """Get recent activity across all users."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM user_activity
                ORDER BY created_at DESC
                LIMIT ?
            ''', (limit,))
            activities = cursor.fetchall()
            return [dict(activity) for activity in activities]


class CalculationHistory:
    """Track user calculator usage."""
    
    @staticmethod
    def save_calculation(user_id, calc_type, input_data, result_text, chemistry, dod):
        """Save a calculation to user history."""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO calculation_history 
                    (user_id, calc_type, input_data, result_text, chemistry, dod)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, calc_type, input_data, result_text, chemistry, dod))
                conn.commit()
                return {"success": True, "id": cursor.lastrowid}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_user_calculations(user_id, limit=50):
        """Get calculation history for a user."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM calculation_history
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (user_id, limit))
            calculations = cursor.fetchall()
            return [dict(calc) for calc in calculations]
    
    @staticmethod
    def get_calculation_by_id(calc_id, user_id):
        """Get a specific calculation."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM calculation_history
                WHERE id = ? AND user_id = ?
            ''', (calc_id, user_id))
            calc = cursor.fetchone()
            return dict(calc) if calc else None
