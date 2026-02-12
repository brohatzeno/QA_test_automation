// -------------------- ABSTRACT BASE CLASS --------------------
class AbstractDoublePendulum {
  constructor(ctx, originX, originY, L1, L2, m1, m2, theta1, theta2, g = 9.8, dt = 0.03, label = '') {
    if (this.constructor === AbstractDoublePendulum) {
      throw new Error("Cannot instantiate abstract class!");
    }

    // Protected fields (accessible in subclasses)
    this._ctx = ctx;
    this._originX = originX;
    this._originY = originY;
    this._L1 = L1;
    this._L2 = L2;
    this._m1 = m1;
    this._m2 = m2;
    this._theta1 = theta1;
    this._theta2 = theta2;
    this._theta1_dot = 0;
    this._theta2_dot = 0;
    this._g = g;
    this._dt = dt;
    this._label = label;
  }

  // -------------------- FINAL ALGORITHM --------------------
  step() {
    this._updateMotion(); // core math logic (cannot be overridden externally)
    this.draw();          // shared draw logic
  }

  // -------------------- CORE MATH LOGIC --------------------
  _updateMotion() {
    const [theta1_ddot, theta2_ddot] = this.computeAccelerations();
    this._theta1_dot += theta1_ddot * this._dt;
    this._theta2_dot += theta2_ddot * this._dt;
    this._theta1 += this._theta1_dot * this._dt;
    this._theta2 += this._theta2_dot * this._dt;
  }

  // -------------------- HOOK: subclass overrides --------------------
  computeAccelerations() {
    throw new Error("computeAccelerations() must be implemented by subclass");
  }

  // -------------------- DRAW LOGIC --------------------
  draw() {
    const ctx = this._ctx;

    const x1 = this._originX + this._L1 * Math.sin(this._theta1);
    const y1 = this._originY + this._L1 * Math.cos(this._theta1);

    const x2 = x1 + this._L2 * Math.sin(this._theta2);
    const y2 = y1 + this._L2 * Math.cos(this._theta2);

    ctx.beginPath();
    ctx.moveTo(this._originX, this._originY);
    ctx.lineTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.strokeStyle = '#e6e6e6';
    ctx.lineWidth = 4;
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(x1, y1, this._m1, 0, 2 * Math.PI);
    ctx.fillStyle = '#ffffff';
    ctx.fill();

    ctx.beginPath();
    ctx.arc(x2, y2, this._m2, 0, 2 * Math.PI);
    ctx.fillStyle = '#ffffff';
    ctx.fill();

    if (this._label) {
      ctx.save();
      ctx.font = '16px sans-serif';
      ctx.fillStyle = '#e6e6e6';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'bottom';
      ctx.fillText(this._label, this._originX, this._originY - 12);
      ctx.restore();
    }
  }
}

// -------------------- SUBCLASS: STANDARD PENDULUM --------------------
class DoublePendulum extends AbstractDoublePendulum {
  computeAccelerations() {
    const delta = this._theta1 - this._theta2;
    const denom1 = this._L1 * (2 - Math.cos(2 * delta));
    const denom2 = this._L2 * (2 - Math.cos(2 * delta));

    const theta1_ddot = (
      - this._g * 2 * Math.sin(this._theta1)
      - Math.sin(this._theta1 - 2 * this._theta2)
      - 2 * Math.sin(delta) * (this._theta2_dot ** 2 * this._L2 + this._theta1_dot ** 2 * this._L1 * Math.cos(delta))
    ) / denom1;

    const theta2_ddot = (
      2 * Math.sin(delta) * (this._theta1_dot ** 2 * this._L1 * 2 + this._g * 2 * Math.cos(this._theta1) + this._theta2_dot ** 2 * this._L2 * Math.cos(delta))
    ) / denom2;

    return [theta1_ddot, theta2_ddot];
  }
}

// -------------------- SUBCLASS: DAMPED PENDULUM --------------------
class DampedPendulum extends DoublePendulum {
  computeAccelerations() {
    const [theta1_ddot, theta2_ddot] = super.computeAccelerations();
    const damping = 0.97; // safe tweak
    return [theta1_ddot * damping, theta2_ddot * damping];
  }
}

// -------------------- SETUP --------------------
const canvas = document.getElementById('pendulumCanvas');
const ctx = canvas.getContext('2d');
const originX = canvas.width / 2;
const originY = 200;

const pendulums = [
  new DoublePendulum(ctx, originX - 150, originY, 180, 180, 20, 20, Math.PI / 2, Math.PI / 2, 9.8, 0.03, 'Double Pendulum'),
  new DampedPendulum(ctx, originX + 150, originY, 180, 180, 20, 20, Math.PI / 2, Math.PI / 2, 9.8, 0.03, 'Damped Pendulum')
];

// -------------------- ANIMATION LOOP --------------------
function animateAll() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  pendulums.forEach(p => p.step());
  requestAnimationFrame(animateAll);
}

animateAll();
