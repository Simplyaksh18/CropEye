import unittest
from app import app, db, User
import time
import atexit
import gc
import sqlite3


def _close_leftover_sqlite_connections():
    """Close any leftover sqlite3.Connection objects at interpreter exit."""
    try:
        for obj in gc.get_objects():
            try:
                if isinstance(obj, sqlite3.Connection):
                    try:
                        obj.close()
                    except Exception:
                        pass
            except Exception:
                continue
    except Exception:
        pass


atexit.register(_close_leftover_sqlite_connections)

class AuthTestCase(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        """Class-level teardown to clean up DB engine after all tests in this class run."""
        try:
            # Remove any active sessions
            db.session.remove()
        except Exception:
            pass
        try:
            # Dispose engine to close underlying sqlite connections
            eng = getattr(db, 'engine', None)
            if eng is not None:
                try:
                    eng.dispose()
                except Exception:
                    pass
        except Exception:
            pass

    
    def setUp(self):
        """Set up a test app context and a test client."""
        self.app = app
        # Use an in-memory SQLite database for tests to isolate and avoid lingering file-based connections
        try:
            self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        except Exception:
            pass

        # Push app context after configuration change so Flask-SQLAlchemy uses the in-memory DB
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        # If an engine exists from prior configuration, dispose it so a fresh in-memory engine will be created
        try:
            eng = getattr(db, 'engine', None)
            if eng is not None:
                try:
                    eng.dispose()
                except Exception:
                    pass
        except Exception:
            pass

        # Create tables in the in-memory DB
        db.create_all()
        # Ensure demo user exists for tests that expect it
        try:
            demo_email = 'demo@cropeye.dev'
            if not User.query.filter_by(email=demo_email).first():
                demo = User()
                demo.email = demo_email
                demo.first_name = 'Demo'
                demo.last_name = 'User'
                demo.farm_name = 'Demo Farm'
                demo.location = 'Demo Valley'
                demo.set_password('DemoPass123!')
                db.session.add(demo)
                db.session.commit()
        except Exception:
            # If seeding fails for any reason, continue — tests will reveal issues
            pass

    def tearDown(self):
        """Clean up the app context."""
        # Minimal safe cleanup: remove session and drop test tables
        try:
            db.session.remove()
        except Exception:
            pass

        try:
            db.drop_all()
        except Exception:
            pass

        # Reset the module-level seed flag so the app will reseed demo user on next request
        try:
            import app as _app_mod
            _app_mod._seed_done = False
        except Exception:
            try:
                setattr(self.app, '_seed_done', False)
            except Exception:
                pass

        # Pop the app context
        try:
            self.app_context.pop()
        except Exception:
            pass

        # Run garbage collection as a best-effort cleanup
        try:
            import gc
            gc.collect()
        except Exception:
            pass

    def test_login(self):
        """Test the /api/login endpoint with correct credentials."""
        print("Attempting login with demo@cropeye.dev...")
        resp = self.client.post('/api/login', json={'email': 'demo@cropeye.dev', 'password': 'DemoPass123!'})
        
        print(f"Response Status: {resp.status_code}")
        print(f"Response Body: {resp.json}")
        
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.json)
        if resp.json is not None:
            self.assertIn('token', resp.json)
            self.assertEqual(resp.json.get('user', {}).get('email'), 'demo@cropeye.dev')

    def test_register_new_user(self):
        """Test a successful new user registration."""
        # Use a unique email to avoid conflicts between test runs
        unique_email = f"testuser_{int(time.time())}@example.com"
        print(f"Attempting to register new user: {unique_email}...")
        
        registration_data = {
            'email': unique_email,
            'password': 'TestPassword123!',
            'firstName': 'Test',
            'lastName': 'User'
        }
        
        resp = self.client.post('/api/register', json=registration_data)
        
        print(f"Response Status: {resp.status_code}")
        print(f"Response Body: {resp.json}")
        
        self.assertEqual(resp.status_code, 201)
        self.assertIsNotNone(resp.json)
        if resp.json:
            self.assertIn('token', resp.json)
            self.assertIsNotNone(resp.json.get('user'))
            self.assertEqual(resp.json.get('user', {}).get('email'), unique_email)

    def test_register_existing_user(self):
        """Test registration with an already existing email."""
        print("Attempting to register with existing email demo@cropeye.dev...")
        resp = self.client.post('/api/register', json={'email': 'demo@cropeye.dev', 'password': 'SomePassword123!', 'firstName': 'Another', 'lastName': 'Demo'})
        
        self.assertEqual(resp.status_code, 400)
        self.assertIsNotNone(resp.json)
        if resp.json is not None:
            self.assertEqual(resp.json.get('message'), 'Email already registered')

if __name__ == '__main__':
    print("🧪 Running Login Integration Test...")
    unittest.main()