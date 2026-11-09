import unittest
from unittest.mock import Mock, patch

import ball
import boy
import game_world
import grass
import play_mode
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_2, SDLK_i


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


class PlayModeItemTests(unittest.TestCase):
    def setUp(self):
        game_world.clear()
        self.play_image_patch = patch.object(
            play_mode, 'load_image', return_value=Mock()
        )
        self.boy_image_patch = patch.object(
            boy, 'load_image', return_value=Mock()
        )
        self.grass_image_patch = patch.object(
            grass, 'load_image', return_value=Mock()
        )
        self.play_image_patch.start()
        self.boy_image_patch.start()
        self.grass_image_patch.start()
        play_mode.init()

    def tearDown(self):
        play_mode.finish()
        self.play_image_patch.stop()
        self.boy_image_patch.stop()
        self.grass_image_patch.stop()

    def send_events(self, *events):
        with patch.object(play_mode, 'get_events', return_value=events):
            play_mode.handle_events()

    def test_item_mode_toggles_and_selection_persists(self):
        self.send_events(Mock(type=SDL_KEYDOWN, key=SDLK_i))
        self.assertTrue(play_mode.item_mode)
        self.send_events(Mock(type=SDL_KEYUP, key=SDLK_i))
        self.send_events(Mock(type=SDL_KEYDOWN, key=SDLK_2))
        self.assertEqual(play_mode.boy.selected_item, 'large')
        self.send_events(Mock(type=SDL_KEYUP, key=SDLK_i))
        self.send_events(Mock(type=SDL_KEYDOWN, key=SDLK_i))

        self.assertFalse(play_mode.item_mode)
        self.assertEqual(play_mode.boy.selected_item, 'large')

    def test_world_updates_while_item_mode_is_open(self):
        class UpdateCounter:
            updates = 0

            def update(self):
                self.updates += 1

            def draw(self):
                pass

        counter = UpdateCounter()
        game_world.add_oject(counter)
        play_mode.item_mode = True

        play_mode.update()

        self.assertEqual(counter.updates, 1)


if __name__ == '__main__':
    unittest.main()
