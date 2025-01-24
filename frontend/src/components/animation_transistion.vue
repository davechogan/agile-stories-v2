<template>
  <div class="animation-container">
    <!-- Brain with Gears -->
    <div class="brain">
      <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <!-- Main Brain Shape -->
        <path class="brain-path" d="M50 10 C20 10 10 30 10 50 C10 70 20 90 50 90 C80 90 90 70 90 50 C90 30 80 10 50 10" />
        
        <!-- Rotating Gears -->
        <g class="gear gear-1">
          <circle cx="35" cy="40" r="12" class="gear-body"/>
          <path d="M35 28 L37 25 L33 25 Z M35 52 L37 55 L33 55 Z M23 40 L20 42 L20 38 Z M47 40 L50 42 L50 38 Z" class="gear-teeth"/>
        </g>
        
        <g class="gear gear-2">
          <circle cx="65" cy="40" r="10" class="gear-body"/>
          <path d="M65 30 L67 27 L63 27 Z M65 50 L67 53 L63 53 Z M55 40 L52 42 L52 38 Z M75 40 L78 42 L78 38 Z" class="gear-teeth"/>
        </g>
        
        <g class="gear gear-3">
          <circle cx="50" cy="65" r="15" class="gear-body"/>
          <path d="M50 50 L52 47 L48 47 Z M50 80 L52 83 L48 83 Z M35 65 L32 67 L32 63 Z M65 65 L68 67 L68 63 Z" class="gear-teeth"/>
        </g>
      </svg>
    </div>

    <!-- Dynamic Sticky Notes -->
    <div v-for="(note, index) in notes" 
         :key="note.id" 
         class="sticky-note"
         :style="{
           transform: `translate(${note.x}px, ${note.y}px) rotate(${note.rotation}deg)`,
           ...getNoteColor(index)
         }">
      <div class="note-content">
        <div class="note-text">{{ note.text }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.animation-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.8);
}

.brain {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: min(35vw, 350px);
  height: min(35vw, 350px);
}

/* Brain and Gear Styles */
.brain-path {
  fill: #2c3e50;
  stroke: #34495e;
  stroke-width: 2;
}

.gear {
  transform-origin: center;
}

.gear-body {
  fill: #95a5a6;
  stroke: #7f8c8d;
  stroke-width: 1;
}

.gear-teeth {
  fill: #95a5a6;
}

.gear-1 {
  animation: rotate 8s linear infinite;
}

.gear-2 {
  animation: rotate-reverse 6s linear infinite;
}

.gear-3 {
  animation: rotate 10s linear infinite;
}

/* Sticky Note Styles */
.sticky-note {
  position: absolute;
  width: min(18vw, 160px);
  height: min(18vw, 140px);
  transition: transform 0.1s linear;
}

.note-content {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  box-shadow: 3px 3px 10px rgba(0,0,0,0.2),
              -1px -1px 4px rgba(0,0,0,0.1);
  border-radius: 4px;
  padding: 15px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: clamp(14px, 1.8vw, 20px);
  color: #2c3e50;
}

.note-text {
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes rotate-reverse {
  from { transform: rotate(360deg); }
  to { transform: rotate(0deg); }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .animation-container {
    width: 95vw;
    height: 95vw;
  }

  .brain {
    width: 50vw;
    height: 50vw;
  }

  .sticky-note {
    width: 30vw;
    height: 25vw;
  }
}
</style>

<script>
export default {
  props: {
    stickyNotes: {
      type: Array,
      default: () => [
        "User Stories",
        "Acceptance Criteria",
        "Technical Tasks",
        "Estimations",
        "Implementation"
      ],
    }
  },
  data() {
    return {
      notes: [], // Will hold note positions and velocities
      animationFrame: null
    }
  },
  mounted() {
    const margin = 160;
    const width = window.innerWidth - margin * 2;
    const height = window.innerHeight - margin * 2;
    const halfWidth = width / 2;
    const halfHeight = height / 2;

    // Helper function to get random velocity away from center
    const getVelocityForQuadrant = (quadrant) => {
      const speed = 4;
      let angle;
      switch(quadrant) {
        case 0: // Top-left: move down-right
          angle = Math.PI * (Math.random() * 0.5 - 0.75);
          break;
        case 1: // Top-right: move down-left
          angle = Math.PI * (Math.random() * 0.5 + 0.25);
          break;
        case 2: // Bottom-left: move up-right
          angle = Math.PI * (Math.random() * 0.5 - 1.25);
          break;
        case 3: // Bottom-right: move up-left
          angle = Math.PI * (Math.random() * 0.5 - 0.25);
          break;
      }
      return {
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed
      };
    };

    this.notes = this.stickyNotes.map((text, index) => {
      const quadrant = index % 4;
      let x, y, velocities;

      // Position notes in corners
      switch(quadrant) {
        case 0: // Top-left
          x = margin + Math.random() * halfWidth * 0.8;
          y = margin + Math.random() * halfHeight * 0.8;
          break;
        case 1: // Top-right
          x = halfWidth + margin + Math.random() * halfWidth * 0.8;
          y = margin + Math.random() * halfHeight * 0.8;
          break;
        case 2: // Bottom-left
          x = margin + Math.random() * halfWidth * 0.8;
          y = halfHeight + margin + Math.random() * halfHeight * 0.8;
          break;
        case 3: // Bottom-right
          x = halfWidth + margin + Math.random() * halfWidth * 0.8;
          y = halfHeight + margin + Math.random() * halfHeight * 0.8;
          break;
      }

      velocities = getVelocityForQuadrant(quadrant);

      return {
        id: index,
        text,
        x,
        y,
        vx: velocities.vx,
        vy: velocities.vy,
        rotation: Math.random() * 360,
        rotationSpeed: (Math.random() - 0.5) * 0.3
      };
    });

    this.startAnimation();
  },
  beforeUnmount() {
    if (this.animationFrame) {
      cancelAnimationFrame(this.animationFrame);
    }
  },
  methods: {
    startAnimation() {
      const animate = () => {
        this.updateNotes();
        this.animationFrame = requestAnimationFrame(animate);
      };
      animate();
    },
    updateNotes() {
      const margin = 160;
      const containerWidth = window.innerWidth - margin;
      const containerHeight = window.innerHeight - margin;

      this.notes.forEach((note, i) => {
        // Keep constant speed
        const speed = Math.sqrt(note.vx * note.vx + note.vy * note.vy);
        const targetSpeed = 4;
        if (speed < targetSpeed * 0.8) {
          note.vx *= 1.1;
          note.vy *= 1.1;
        }

        // Update position
        note.x += note.vx;
        note.y += note.vy;
        note.rotation += note.rotationSpeed;

        // Only bounce off screen edges
        if (note.x < margin || note.x > containerWidth - margin) {
          note.vx *= -1;
          note.x = note.x < margin ? margin : containerWidth - margin;
          note.vy += (Math.random() - 0.5) * 2;
        }
        if (note.y < margin || note.y > containerHeight - margin) {
          note.vy *= -1;
          note.y = note.y < margin ? margin : containerHeight - margin;
          note.vx += (Math.random() - 0.5) * 2;
        }

        // Only check collisions with other notes, ignore brain
        for (let j = i + 1; j < this.notes.length; j++) {
          const other = this.notes[j];
          const dx = other.x - note.x;
          const dy = other.y - note.y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          const minDistance = margin * 0.9;

          if (distance < minDistance) {
            const angle = Math.atan2(dy, dx);
            const force = (minDistance - distance) / minDistance;
            
            const repulsionX = Math.cos(angle) * force * 2;
            const repulsionY = Math.sin(angle) * force * 2;
            
            note.vx -= repulsionX;
            note.vy -= repulsionY;
            other.vx += repulsionX;
            other.vy += repulsionY;

            const newSpeed1 = Math.sqrt(note.vx * note.vx + note.vy * note.vy);
            const newSpeed2 = Math.sqrt(other.vx * other.vx + other.vy * other.vy);
            
            note.vx = (note.vx / newSpeed1) * targetSpeed;
            note.vy = (note.vy / newSpeed1) * targetSpeed;
            other.vx = (other.vx / newSpeed2) * targetSpeed;
            other.vy = (other.vy / newSpeed2) * targetSpeed;
          }
        }

        // Maintain minimum speed
        const currentSpeed = Math.sqrt(note.vx * note.vx + note.vy * note.vy);
        if (currentSpeed < 2) {
          const angle = Math.random() * Math.PI * 2;
          note.vx = Math.cos(angle) * targetSpeed;
          note.vy = Math.sin(angle) * targetSpeed;
        }
      });
    },
    getNoteColor(index) {
      const colors = [
        { bg: '#fff7c0', shadow: '#e6d28a' }, // Yellow
        { bg: '#c0f0c0', shadow: '#8ad28a' }, // Green
        { bg: '#c0e0ff', shadow: '#8ab2d2' }, // Blue
        { bg: '#ffc0db', shadow: '#d28aa6' }, // Pink
        { bg: '#ffd7b0', shadow: '#d2a88a' }  // Orange
      ];
      const color = colors[index % colors.length];
      return {
        background: `linear-gradient(135deg, ${color.bg} 0%, ${color.shadow} 100%)`
      };
    }
  }
};
</script>
