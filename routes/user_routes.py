"""
Flask blueprint for user authentication and management routes.
"""
from flask import Blueprint, request, jsonify
from data.user_manager import UserManager, SessionManager, ActivityLogger
from functools import wraps

user_bp = Blueprint('user', __name__, url_prefix='/user')


def login_required(f):
    """Decorator to require login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({"error": "Missing authentication token"}), 401
        
        user_id = SessionManager.verify_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        request.user_id = user_id
        return f(*args, **kwargs)
    return decorated_function


@user_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        full_name = data.get('full_name', '').strip()
        
        # Validation
        if not all([username, email, password]):
            return jsonify({"error": "Missing required fields"}), 400
        
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400
        
        # Create user
        result = UserManager.create_user(username, email, password, full_name)
        
        if result['success']:
            ActivityLogger.log_activity(
                result['user_id'],
                'USER_REGISTERED',
                f'User {username} registered',
                request.remote_addr
            )
            return jsonify({
                "success": True,
                "message": "User registered successfully",
                "user_id": result['user_id']
            }), 201
        else:
            return jsonify({"error": result['error']}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route('/login', methods=['POST'])
def login():
    """Login user and return session token."""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({"error": "Missing username or password"}), 400
        
        # Authenticate
        user = UserManager.authenticate_user(username, password)
        
        if not user:
            ActivityLogger.log_activity(
                None,
                'FAILED_LOGIN',
                f'Failed login attempt for {username}',
                request.remote_addr
            )
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Create session
        session_result = SessionManager.create_session(user['id'])
        
        if session_result['success']:
            ActivityLogger.log_activity(
                user['id'],
                'USER_LOGIN',
                f'User {username} logged in',
                request.remote_addr
            )
            return jsonify({
                "success": True,
                "token": session_result['token'],
                "user": user
            }), 200
        else:
            return jsonify({"error": "Failed to create session"}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Logout user by revoking token."""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        result = SessionManager.revoke_token(token)
        
        if result['success']:
            ActivityLogger.log_activity(
                request.user_id,
                'USER_LOGOUT',
                'User logged out',
                request.remote_addr
            )
            return jsonify({"success": True, "message": "Logged out successfully"}), 200
        else:
            return jsonify({"error": result['error']}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    """Get current user profile."""
    try:
        user = UserManager.get_user_by_id(request.user_id)
        if user:
            return jsonify({"success": True, "user": user}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    """Update user profile."""
    try:
        data = request.get_json()
        result = UserManager.update_user(request.user_id, **data)
        
        if result['success']:
            ActivityLogger.log_activity(
                request.user_id,
                'PROFILE_UPDATED',
                f'User updated profile',
                request.remote_addr
            )
            user = UserManager.get_user_by_id(request.user_id)
            return jsonify({"success": True, "user": user}), 200
        else:
            return jsonify({"error": result['error']}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route('/activity', methods=['GET'])
@login_required
def get_activity():
    """Get user activity log."""
    try:
        limit = request.args.get('limit', 100, type=int)
        activities = ActivityLogger.get_user_activity(request.user_id, limit)
        return jsonify({"success": True, "activities": activities}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route('/admin/users', methods=['GET'])
@login_required
def admin_get_users():
    """Admin endpoint: Get all users."""
    # TODO: Add admin role check
    try:
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        users = UserManager.get_all_users(limit, offset)
        return jsonify({"success": True, "users": users}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    """Admin endpoint: Delete a user."""
    # TODO: Add admin role check
    try:
        soft_delete = request.json.get('soft_delete', True)
        result = UserManager.delete_user(user_id, soft_delete)
        
        if result['success']:
            ActivityLogger.log_activity(
                request.user_id,
                'ADMIN_DELETE_USER',
                f'Admin deleted user {user_id}',
                request.remote_addr
            )
            return jsonify({"success": True, "message": "User deleted"}), 200
        else:
            return jsonify({"error": result['error']}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
