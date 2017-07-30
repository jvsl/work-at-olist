from channels.models import Channel, Category
from rest_framework.test import APITestCase


class TestChannel(APITestCase):

    def test_create_channel(self):
        # Arrange
        channel = {"name": "walmart"}
        # Act
        Channel.objects.create(**channel)
        all_channels = Channel.objects.all()
        # Assert
        self.assertEqual(len(all_channels), 1)
        self.assertEqual(all_channels[0].name, "walmart")

    def test_create_channel_with_one_category(self):
        # Arrange
        channel_name = {"name": "walmart"}
        channel = Channel.objects.create(**channel_name)
        books_category = {"name": "books"}
        # Act
        category = Category.objects.create(**books_category)
        category.channel = channel
        category.save()
        # Assert
        self.assertEqual(books_category.get("name"), category.name)
        self.assertEqual(channel_name.get("name"), category.channel.name)

    def test_create_channel_with_many_categories_and_children(self):
        # Assert
        channel_name = {"name": "walmart"}
        channel = Channel.objects.create(**channel_name)
        books_category = {"name": "books"}

        category_father = Category.objects.create(**books_category)
        category_father.channel = channel
        category_father.save()

        subcategory_action = {"name": "action", "parent": category_father}
        subcategory_romance = {"name": "romance", "parent": category_father}
        # Act
        Category.objects.create(**subcategory_action)
        Category.objects.create(**subcategory_romance)
        # Assert
        all_children = category_father.get_children()
        self.assertEqual(len(all_children), 2)

    def test_create_channel_with_categories_and_subcategories(self):
        # Assert
        channel_name = {"name": "walmart"}
        channel = Channel.objects.create(**channel_name)

        category_books = {"name": "books"}

        category_father = Category.objects.create(**category_books)
        category_father.channel = channel
        category_father.save()

        action_category = {"name": "action", "parent": category_father}
        # Act
        action_category_object = Category.objects.create(**action_category)

        child_of_action_category = {"name": "Game Of Thrones",
                                    "parent": action_category_object}

        child_of_action_category_object = \
            Category.objects.create(**child_of_action_category)
        ancestors = \
            child_of_action_category_object.get_ancestors(ascending=False,
                                                          include_self=False)
        # Assert
        self.assertEqual(child_of_action_category_object.get_root().name,
                         "books")
        self.assertEqual(len(ancestors), 2)