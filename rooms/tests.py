from rest_framework.test import APITestCase

from users.models import User

from . import models


class TestAmenities(APITestCase):
    """Test for Amenities view"""

    NAME = "Amenity Test"
    DESC = "AMenity Des"
    URL = "http://127.0.0.1:8000/api/v1/rooms/amenities/"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_get_amenities(self):
        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Status code is not 200.",
        )
        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["name"],
            self.NAME,
        )
        self.assertEqual(
            data[0]["description"],
            self.DESC,
        )

    def test_post_amenities(self):
        new_amenity_name = "new_amenity"
        new_amenity_desc = "new amenity desc"
        response = self.client.post(
            self.URL,
            data={
                "name": new_amenity_name,
                "description": new_amenity_desc,
            },
        )
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code.",
        )

        self.assertEqual(
            data.get("name"),
            new_amenity_name,
        )
        self.assertEqual(
            data.get("description"),
            new_amenity_desc,
        )

        response = self.client.post(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)


class TestAmenitiy(APITestCase):
    NAME = "TEST AMENITY"
    DESC = "TEST DSC"
    KIMCHI = "kimchi"

    def setUp(self):
        models.Amenity.objects.create(name=self.NAME, description=self.DESC)

    def test_amenity_not_found(self):
        response = self.client.get("/api/v1/rooms/amenities/2")
        self.assertEqual(
            response.status_code,
            404,
        )

    def test_get_amenity(self):

        response = self.client.get("/api/v1/rooms/amenities/1")
        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()
        self.assertEqual(
            data["name"],
            self.NAME,
        )
        self.assertEqual(
            data["description"],
            self.DESC,
        )

    def test_put_amenity(self):
        # updating amenity that doesn't exist.
        response = self.client.put("/api/v1/rooms/amenities/2")
        self.assertEqual(response.status_code, 404)

        # updated successfully.
        response = self.client.put(
            "/api/v1/rooms/amenities/1",
            data={
                "name": self.KIMCHI,
            },
        )
        self.assertEqual(response.status_code, 200)

        # updated data check
        data = response.json()
        self.assertEqual(data["name"], self.KIMCHI)

    def test_delete_amenity(self):
        response = self.client.delete("/api/v1/rooms/amenities/1")
        self.assertEqual(response.status_code, 204)


class TestRooms(APITestCase):

    def setUp(self):
        user = User.objects.create(username="test")
        user.set_password("123")
        user.save()
        self.user = user

    def test_create_room(self):
        response = self.client.post("/api/v1/rooms/")
        self.assertEqual(response.status_code, 403)

        # self.client.login(
        #     username="test",
        #     password="123",
        # )
        self.client.force_login(
            self.user,
        )
        response = self.client.post("/api/v1/rooms/")
        print(response)
