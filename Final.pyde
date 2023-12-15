import random
import copy
from lists import *
from Button import *

objects = []  # List to store all objects
gravity = PVector(0, 0.5)  # Acceleration due to gravity
restitution = 0.8  # Coefficient of restitution for bouncing
repulsion_strength = 0.05  # Strength of the repulsion force
damping = 0.01  # Damping factor for velocity
friction = 0.1  # Friction coefficient for slowing down the objects
wall_thickness = 470 # Thickness of the walls
max_velocity = 5  # Maximum velocity of the circles

restart_screen = False  # Global variable to control restart screen

palette = TurkishPalette
mouse_mode = "Create"
time = 0

class Object:
    
    def __init__(self, x, y, radius, mass, color_):
        self.shape = None
        svg_index = random.randint(0, len(svg_options) - 1)
        svg_file = svg_options[svg_index]
        self.shape = loadImage(svg_file)
        self.position = PVector(x, y)
        self.velocity = PVector(0, 0)
        self.radius = radius
        self.bounding_circle_radius = radius  # Bounding circle radius
        self.mass = mass
        self.is_grabbed = False  # Indicates if the object is grabbed by the mouse
        self.offset = PVector(0, 0)  # Offset between object position and mouse cursor
        self.max_velocity = max_velocity
        self.tint_color = color_
        self.angle = random.uniform(0, TWO_PI)  # Randomly specify an angle
        self.time = -1
  
    def update(self):
        self.velocity.add(gravity)
        self.velocity.mult(1 - damping)  # Apply damping to gradually reduce velocity
        self.position.add(self.velocity)
        self.velocity.mult(1 - friction)  # Apply friction to gradually slow down the objects
        
        # Limit the velocity to the maximum velocity
        self.velocity.limit(self.max_velocity)
        
        # Limit the velocity
        if self.velocity.mag() > self.max_velocity:
            self.velocity.normalize().mult(self.max_velocity)

        # Check collision with ground
        if self.position.y + self.bounding_circle_radius >= ground_y :
            self.position.y = ground_y - self.bounding_circle_radius
            self.velocity.y *= -restitution
        
        if self.position.y + self.bounding_circle_radius <= ceiling_y:
            self.position.y = - self.bounding_circle_radius + 220
            self.velocity.y = 0

        # Check collision with walls
        if self.position.x - self.bounding_circle_radius <= wall_thickness + 35:
            self.position.x = self.bounding_circle_radius + wall_thickness + 35
            self.velocity.x *= -restitution
        elif self.position.x + self.bounding_circle_radius >= width - wall_thickness - 35:
            self.position.x = width - self.bounding_circle_radius - wall_thickness  - 35
            self.velocity.x *= -restitution
            
        
        # rotate it
        if self.velocity.x > 1 or self.velocity.y > 1:
            self.angle += random.uniform(-0.05, 0.05)


    def check_collision(self, other):
        distance = self.position.dist(other.position)
        if distance <= self.bounding_circle_radius + other.bounding_circle_radius:
            # Objects collided
            self.resolve_collision(other)

    def resolve_collision(self, other):
        total_radius = self.bounding_circle_radius + other.bounding_circle_radius
        overlap = total_radius - self.position.dist(other.position)
        overlap *= 0.5

        direction = PVector.sub(other.position, self.position).normalize()
        separation_vector = direction.copy().mult(overlap)

        self.position.sub(separation_vector)
        other.position.add(separation_vector)

        # Add randomness to the bounce direction
        angle = random.uniform(-PI / 4, PI / 4)  # Adjust the range of randomness as desired
        direction.rotate(angle)

        # Add randomness to the restitution coefficient
        restitution_coefficient = random.uniform(0.7, 0.9)  # Adjust the range of randomness as desired

        self.velocity = direction.mult(self.velocity.mag() * restitution_coefficient)
        other.velocity = direction.mult(other.velocity.mag() * restitution_coefficient)

    def apply_repulsion(self, other):
        direction = PVector.sub(self.position, other.position)
        distance = direction.mag()
        if distance < self.bounding_circle_radius + other.bounding_circle_radius:
            repulsion_force = direction.normalize().mult(repulsion_strength)
        else:
            repulsion_force = PVector(0, 0)  # Initialize with zero vector
        self.velocity.add(repulsion_force.div(self.mass))
        other.velocity.sub(repulsion_force.div(other.mass))

    def display(self):
        pushMatrix()
        pushStyle()

        
        if button_states[6] == True:
            strokeWeight(1)
            # Draw the bounding circle
            stroke(255, 0, 0)  # Red color
            noFill()
            ellipse(self.position.x, self.position.y, 2 * self.bounding_circle_radius, 2 * self.bounding_circle_radius)

        tint(self.tint_color)  # Apply tint color to the image

        # Calculate the desired dimensions based on a constant resizing rate
        resize_factor = 0.1  # Adjust the resize factor as desired
        resized_width = self.shape.width * resize_factor
        resized_height = self.shape.height * resize_factor
        
        
        
        translate(self.position.x, self.position.y)  # Translate to the object's position
        rotate(self.angle)  # Rotate the image by the specified angle
        image(self.shape, -resized_width / 2, -resized_height / 2, resized_width, resized_height)  # Draw the image

        popStyle()
        popMatrix()

    def delete(self):
        # Delete the object
        self.disappearing_image = loadImage("human 1_1.png")  # Load the disappearing image
        self.deletion_start_time = millis()  # Start the deletion timer

    def is_deletion_complete(self):
        # Check if the deletion duration has passed
        return millis() - self.deletion_start_time >= 1000  # Change the duration as desired


def setup():
    fullScreen(P2D)
    global img, sign_img, dog_img, dog_img2
    global ground_y, height_constant, height_constant2, ceiling_y
    height_constant = 150
    height_constant2 = 220
    ground_y = height - height_constant
    ceiling_y = height_constant2
    restart_screen = False
    img = loadImage("frame.jpg")
    sign_img = loadImage("Keith Haring sign.png")
    dog_img = loadImage("Dog2 bark.png")
    dog_img2 = loadImage("Dog2 bark_1.png")
    
def draw():
    global time
    background(100)
    image(img, 0, 0, width, height)
    image(sign_img, 1490, 910, width/15, height/15)
    image(dog_img, 1490, 300, width/10, height/10)
    image(dog_img2, 230, 750, width/10, height/10)

    # Update and display all objects
    for obj in objects:
        obj.update()
        obj.display()
    
    # Check collision and apply repulsion between objects
    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            objects[i].check_collision(objects[j])
            objects[i].apply_repulsion(objects[j])
            
    button_draw(width)

    for obj in objects:
        if obj.time > 0:
            obj.time -=1
            print(obj.time)
        if obj.time == 0:
            objects.remove(obj)
            
    if time > 0:
        time -= 1
    if time == 0:
        button_states[4] = False
        button_states[5] = False
        button_states[8] = False


def restart_game():
    global objects, restart_screen
    objects = []
    restart_screen = False
        
def mouseDragged():
    if not restart_screen:
        # Update the position of the grabbed object based on the mouse cursor
        for obj in objects:
            if obj.is_grabbed:
                obj.position.x = mouseX + obj.offset.x
                obj.position.y = mouseY + obj.offset.y
                                        
def mouseReleased():
    if not restart_screen:
        # Release the grabbed object when the left mouse button is released
        for obj in objects:
            obj.is_grabbed = False
            
def mousePressed():
    global mouse_mode
    click = True
    button_spacing = (width - button_size * button_count) / (button_count + 1)
    for i in range(button_count):
        button_x = button_spacing * (i + 1) + button_size * i
        if button_x < mouseX < button_x + button_size and button_y < mouseY < button_y + button_size:
            if i == 4:
                pp = int(len(objects) / 5)
                deletes(pp)
                time = 70
            elif i == 5:
                deletes(len(objects))
            elif i == 8:
                changes()
            elif i == 0 or 1 or 2 or 3 or 7:
                mouse_mode = button_names[i]
                button_states[0] = False
                button_states[1] = False
                button_states[2] = False
                button_states[3] = False
                button_states[7] = False
            button_states[i] = not button_states[i]  # Toggle button state
            print(button_states)
            print(mouse_mode)
            click = False
           
                
    if click == True:
        if mouse_mode == "Create":
            create()
        elif mouse_mode == "Create Bulk":
            for r in range(5):
                create()
        elif mouse_mode == "Grabbing":
            grab()
        elif mouse_mode == "Delete":
            delete()
        elif mouse_mode == "Change \nColor":
            change()
            
                    
def create():
    if len(objects) <= 300:
        # Add a new ball at the mouse position
        radius = 45  # Randomize the radius as desired
        mass = radius * 0.9  # Adjust the mass based on the radius
        obj = Object(mouseX, mouseY, radius, mass, random.choice(palette)) 
        objects.append(obj)
        
def grab():
    # Check if the mouse is inside any existing object
    for obj in objects:
        distance = dist(mouseX, mouseY, obj.position.x, obj.position.y)
        if distance <= obj.radius:
            # Grab the object and track the mouse cursor
            obj.is_grabbed = True
            obj.offset = PVector(obj.position.x - mouseX, obj.position.y - mouseY)
            
def delete():
    # Delete object at mouseX, mouseY
    for obj in objects:
        if dist(obj.position.x, obj.position.y, mouseX, mouseY) <= obj.radius:
            objects.remove(obj)
            
def deletes(pp):
    if len(objects) >= 25:
        to_remove = random.sample(objects, pp)  # Randomly select 6 objects to remove
        for obj in to_remove:
            objects.remove(obj)
    elif pp != 0:
        to_remove = random.sample(objects, pp*3)
        for obj in to_remove:
            objects.remove(obj)
    else:
        for obj in objects:
            objects.remove(obj)
    
        
def change():
    for obj in objects:
        if dist(obj.position.x, obj.position.y, mouseX, mouseY) <= obj.radius:
            obj.tint_color = random.choice(palette)
            
def changes():
    palette = random.choice(palettes)
    for obj in objects:
        obj.tint_color = random.choice(palette)
