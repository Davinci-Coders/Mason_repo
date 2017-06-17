# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from story.forms import PostForm
from story.models import Post


class TestViews(TestCase):
    def setUp(self):
        self.post_obj = Post(author='guy', title='story 1', text='my story')
        self.post_obj.save()

        self.user = User(username='user', first_name='first', last_name='last', email='human@email.com')
        self.user.set_password('password')
        self.user.save()

    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_story(self):
        response = self.client.get(reverse('story'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context[0]['posts']), len(Post.objects.all()))

    def test_specific(self):
        response = self.client.get(reverse('specific', kwargs={'blog_id': self.post_obj.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0]['post'], self.post_obj)

    def test_post_new_anon(self):
        response = self.client.get(reverse('post_new'))
        self.assertEqual(response.status_code, 302)

    def test_post_new_valid_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('post_new'))
        self.assertEqual(response.status_code, 200)

        self.assertIsInstance(response.context[0]['form'], PostForm)

        # more examples of how to use assertIsInstance
        self.assertIsInstance(self.user, User)
        self.assertIsInstance(self.post_obj, Post)

    def test_post_new_valid_post(self):
        self.client.force_login(self.user)
        data = {
            'author': 'the amazing string',
            'title': 'yet another title',
            'text': 'lorem ipsum stuff...',
        }

        # store the original count of how many posts exist
        posts_count = Post.objects.count()
        # equivalent of
        # posts_count = len(Post.objects.all())

        response = self.client.post(reverse('post_new'), data)
        self.assertEqual(response.status_code, 200)

        # check that the total number of posts has increased by 1
        # when the client sends in valid data to save
        new_posts_count = Post.objects.count()
        self.assertEqual(new_posts_count, posts_count + 1)
