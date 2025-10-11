import unittest
from app import app, db, User
import time

class AuthTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up a test app context and a test client."""
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        
        # The @app.before_request hook in app.py handles seeding,
        # but we ensure the tables exist for the test context.
        db.create_all()

    def tearDown(self):
        """Clean up the app context."""
        self.app_context.pop()

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