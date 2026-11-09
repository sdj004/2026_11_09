import unittest
from unittest.mock import Mock, patch

import ball
import boy


class BallImageTests(unittest.TestCase):
    def setUp(self):
        ball.Ball.images.clear()

    @patch.object(ball, 'load_image')
    def test_ball_caches_images_by_resource(self, load_image):
        small_image = Mock()
        large_image = Mock()
        load_image.side_effect = [small_image, large_image]

        small_ball = ball.Ball(10, 20, 5)
        large_ball = ball.Ball(10, 20, 5, 'ball41x41.png')
        another_large_ball = ball.Ball(30, 40, -5, 'ball41x41.png')

        self.assertIs(small_ball.image, small_image)
        self.assertIs(large_ball.image, large_image)
        self.assertIs(another_large_ball.image, large_image)
        self.assertEqual(load_image.call_count, 2)


class BoyItemTests(unittest.TestCase):
    def test_selected_large_ball_uses_large_resource(self):
        with patch.object(boy, 'load_image', return_value=Mock()):
            with patch.object(boy, 'Ball') as ball_factory:
                with patch.object(boy.game_world, 'add_oject') as add_object:
                    player = boy.Boy()
                    player.selected_item = 'large'

                    player.fire_ball()

        ball_factory.assert_called_once_with(
            400, 90, 10, 'ball41x41.png'
        )
        add_object.assert_called_once_with(ball_factory.return_value)

    def test_empty_item_does_not_create_ball(self):
        with patch.object(boy, 'load_image', return_value=Mock()):
            with patch.object(boy, 'Ball') as ball_factory:
                player = boy.Boy()
                player.selected_item = 'none'

                player.fire_ball()

        ball_factory.assert_not_called()


if __name__ == '__main__':
    unittest.main()
