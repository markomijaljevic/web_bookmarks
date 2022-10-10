from django.test import TestCase
from bookmark.models import Bookmark
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


class AuthenticatedUserBookmarkViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            username="testUser",
            password="testpass",
        )
        self.client.force_authenticate(self.user)

        Bookmark.objects.create(title="Test title", url="www.test.com")
        Bookmark.objects.create(
            title="Test title", url="www.test.com", private=True, user=self.user
        )

    def test_create_bookmark_good(self):
        response = self.client.post(
            "/api/bookmark/",
            data={
                "title": "Test create bookmark",
                "url": "www.test.com",
            },
        )

        self.assertEqual(response.status_code, 201)

    def test_create_bookmark_bad(self):
        response = self.client.post(
            "/api/bookmark/",
            data={
                "url": "www.test.com",
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_get_bookmark_good(self):
        response = self.client.get("/api/bookmark/1/")

        self.assertEqual(response.status_code, 200)

    def test_get_bookmark_bad(self):
        response = self.client.get("/api/bookmark/test/")

        self.assertEqual(response.status_code, 404)

    def test_update_bookmark_good(self):
        response = self.client.put(
            "/api/bookmark/1/",
            data={
                "title": "put",
                "url": "test",
            },
        )

        self.assertEqual(response.data["title"], "put")

    def test_update_bookmark_bad(self):
        response = self.client.put(
            "/api/bookmark/1/", data={"url": "test"}, content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_delete_bookmark_good(self):
        response = self.client.delete("/api/bookmark/1/")

        self.assertEqual(response.status_code, 204)

    def test_filter_private_bookmark_good(self):
        response = self.client.get("/api/bookmark/", {"private": True})
        private = dict(response.data[0])["private"]

        self.assertTrue(private)

    def test_filter_private_bookmark_by_user_good(self):
        response = self.client.get(
            "/api/bookmark/", {"private": True, "user_id": self.user.id}
        )

        private = dict(response.data[0])["private"]
        user_id = dict(response.data[0])["id"]

        self.assertTrue(private)
        self.assertEqual(user_id, 2)

    def test_filter_public_bookmark_good(self):
        response = self.client.get("/api/bookmark/", {"private": False})
        private = dict(response.data[0])["private"]

        self.assertFalse(private)


class AnonymousUserBookmarkViewSetTest(TestCase):
    def setUp(self):
        Bookmark.objects.create(title="Test title", url="www.test.com")
        Bookmark.objects.create(title="Test title", url="www.test.com", private=True)

    def test_create_bookmark_good(self):
        response = self.client.post(
            "/api/bookmark/",
            data={
                "title": "Test create bookmark",
                "url": "www.test.com",
            },
        )

        self.assertEqual(response.status_code, 401)

    def test_create_bookmark_bad(self):
        response = self.client.post(
            "/api/bookmark/",
            data={
                "url": "www.test.com",
            },
        )

        self.assertEqual(response.status_code, 401)

    def test_get_bookmark_good(self):
        response = self.client.get("/api/bookmark/1/")

        self.assertEqual(response.status_code, 200)

    def test_get_bookmark_bad(self):
        response = self.client.get("/api/bookmark/2/")

        self.assertEqual(response.status_code, 404)

    def test_update_bookmark_good(self):
        response = self.client.put(
            "/api/bookmark/1/",
            data={
                "title": "put",
                "url": "test",
            },
        )

        self.assertEqual(response.status_code, 401)

    def test_delete_bookmark_good(self):
        response = self.client.delete("/api/bookmark/1/")

        self.assertEqual(response.status_code, 401)

    def test_filter_private_bookmark_good(self):
        response = self.client.get("/api/bookmark/", {"private": True})

        self.assertEqual(len(response.data), 0)

    # def test_filter_private_bookmark_by_user_good(self):
    #     response = self.client.get('/api/bookmark/',
    #                                {'private': True, 'user_id': 2})
    #     print(response.data)
    #     self.assertEqual(len(response.data), 0)

    def test_filter_public_bookmark_good(self):
        response = self.client.get("/api/bookmark/", {"private": False})
        private = dict(response.data[0])["private"]

        self.assertFalse(private)


class UsersTest(TestCase):
    def test_create_user_good(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="test", email="test@user.com", password="test"
        )

        self.assertEqual(user.email, "test@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_bad(self):
        User = get_user_model()

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(username="", email="", password="foo")
