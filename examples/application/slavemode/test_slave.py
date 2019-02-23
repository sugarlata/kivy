'''
Test showing using a slave mode of Kivy main loop while testing
a root widget from an application changing its text after some
time period.

.. versionadded:: 1.11.0
'''

import unittest
from os import environ


class SimpleTestCase(unittest.TestCase):
    '''
    Simple TestCase setting & unsetting slave mode and showcasing
    testing with runTouchApp() + stopTouchApp() with a Window being
    opened and closed and testing with a custom application main loop
    and Kivy being run in the slave mode.

    .. versionadded:: 1.11.0
    '''

    @classmethod
    def setUpClass(cls):
        '''
        Set slave mode just for this test case.

        Any tests running in normal mode will most likely have
        global variables present, therefore it's reasonable
        to assume failure while mixing the modes.

        .. versionadded:: 1.11.0
        '''
        environ['KIVY_SLAVE_MODE'] = '1'

    @classmethod
    def tearDownClass(cls):
        '''
        Clean slave mode flag from the environment.

        It should allow any normal mode tests to run properly even if
        a slave mode test ran prior to normal ones due to slave mode
        not importing the ``kivy.core.window`` module.

        .. versionadded:: 1.11.0
        '''
        if 'KIVY_SLAVE_MODE' in environ:
            del environ['KIVY_SLAVE_MODE']

    def test_widget(self):
        # pylint: disable=protected-access
        '''
        Test a root widget by using slave mode, spawning your own Window
        manually and pushing the frames forward by yourself with the
        EventLoop.idle().

        .. versionadded:: 1.11.0
        '''

        from kivy.clock import Clock
        from kivy.base import EventLoop
        from kivy.app import runTouchApp, stopTouchApp
        from simpleapp import Simple

        # get OpenGL window
        import kivy.core.window
        kivy.core.window.Window = kivy.core.window.get_core_window()
        EventLoop.ensure_window()

        # get widget from App instance and run it
        app = Simple()
        widget = app.build()
        runTouchApp(widget)

        # manage the event loop
        frames = 60
        delta = 5
        for frame in range(frames):
            EventLoop.idle()

            # on 30th frame, i.e. on 0.5s the Clock.schedule_once
            # is triggered and the text has been changed since
            # however it's not accurate to the single frame,
            # therefore approximate with some delta
            if frame < Clock._max_fps * app.INTERVAL - delta:
                self.assertEqual(widget.text, app.TEXT_DEFAULT)
            elif frame > Clock._max_fps * app.INTERVAL + delta:
                self.assertEqual(widget.text, app.TEXT_CHANGED)

        # destroy the window and stop eventloop
        EventLoop.window.close()
        stopTouchApp()

    def mainloop_widget_hook(self, frame, fps, widget, app):
        '''
        Custom main loop hook used for testing.

        .. versionadded:: 1.11.0
        '''

        delta = 5
        if frame < fps * app.INTERVAL + delta:
            self.assertEqual(widget.text, app.TEXT_DEFAULT)
        elif frame > fps * app.INTERVAL - delta:
            self.assertEqual(widget.text, app.TEXT_CHANGED)

    def test_mainloop_widget(self):
        # pylint: disable=no-else-return,protected-access,too-many-locals
        '''
        Test a root widget by using slave mode, spawning your own Window
        manually and pushing the frames forward by yourself with the
        EventLoop.idle() in your own main loop while polling for the Window
        events both during the pause mode and active mode.

        .. versionadded:: 1.11.0
        '''

        from kivy.clock import Clock
        from kivy.base import EventLoop
        from kivy.app import runTouchApp, stopTouchApp
        from kivy.core.flow import FlowReturn, FlowBreak, FlowContinue
        from simpleapp import Simple

        # get OpenGL window
        import kivy.core.window
        kivy.core.window.Window = kivy.core.window.get_core_window()
        EventLoop.ensure_window()

        # get App instance and run it
        app = Simple()
        widget = app.build()
        runTouchApp(widget)

        # manage the event loop
        #
        # two while loops because of a Window main loop (polling one)
        # is being wrapped with an event loop (e.g. for EventDispatcher)
        current_frame = 0
        while current_frame < 60:
            while current_frame < 60:
                current_frame += 1
                EventLoop.idle()

                flow = EventLoop.window.slave_poll()
                flow_type = type(flow)
                if flow_type is FlowReturn:
                    return flow.return_value
                elif flow_type is FlowBreak:
                    break
                elif flow_type is FlowContinue:
                    continue

                # test in custom main loop too
                # note:
                #     generally you would want some hook function
                #     instead of just copy-pasting your test in here
                #
                # in case of premature errors / segfaults use pdb.set_trace()
                self.mainloop_widget_hook(
                    current_frame, Clock._max_fps,
                    widget, app
                )

        # destroy the window and stop eventloop
        EventLoop.window.close()
        stopTouchApp()


if __name__ == '__main__':
    unittest.main()
