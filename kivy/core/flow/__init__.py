'''
Kivy main loop flow
===================

To direct Kivy main loop flow we use Python keywords such as ``return``,
 ``continue`` or ``break``. In `slave` mode however you either copy
verbosely the entire Window main loop or the EventLoop main loop which
is almost only another ``while True`` wrapper or you call only specific parts.

While doing the former, i.e. copying verbosely, you will be in constant
struggle to maintain 1-to-1 consistency with the Kivy main loop and hope
something doesn't change between the releases.

With these classes we can control the flow with a small overhead and give you
an API to manually trigger a non-blocking Kivy main loop (i.e. without
``while True`` on our side) constructs by keeping the Python keywords under
control via various returned objects as a mark for the futrher action within
the first level of our ``while True`` loop, therefore keeping the polling
or other behaviors linear and completely non-related to the loop manipulation
via ``return``, ``continue``, ``break``, etc.

You can do a main loop in your app like this::

    # trigger the slave mode for the framework
    # !!! has to be done before importing anything from Kivy
    from os import environ
    environ['KIVY_SLAVE_MODE'] = '1'
    from kivy.core.flow import FlowReturn, FlowBreak

    # make sure OpenGL window is available
    EventLoop.ensure_window()
    window = EventLoop.window


    def my_main_loop():
        # your custom main loop
        while True:
            flow = window.slave_poll()
            if isinstance(flow, FlowReturn):
                return flow.return_value
            elif isinstance(flow, FlowBreak):
                break
            ...


    if __name__ == '__main__':
        my_main_loop()

.. versionadded:: 1.11.0
'''


class FlowBase(object):
    pass


class FlowReturn(FlowBase):
    def __init__(self, value):
        self._return_value = value

    @property
    def return_value(self):
        return self._return_value


class FlowBreak(FlowBase):
    pass


class FlowContinue(FlowBase):
    pass
