/**
 * Main Reveal.js Configuration for Thesis Presentation
 * Neural Rendering Dataset Collection - Master's Thesis Defense
 */

import Reveal from '/presentation/node_modules/reveal.js/dist/reveal.esm.js';
import Markdown from '/presentation/node_modules/reveal.js/plugin/markdown/markdown.esm.js';
import Notes from '/presentation/node_modules/reveal.js/plugin/notes/notes.esm.js';
import Highlight from '/presentation/node_modules/reveal.js/plugin/highlight/highlight.esm.js';
import Zoom from '/presentation/node_modules/reveal.js/plugin/zoom/zoom.esm.js';

// Slide files to load in order
const slideFiles = [
  '/presentation/slides/00-title.html',
  '/presentation/slides/01-introduction.html',
  '/presentation/slides/02-background.html',
  '/presentation/slides/03-methodology.html',
  '/presentation/slides/04-implementation.html',
  '/presentation/slides/05-results.html',
  '/presentation/slides/06-discussion.html',
  '/presentation/slides/07-conclusion.html'
];

// Load slides then initialize
async function loadSlides() {
  const container = document.getElementById('slides-container');

  try {
    const responses = await Promise.all(
      slideFiles.map(file => fetch(file).then(r => {
        if (!r.ok) throw new Error(`Failed to load ${file}: ${r.status}`);
        return r.text();
      }))
    );

    container.innerHTML = responses.join('\n');
    initReveal();
  } catch (error) {
    console.error('Error loading slides:', error);
    container.innerHTML = `
      <section>
        <h2>Error Loading Slides</h2>
        <p>${error.message}</p>
      </section>
    `;
  }
}

function initReveal() {
  Reveal.initialize({
    width: 1920,
    height: 1080,
    margin: 0.04,
    minScale: 0.2,
    maxScale: 2.0,

    hash: true,
    history: true,
    slideNumber: 'c/t',

    transition: 'slide',
    transitionSpeed: 'default',
    backgroundTransition: 'fade',

    autoSlide: 0,
    controls: true,
    controlsLayout: 'bottom-right',
    progress: true,
    keyboard: true,
    overview: true,
    touch: true,
    fragments: true,
    center: true,

    hideInactiveCursor: true,
    hideCursorTime: 3000,

    plugins: [Markdown, Notes, Highlight, Zoom]
  }).then(() => {
    console.log('Reveal.js initialized');
    console.log('Keyboard shortcuts: S=notes, O=overview, F=fullscreen, ?=help');
  });
}

// Export for debugging
window.Reveal = Reveal;

// Start
loadSlides();
