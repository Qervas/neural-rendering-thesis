/**
 * Comparison Slider Module
 * Helper functions for img-comparison-slider (loaded via CDN)
 */

/**
 * Initialize all comparison sliders in the presentation
 */
export function initComparisonSliders() {
  // Wait for slides to load
  setTimeout(() => {
    const sliders = document.querySelectorAll('img-comparison-slider');

    sliders.forEach((slider, index) => {
      // Add labels if data attributes are present
      const leftLabel = slider.dataset.leftLabel;
      const rightLabel = slider.dataset.rightLabel;

      if (leftLabel || rightLabel) {
        wrapWithLabels(slider, leftLabel, rightLabel);
      }

      console.log(`Comparison slider ${index + 1} initialized`);
    });

    console.log(`Total comparison sliders: ${sliders.length}`);
  }, 500);
}

/**
 * Wrap slider with label elements
 */
function wrapWithLabels(slider, leftLabel, rightLabel) {
  const container = document.createElement('div');
  container.className = 'comparison-container';

  slider.parentNode.insertBefore(container, slider);
  container.appendChild(slider);

  if (leftLabel) {
    const left = document.createElement('span');
    left.className = 'comparison-label left';
    left.textContent = leftLabel;
    container.appendChild(left);
  }

  if (rightLabel) {
    const right = document.createElement('span');
    right.className = 'comparison-label right';
    right.textContent = rightLabel;
    container.appendChild(right);
  }
}
