'''
Simple Application with Clock to showcase slave mode, getting to the next
frame and Clock ticking/scheduling.

.. versionadded:: 1.11.0
'''

from kivy.app import App
from kivy.uix.button import Button
from kivy.clock import Clock


class Simple(App):
    '''
    Main application class.

    .. versionadded:: 1.11.0
    '''

    TEXT_DEFAULT = 'default'
    TEXT_CHANGED = 'changed'
    INTERVAL = 0.5

    @staticmethod
    def change_text(widget):
        '''
        Change the text attribute of a widget.

        .. versionadded:: 1.11.0
        '''
        widget.text = Simple.TEXT_CHANGED

    def build(self):
        '''
        Kivy build method.

        .. versionadded:: 1.11.0
        '''

        widget = Button(text=Simple.TEXT_DEFAULT)
        Clock.schedule_once(
            lambda dt: self.change_text(widget),
            Simple.INTERVAL
        )
        return widget


if __name__ == '__main__':
    Simple().run()
