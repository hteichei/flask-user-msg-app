import unittest
from app import app, db, User, Message
from flask_testing import TestCase


class MyAppIntegrationTestCase(unittest.TestCase):
    # def test_user_index(self):
    #     client = app.test_client()

    #         result = client.get('/users')
    #         self.assertIn(b'<h1 class="display-4">USERS</h1>', result.data)
    #         self.assertEqual(result.status_code, 200)

    #     def test_user_show(self):
    #         client = app.test_client()

    #         response = client.get('/users/20')
    #         self.assertEqual(response.status_code, 200)

    #     def test_user_create(self):
    #         self.client = app.test_client()

    #         response = self.client.post(
    #             '/users',
    #             data={
    #                 'first_name': 'John',
    #                 'last_name': 'Dope'
    #             },
    #             follow_redirects=True)
    #         self.assertIn(b'John Dope', response.data)

    # def test_edit(self):
    #     self.client = app.test_client()

    #     response = self.client.get('/users/8/edit')
    #     self.assertIn(b'Coco', response.data)
    #     self.assertIn(b'Butter', response.data)

    # def test_update(self):
    #     client = app.test_client()

    #     response = client.patch(
    #         '/users/8',
    #         data=dict(first_name='Good', last_name='Stuff'),
    #         follow_redirects=True)
    #     self.assertIn(b'Good Stuff', response.data)
    #     self.assertNotIn(b'Coco Butter', response.data)

    # def test_delete(self):
    #     self.client = app.test_client()

    #     response = self.client.delete('/users/6', follow_redirects=True)
    #     self.assertNotIn(b'Hank Teicheira', response.data)

    # def test_message_index(self):
    #     self.client = app.test_client()
    #     response = self.client.get('/users/28/messages')
    #     self.assertEqual(response.status_code, 200)

    # def test_message_show(self):
    #     self.client = app.test_client()
    #     response = self.client.get('/users/17')
    #     self.assertEquals(response.status_code, 200)

    # def test_message_edit(self):
    #     self.client = app.test_client()
    #     response = self.client.get('/user/17/messages/edit')
    #     self.assertEquals(response.status_code, 200)

    # def test_message_create(self):
    #     self.client = app.test_client()
    #     response = self.client.post(
    #         '/users/28/messages',
    #         data=dict(message_content='Bananas'),
    #         follow_redirects=True)
    #     self.assertIn(b'Bananas', response.data)

    # def test_message_update(self):
    #     client = app.test_client()
    #     response = client.patch(
    #         '/user/17/messages',
    #         data=dict(message_content='Gophers'),
    #         follow_redirects=True)
    #     self.assertIn(b'Gophers', response.data)
    #     self.assertNotIn(b'Pineapple', response.data)

    # def test_message_delete(self):
    #     client = app.test_client()
    #     response = client.delete('/users/27/messages', follow_redirects=True)
    #     self.assertNotIn(b'Gophers', response.data)


if __name__ == "__main__":
    unittest.main()