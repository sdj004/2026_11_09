import unittest
from unittest.mock import Mock, patch

import ball
import boy
import game_world
import grass
import play_mode
from sdl2 import (SDL_KEYDOWN, SDL_KEYUP, SDLK_0, SDLK_1, SDLK_2,
                  SDLK_i, SDLK_p, SDLK_SPACE)


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

    def test_space_wakes_sleeping_player_without_firing(self):
        with patch.object(boy, 'load_image', return_value=Mock()):
            with patch.object(boy, 'Ball') as ball_factory:
                player = boy.Boy()
                player.fall_asleep()
                event = Mock(type=SDL_KEYDOWN, key=SDLK_SPACE)

                player.handle_event(event)

        self.assertEqual(player.state, 'IDLE')
        ball_factory.assert_not_called()


class PlayModeItemTests(unittest.TestCase):
    def setUp(self):
        game_world.clear()
        self.play_image_patch = patch.object(
            play_mode, 'load_image', side_effect=[Mock(), Mock()]
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
        self.send_events(Mock(type=SDL_KEYDOWN, key=SDLK_i))
        self.assertTrue(play_mode.item_mode)
        self.send_events(Mock(type=SDL_KEYUP, key=SDLK_i))
        self.send_events(Mock(type=SDL_KEYDOWN, key=SDLK_2))
        self.assertFalse(play_mode.item_mode)
        self.assertEqual(play_mode.boy.selected_item, 'large')

        self.assertFalse(play_mode.item_mode)
        self.assertEqual(play_mode.boy.selected_item, 'large')

    def test_open_menu_highlights_selected_item(self):
        play_mode.item_mode = True
        play_mode.boy.selected_item = 'large'

        with patch.object(play_mode, 'clear_canvas'), \
                patch.object(play_mode, 'update_canvas'), \
                patch.object(play_mode, 'get_canvas_width', return_value=800), \
                patch.object(play_mode, 'get_canvas_height', return_value=600), \
                patch.object(game_world, 'render'), \
                patch.object(play_mode, 'draw_rectangle') as draw_rectangle:
            play_mode.render()

        play_mode.item_select_image.draw.assert_called_once_with(400, 300)
        draw_rectangle.assert_called_once_with(
            274, 226, 526, 274, 255, 215, 0
        )

    def test_selecting_item_hides_menu_and_it_can_reopen(self):
        play_mode.item_mode = True
        self.send_events(Mock(type=SDL_KEYDOWN, key=SDLK_1))
        play_mode.item_select_image.draw.reset_mock()

        with patch.object(play_mode, 'clear_canvas'), \
                patch.object(play_mode, 'update_canvas'), \
                patch.object(game_world, 'render'):
            play_mode.render()

        self.assertFalse(play_mode.item_mode)
        play_mode.item_select_image.draw.assert_not_called()

        self.send_events(Mock(type=SDL_KEYUP, key=SDLK_i))
        self.send_events(Mock(type=SDL_KEYDOWN, key=SDLK_i))
        with patch.object(play_mode, 'clear_canvas'), \
                patch.object(play_mode, 'update_canvas'), \
                patch.object(play_mode, 'get_canvas_width', return_value=800), \
                patch.object(play_mode, 'get_canvas_height', return_value=600), \
                patch.object(game_world, 'render'), \
                patch.object(play_mode, 'draw_rectangle'):
            play_mode.render()

        self.assertTrue(play_mode.item_mode)
        play_mode.item_select_image.draw.assert_called_once_with(400, 300)

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

    def test_number_keys_select_each_item(self):
        for key, selected_item in (
                (SDLK_0, 'none'),
                (SDLK_1, 'small'),
                (SDLK_2, 'large')):
            if not play_mode.item_mode:
                self.send_events(Mock(type=SDL_KEYUP, key=SDLK_i))
                self.send_events(Mock(type=SDL_KEYDOWN, key=SDLK_i))
            self.send_events(Mock(type=SDL_KEYDOWN, key=key))
            self.assertFalse(play_mode.item_mode)
            self.assertEqual(play_mode.boy.selected_item, selected_item)

    def test_pause_stops_updates_and_takes_overlay_precedence(self):
        class UpdateCounter:
            updates = 0

            def update(self):
                self.updates += 1

            def draw(self):
                pass

        counter = UpdateCounter()
        game_world.add_oject(counter)
        play_mode.item_mode = True
        self.send_events(Mock(type=SDL_KEYDOWN, key=SDLK_p))
        play_mode.update()

        self.assertTrue(play_mode.paused)
        self.assertEqual(counter.updates, 0)

        play_mode.item_select_image.draw.reset_mock()
        with patch.object(play_mode, 'clear_canvas'), \
                patch.object(play_mode, 'update_canvas'), \
                patch.object(play_mode, 'get_canvas_width', return_value=800), \
                patch.object(play_mode, 'get_canvas_height', return_value=600), \
                patch.object(game_world, 'render'), \
                patch.object(play_mode, 'draw_rectangle') as draw_rectangle:
            play_mode.render()

        play_mode.pause_image.draw.assert_called_once_with(400, 300)
        play_mode.item_select_image.draw.assert_not_called()
        draw_rectangle.assert_not_called()


if __name__ == '__main__':
    unittest.main()
