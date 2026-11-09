import unittest
from unittest.mock import Mock, patch

import ball


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


if __name__ == '__main__':
    unittest.main()
