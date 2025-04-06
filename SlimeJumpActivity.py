import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import pygame

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton
from sugar3.graphics.toolbutton import ToolButton

import sugargame.canvas
import slimejump

class SlimeJumpActivity(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        
        # Create the game instance
        self.game = slimejump.SlimeJumpGame()
        
        # Build the activity toolbar
        self.build_toolbar()
        
        # Create the game canvas
        self._canvas = sugargame.canvas.PygameCanvas(self, main=self.game.run)

        # Set the canvas as the activity's canvas
        self.set_canvas(self._canvas)
        
        # These lines are crucial for keyboard input
        self._canvas.set_can_focus(True)
        self._canvas.grab_focus()
        
        # Connect key press events at the Gtk level
        self.connect('key-press-event', self._key_press_cb)
        self.connect('key-release-event', self._key_release_cb)
        self.show_all()

    #----------------
    def _key_press_cb(self, widget, event):
        # Forward the key press to the game
        if hasattr(self.game, 'key_press'):
            self.game.key_press(event.keyval)
        return False  # Allow event propagation
    
    def _key_release_cb(self, widget, event):
        # Forward the key release to the game
        if hasattr(self.game, 'key_release'):
            self.game.key_release(event.keyval)
        return False  # Allow event propagation
    #-------------------
    
    def build_toolbar(self):
        toolbar_box = ToolbarBox()
        
        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        
        # Add a restart button
        restart_button = ToolButton('view-refresh')
        restart_button.set_tooltip('Restart Game')
        restart_button.connect('clicked', self._restart_game)
        toolbar_box.toolbar.insert(restart_button, -1)
        
        # Add the standard stop button
        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show_all()
    
    def _restart_game(self, widget):
        self.game.restart()
