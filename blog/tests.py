from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase

from . import models


class BlogPostTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create One User
        cls.user = User.objects.create(username='user1')

        # Create One Post
        cls.post1 = models.Post.objects.create(
            title='post1',
            text='this is a description1',
            status=models.Post.STATUS_CHOICES[0][0],  # Published
            author=cls.user,
        )

        # Create Two Post
        cls.post2 = models.Post.objects.create(
            title='post2',
            text='this is a description2',
            status=models.Post.STATUS_CHOICES[1][0],  # Draft
            author=cls.user,
        )

    # def setUp(self):
    #     # Create One User
    #     self.user = User.objects.create(username='user1')
    #
    #     # Create One Post
    #     self.post1 = models.Post.objects.create(
    #         title='post1',
    #         text='this is a description1',
    #         status=models.Post.STATUS_CHOICES[0][0],  # Published
    #         author=self.user,
    #     )
    #
    #     # Create Two Post
    #     self.post2 = models.Post.objects.create(
    #         title='post2',
    #         text='this is a description2',
    #         status=models.Post.STATUS_CHOICES[1][0],  # Draft
    #         author=self.user,
    #     )

    # check function __str__ in file models.py app blog
    def test_post_model_str(self):
        post = self.post1
        self.assertEqual(str(post), post.title)

    def test_post_detail(self):
        self.assertEqual(self.post1.title, 'post1')
        self.assertEqual(self.post1.text, 'this is a description1')

    def test_post_list_url(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_post_list_by_name(self):
        response = self.client.get(reverse('post_list_name'))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_url(self):
        response = self.client.get(f'/blog/{self.post1.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_by_name(self):
        response = self.client.get(reverse('post_detail_name', args=[self.post1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_post_title_on_blog_list_page(self):
        response = self.client.get(reverse('post_list_name'))
        self.assertContains(response, self.post1.title)

    def test_post_title_on_blog_detail_page(self):
        response = self.client.get(reverse('post_detail_name', args=[self.post1.pk]))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)

    def test_should_use_template_render_a_post_list_name(self):
        response = self.client.get(reverse('post_list_name'))
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_should_use_template_render_a_post_detail_name(self):
        response = self.client.get(reverse('post_detail_name', args=[self.post1.pk]))
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_post_list_view_contains_welcome_text(self):
        url = reverse('post_list_name')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome')

    # Check Use Method get_object_or_404 in File View.py
    def test_status_404_if_post_id_not_exist(self):
        response = self.client.get(reverse('post_detail_name', args=[self.post1.id + 2]))
        self.assertEqual(response.status_code, 404)

    # TDD Test Driven Development
    def test_draft_post_not_show_posts_list(self):
        response = self.client.get(reverse('post_list_name'))
        self.assertContains(response, self.post1.title)
        self.assertNotContains(response, self.post2.title)

    def test_create_new_post_url(self):
        response = self.client.get('/blog/create/')
        self.assertEqual(response.status_code, 200)

    def test_create_new_post_url_by_name(self):
        response = self.client.get(reverse('show_form_add_name'))
        self.assertEqual(response.status_code, 200)

    def test_should_use_template_render_a_create_post(self):
        response = self.client.get(reverse('show_form_add_name'))
        self.assertTemplateUsed(response, 'blog/post_create.html')

    def test_check_contain_text_title_and_text_in_post_create(self):
        response = self.client.get(reverse('show_form_add_name'))
        self.assertContains(response, 'Title')
        self.assertContains(response, 'Text')

    # check send data database in page create view
    # redirection
    def test_post_create_view(self):
        response = self.client.post(reverse('show_form_add_name'), {
            'title': 'some title',
            'text': 'this is some text',
            'status': 'pub',
            'author': self.user.id,
        })
        self.assertEqual(response.status_code, 302)  # test redirection
        self.assertEqual(models.Post.objects.last().title, 'some title')
        self.assertEqual(models.Post.objects.last().text, 'this is some text')

    # test The update is done correctly, and it redirects to a page
    def test_post_update_view(self):
        response = self.client.post(reverse('post_update_view_name', args=[self.post2.id]), {
            'title': 'post1 updated',
            'text': 'this is a description1 updated',
            'status': 'pub',
            'author': self.user.id,
        })
        self.assertEqual(response.status_code, 302)  # test redirection
        self.assertEqual(models.Post.objects.last().title, 'post1 updated')
        self.assertEqual(models.Post.objects.last().text, 'this is a description1 updated')

    # test To delete is done correctly, and it redirects to a page
    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete_view_name', args=[self.post1.id]))
        self.assertEqual(response.status_code, 302)  # test redirection
