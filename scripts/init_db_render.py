#!/usr/bin/env python3
"""Initialize database for Render deployment.

This script runs once after deployment via Procfile's 'release' command,
ensuring all required tables exist before the web service starts.

Usage:
    python scripts/init_db_render.py
"""

import os
import sys

# Add project root to path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.education_store import ensure_db


def main():
    """Initialize database and verify tables exist."""
    try:
        print("🔄 Initializing education database...")
        ensure_db()
        print("✅ Database initialized successfully")
        print("✅ All required tables exist")
        return 0
    except Exception as e:
        print(f"❌ Database initialization failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
