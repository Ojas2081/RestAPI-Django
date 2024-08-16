from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models


class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='Newpassword@12',
            is_staff=True)
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.streamplatform = models.StreamPlatform.objects.create(
            name="Netflix",
            about="#1 Streamin Platform",
            website="https://www.netflix.com"
        )

    def test_streamplatform_create(self):
        data = {
            "name": "Netflix",
            "about": "#1 Streamin Platform",
            "website": "https://www.netflix.com"
        }
        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)

    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_streamplatform_individual(self):
        response = self.client.get(
            reverse('streamplatform-detail', args=(self.streamplatform.id,)))
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_streamplatform_update(self):
        data = {
            "name": "Netflix-Automate",
            "about": "#1 Streamin Platform - put",
            "website": "https://www.netflix.com"
        }
        response = self.client.put(
            reverse('streamplatform-detail', args=(self.streamplatform.id,)), data)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_streamplatform_delete(self):
        response = self.client.delete(
            reverse('streamplatform-detail', args=(self.streamplatform.id,)))
        self.assertEqual(response.status_code,
                         status.HTTP_204_NO_CONTENT)


class WatchListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='Newpassword@12'
        )
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.streamplatform = models.StreamPlatform.objects.create(
            name="Netflix",
            about="#1 Streamin Platform",
            website="https://www.netflix.com"
        )
        self.watchlist = models.WatchList.objects.create(
            platform=self.streamplatform,
            title="example movie",
            storyline="storyline example",
            active=True)

    def test_watchlist_create(self):
        data = {
            "platform": self.streamplatform,
            "title": "example movie",
            "storyline": "storyline example",
            "active": True
        }
        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_watchlist_individual(self):
        response = self.client.get(
            reverse('movie-detail'), args=(self.watchlist.id,))
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_watchlist_update(self):
        data = {
            "platform": self.streamplatform,
            "title": "example movie",
            "storyline": "storyline example",
            "active": True
        }
        response = self.client.put(
            reverse('movie-detail', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_watchlist_delete(self):
        response = self.client.delete(
            reverse('movie-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

# class ReviewTestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username='testuser',
#             password='Newpassword@12'
#             )
#         self.token = Token.objects.get(user__username=self.user.username)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
