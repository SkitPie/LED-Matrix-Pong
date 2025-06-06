"""Minimal 2D game engine for the LED matrix display."""

import spidev  # Imported for completeness; initialized in :mod:`led_display`
import time
import threading

from led_display import set_pixel, clear_display, init_display, update_display

class GameObject:
    """A simple rectangular entity managed by :class:`GameEngine`."""

    def __init__(self, x, y, width, height, vx=0, vy=0, trigger=None):
        """Initialize the object with position, size and velocity."""

        self.x = x

        self.y = y

        self.width = width

        self.height = height

        self.vx = vx

        self.vy = vy

        self.is_static = False

        self.is_trigger = False

        self.trigger = trigger

    def move(self, dx, dy):
        """Translate the object by ``dx`` and ``dy`` if not static."""

        if not self.is_static:
            self.x += dx
            self.y += dy

    def setPos(self, posx, posy):
        """Place the object at ``(posx, posy)``."""
        self.x = posx
        self.y = posy

    def set_velocity(self, vx, vy):
        """Assign a new velocity if the object is movable."""

        if not self.is_static:
            self.vx = vx
            self.vy = vy

    def update(self):
        """Advance the object's position by its velocity."""

        if not self.is_static:
            self.x += self.vx
            self.y += self.vy

    def get_rect(self):
        """Return the bounding rectangle of the object."""
        return (self.x, self.y, self.width, self.height)

    def collides_with(self, other):
        """Determine whether this object intersects ``other``."""

        return (
            self.x < other.x + other.width
            and self.x + self.width > other.x
            and self.y < other.y + other.height
            and self.y + self.height > other.y
        )

class GameEngine:
    """Engine managing game objects and rendering on the LED matrix."""

    def __init__(self, width=32, height=8):
        """Create a new engine with the given display size."""

        self.width = width
        self.height = height

        self.objects = []
        self.running = False

        self.game_thread = None
        self.render_thread = None

        self.objects_lock = threading.Lock()

        init_display()  # LED-Matrix initialisieren

    def add_object(self, obj):
        """Register a :class:`GameObject` with the engine."""

        with self.objects_lock:
            self.objects.append(obj)

    def remove_object(self, obj):
        """Remove an object from the engine if present."""

        with self.objects_lock:
            if obj in self.objects:
                self.objects.remove(obj)

    def handle_collisions(self):
        """Handle wall and object collisions for all objects."""

        with self.objects_lock:

            # Wandkollisionen

            for obj in self.objects:

                if obj.is_static:

                    continue

                if obj.x < 0:

                    obj.x = 0

                    obj.vx = -obj.vx

                elif obj.x + obj.width > self.width:

                    obj.x = self.width - obj.width

                    obj.vx = -obj.vx

                if obj.y < 0:

                    obj.y = 0

                    obj.vy = -obj.vy

                elif obj.y + obj.height > self.height:

                    obj.y = self.height - obj.height

                    obj.vy = -obj.vy

            # Objektkollisionen

            for i in range(len(self.objects)):

                for j in range(i + 1, len(self.objects)):

                    obj1 = self.objects[i]

                    obj2 = self.objects[j]

                    if obj1.collides_with(obj2):

                        self.handle_object_collision(obj1, obj2)
                        self.handle_trigger(obj1, obj2)
                        

    def handle_object_collision(self, obj1, obj2):
        """Resolve a collision between two objects."""

        # Statisches vs Bewegliches Objekt

        if obj1.is_static and not obj2.is_static:

            # Horizontale Kollision (von der Seite)

            if abs(obj2.x - obj1.x) < obj1.width or abs(obj2.x - (obj1.x + obj1.width)) < obj1.width:

                obj2.vx = -obj2.vx

            # Vertikale Kollision (von oben/unten)

            else:

                obj2.vy = -obj2.vy

        elif obj2.is_static and not obj1.is_static:

            if abs(obj1.x - obj2.x) < obj2.width or abs(obj1.x - (obj2.x + obj2.width)) < obj2.width:

                obj1.vx = -obj1.vx

            else:

                obj1.vy = -obj1.vy

        # Zwei bewegliche Objekte

        elif not obj1.is_static and not obj2.is_static:

            obj1.vx, obj2.vx = obj2.vx, obj1.vx

            obj1.vy, obj2.vy = obj2.vy, obj1.vy

    def handle_trigger(self, obj1, obj2):
        """Invoke trigger callbacks when trigger objects are hit."""
        if obj1.is_trigger and obj1.trigger is not None:
            obj1.trigger(obj1)
        if obj2.is_trigger and obj2.trigger is not None:
            obj2.trigger(obj2)

    def update_game(self):
        """Update all objects and resolve collisions."""

        with self.objects_lock:

            for obj in self.objects:

                obj.update()

        self.handle_collisions()

    def render_frame(self):
        """Draw the current scene to the LED matrix."""

        clear_display()  # Display löschen

        with self.objects_lock:

            for obj in self.objects:

                x, y, w, h = obj.get_rect()

                for i in range(int(y), int(y + h)):

                    for j in range(int(x), int(x + w)):

                        if 0 <= j < self.width and 0 <= i < self.height:

                            set_pixel(j, i, True)  # Pixel aktivieren

        update_display()  # Änderungen auf Matrix anzeigen

    def game_loop(self):
        """Continuously update game logic at ~30 FPS."""

        while self.running:

            start_time = time.time()

            self.update_game()

            elapsed = time.time() - start_time

            time.sleep(max(0, 0.033 - elapsed))  # 30 FPS

    def render_loop(self):
        """Continuously render frames at ~30 FPS."""

        while self.running:

            start_time = time.time()

            self.render_frame()

            elapsed = time.time() - start_time

            time.sleep(max(0, 0.033 - elapsed))  # 30 FPS

    def start(self):
        """Start the update and render threads."""

        self.running = True

        self.game_thread = threading.Thread(target=self.game_loop)

        self.render_thread = threading.Thread(target=self.render_loop)

        self.game_thread.start()

        self.render_thread.start()

    def stop(self):
        """Stop the engine and wait for threads to finish."""

        self.running = False

        self.game_thread.join()

        self.render_thread.join()
