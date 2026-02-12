# Building a Double Pendulum Simulation in JavaScript – Learning Report

## 1. Introduction
In this project, I built a double pendulum simulation using JavaScript and the HTML canvas.

A double pendulum is one pendulum attached to the end of another. Instead of simple back-and-forth motion, it moves in a complex and unpredictable way.

I found it exciting because:
- It combines physics and programming.
- It shows chaotic motion — tiny changes in starting position lead to very different outcomes.
- It looks visually compelling while being mathematically deep.

This project helped me understand not just animation, but also how real physical systems can be simulated with code. I also learned how to structure the simulation using clean object-oriented design. The demo runs two pendulums side-by-side (a standard one and a damped one) so you can compare their behavior directly.

## 2. Understanding the Physics (Beginner Friendly)
I avoided heavy formulas and focused on what the concepts mean.

### Angles (θ₁ and θ₂)
- θ₁ is the angle of the first rod.
- θ₂ is the angle of the second rod.
- These angles describe where each rod points.
Instead of tracking x and y positions directly, I learned we track angles and compute positions from them.

### Angular Velocity
- This is how fast the angle changes.
- Faster swings mean higher angular velocity.
Think of it like:
- Angle = position
- Angular velocity = speed of rotation

### Angular Acceleration
- This is how fast the angular velocity changes.
- Gravity pulls the pendulum down, causing it to speed up or slow down.

### Role of Gravity
Gravity is the main force pulling the pendulum downward. Without it, the pendulum would not swing.

### Why the System Becomes Chaotic
The second pendulum depends on the first, and both affect each other at the same time.
That creates:
- Extreme sensitivity
- Tiny starting differences → huge differences later
It’s like balancing two rulers on each other — very unstable and unpredictable.

## 3. Core Equations in Practice
Instead of focusing on formulas, I focused on what happens each frame.

Each animation step:
1. Calculate how gravity and motion affect each pendulum (angular acceleration).
2. Update angular velocities.
3. Update angles (new positions).

### Why small time steps (dt) matter
We update the system in very tiny slices of time.
- Smaller steps = smoother motion and more accuracy
- Larger steps = unrealistic or unstable motion
So dt is a balance between realism and performance.

## 4. Translating Physics into JavaScript

### Variables
I used variables to represent:
- Angles
- Angular velocities
- Gravity
- Rod lengths
- Masses

In this version, the mass values are used to size the bob circles in the drawing rather than in the physics equations. The acceleration formulas are a simplified equal-mass version, so `_m1` and `_m2` are not part of the math yet.

### Acceleration Function
A function calculates angular acceleration based on:
- Current angles
- Current speeds
- Gravity
- Rod lengths

### Update Loop
Each frame:
```
velocity += acceleration * dt
angle += velocity * dt
```

### Drawing on Canvas
Using `Math.sin()` and `Math.cos()`:
- Convert angles → x/y positions
- Draw rods (lines)
- Draw masses (circles)
- Draw a label above each top pivot so you can identify each pendulum

### requestAnimationFrame
This tells the browser:
“Render this again before the next screen refresh.”
It creates a smooth loop at roughly 60 frames per second.

## 5. Moving from Functional Code to OOP
At first, everything was:
- Global variables
- Standalone functions

It worked, but became messy as the project grew.
I realized that all the data and behavior belong to one thing: a pendulum.
So I moved to object-oriented design, and even set up an abstract base class to enforce structure.

## 6. OOP Concepts I Learned

### Classes and Objects
I created a class to represent a pendulum.
Each instance has its own:
- Angles
- Velocities
- Position
- Behavior
This lets me run multiple pendulums at once.

### Encapsulation
Physics variables stay inside the class.
Outside code is discouraged from changing angles or velocities directly, which helps prevent accidental bugs. By convention, outside code should avoid these fields even though JavaScript does not technically prevent access.
I used underscore-prefixed fields (like `_theta1`, `_ctx`) as a convention to mark internal or protected data — it’s a naming convention, not enforced privacy.

### Abstraction
I created an abstract base class called `AbstractDoublePendulum`. It cannot be instantiated directly because the constructor checks `this.constructor` and throws an error if you try. This keeps the core structure consistent while allowing subclasses to implement specific physics.

### Inheritance
The inheritance chain is:
- `AbstractDoublePendulum` → `DoublePendulum` → `DampedPendulum`

The base class holds shared behavior, the standard pendulum implements the real physics, and the damped pendulum extends that to reduce energy over time. In the damped version, I call `super.computeAccelerations()` first, then apply a damping factor (0.97) so the acceleration is reduced by about 3% each frame to simulate energy loss.

### Polymorphism
Both pendulums share the same method names (`step()`, `draw()`), but they behave differently internally.
So the animation loop can treat them the same:
```
pendulums.forEach(p => p.step());
```

### Template Method and Hook Method
The `step()` method acts like a Template Method: it defines the fixed flow of the algorithm (update motion, then draw). I treat `step()` as a final method by design, not by language enforcement, since JavaScript does not have true `final` methods. In the abstract base class, `computeAccelerations()` is intentionally unimplemented as a hook method, which forces subclasses to supply the physics details.

## 7. How OOP Helped
OOP made the project:
- Easier to manage
- Easier to extend
- Closer to how we naturally model real systems

The abstract base class sets the rules, and subclasses fill in the details. This makes the code structure match the concept:
“A pendulum is an object with properties and behavior.”

## 8. Challenges I Faced
Real struggles I had:
- Understanding angular motion vs x/y motion
- Remembering JavaScript uses radians, not degrees
- Tuning `dt` for realistic speed
- Keeping the pendulum centered on screen
- Debugging chaotic behavior (hard to tell if it’s a bug or real chaos)
- Realizing OOP changes structure, not the physics itself
- Understanding that JavaScript does not enforce `final` or `protected` like some other OOP languages — those are design choices and conventions here

## 9. Key Takeaways
I learned:
- How physics can be simulated step by step over time
- How browser animation works
- How small time updates create continuous motion
- How to think in objects instead of just functions
- That OOP is about organizing logic, not changing how JavaScript runs
- That design patterns like Template Method and hook methods can make code more reusable and safe

## 10. Future Improvements
If I continue this project, I would like to:
- Add motion trails to show chaotic paths
- Turn the pendulum into a reusable module
- Add UI sliders for gravity, mass, and length
- Create more pendulum types using inheritance
