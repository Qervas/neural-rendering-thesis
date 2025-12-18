/**
 * Diagram Animator Module
 * Step-by-step SVG diagram animations with GSAP
 */

import gsap from 'gsap';

// Store diagram instances
const diagrams = new Map();

/**
 * Initialize diagram animations
 */
export function initDiagramAnimator() {
  // Find all diagram containers
  const containers = document.querySelectorAll('.diagram-container');

  containers.forEach((container, index) => {
    const diagramId = container.id || `diagram-${index}`;
    const animator = new DiagramAnimator(container, diagramId);
    diagrams.set(diagramId, animator);

    console.log(`Diagram animator initialized: ${diagramId}`);
  });

  // Expose global access
  window.diagramAnimator = {
    get: (id) => diagrams.get(id),
    playStep: (id, step) => diagrams.get(id)?.playStep(step),
    reset: (id) => diagrams.get(id)?.reset()
  };
}

/**
 * DiagramAnimator class for individual diagrams
 */
class DiagramAnimator {
  constructor(container, id) {
    this.container = container;
    this.id = id;
    this.steps = [];
    this.currentStep = -1;
    this.timeline = null;

    this.init();
  }

  init() {
    // Find all elements with step data attributes
    const stepElements = this.container.querySelectorAll('[data-step]');

    // Group elements by step number
    const stepGroups = new Map();
    stepElements.forEach(el => {
      const stepNum = parseInt(el.dataset.step);
      if (!stepGroups.has(stepNum)) {
        stepGroups.set(stepNum, []);
      }
      stepGroups.get(stepNum).push(el);

      // Initially hide
      gsap.set(el, { opacity: 0, y: 20 });
    });

    // Sort steps
    this.steps = Array.from(stepGroups.entries())
      .sort((a, b) => a[0] - b[0])
      .map(([stepNum, elements]) => ({ stepNum, elements }));

    // Create master timeline
    this.createTimeline();
  }

  createTimeline() {
    this.timeline = gsap.timeline({ paused: true });

    this.steps.forEach((step, index) => {
      const label = `step${step.stepNum}`;

      this.timeline.addLabel(label);
      this.timeline.to(step.elements, {
        opacity: 1,
        y: 0,
        duration: 0.5,
        stagger: 0.1,
        ease: 'power2.out'
      }, label);
    });
  }

  /**
   * Play animation to a specific step
   */
  playStep(stepIndex) {
    if (stepIndex < 0 || stepIndex >= this.steps.length) return;

    const step = this.steps[stepIndex];
    this.timeline.seek(`step${step.stepNum}`);
    this.timeline.play();
    this.currentStep = stepIndex;

    // Add highlight effect
    this.highlightStep(stepIndex);
  }

  /**
   * Play all steps sequentially
   */
  playAll(delay = 0) {
    this.timeline.delay(delay).play(0);
  }

  /**
   * Reset to initial state
   */
  reset() {
    this.timeline.pause(0);
    this.currentStep = -1;
    this.clearHighlights();
  }

  /**
   * Go to next step
   */
  next() {
    if (this.currentStep < this.steps.length - 1) {
      this.playStep(this.currentStep + 1);
    }
  }

  /**
   * Go to previous step
   */
  prev() {
    if (this.currentStep > 0) {
      this.playStep(this.currentStep - 1);
    }
  }

  /**
   * Highlight current step elements
   */
  highlightStep(stepIndex) {
    this.clearHighlights();

    const step = this.steps[stepIndex];
    step.elements.forEach(el => {
      el.classList.add('step-highlight');
    });
  }

  clearHighlights() {
    this.container.querySelectorAll('.step-highlight')
      .forEach(el => el.classList.remove('step-highlight'));
  }
}

/**
 * Animate pipeline arrows (draw effect)
 */
export function animatePipelineArrows(container, duration = 0.8) {
  const arrows = container.querySelectorAll('.pipeline-arrow');

  gsap.fromTo(arrows,
    { strokeDashoffset: 100 },
    {
      strokeDashoffset: 0,
      duration,
      stagger: 0.2,
      ease: 'power2.inOut'
    }
  );
}

/**
 * Create a typing effect for text elements
 */
export function typeText(element, text, speed = 50) {
  return new Promise(resolve => {
    let index = 0;
    element.textContent = '';

    function type() {
      if (index < text.length) {
        element.textContent += text.charAt(index);
        index++;
        setTimeout(type, speed);
      } else {
        resolve();
      }
    }

    type();
  });
}

/**
 * Animate number counting
 */
export function animateNumber(element, endValue, duration = 1000, prefix = '', suffix = '') {
  const startValue = 0;
  const startTime = performance.now();

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);

    // Ease out
    const eased = 1 - Math.pow(1 - progress, 3);
    const currentValue = Math.round(startValue + (endValue - startValue) * eased);

    element.textContent = `${prefix}${currentValue.toLocaleString()}${suffix}`;

    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }

  requestAnimationFrame(update);
}

/**
 * Stagger fade-in animation for list items
 */
export function staggerFadeIn(elements, options = {}) {
  const { duration = 0.5, stagger = 0.1, y = 30 } = options;

  gsap.fromTo(elements,
    { opacity: 0, y },
    {
      opacity: 1,
      y: 0,
      duration,
      stagger,
      ease: 'power2.out'
    }
  );
}

// Export utilities
export { DiagramAnimator };
