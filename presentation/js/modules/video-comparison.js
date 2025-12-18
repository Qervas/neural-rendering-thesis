/**
 * Video Comparison Module for Reveal.js
 * Syncs side-by-side videos and provides playback controls
 */

export function initVideoComparison(Reveal) {
  // Initialize on slide change
  Reveal.on('slidechanged', event => {
    // Pause videos on previous slide
    const previousVideos = event.previousSlide?.querySelectorAll('.video-comparison video');
    previousVideos?.forEach(v => v.pause());

    // Setup comparison on current slide
    setupVideoComparison(event.currentSlide);
  });

  // Also setup on ready for initial slide
  Reveal.on('ready', event => {
    setupVideoComparison(event.currentSlide);
  });

  console.log('Video comparison module initialized');
}

function setupVideoComparison(slide) {
  if (!slide) return;

  const comparisons = slide.querySelectorAll('.video-comparison');
  comparisons.forEach(container => {
    const videos = Array.from(container.querySelectorAll('video'));
    if (videos.length < 2) return;

    // Check if already initialized
    if (container.dataset.initialized === 'true') {
      // Just restart videos
      videos.forEach(v => {
        v.currentTime = 0;
        v.play().catch(() => {});
      });
      return;
    }
    container.dataset.initialized = 'true';

    // Setup video sync
    setupVideoSync(videos);

    // Add controls
    addVideoControls(container, videos);

    // Start playback
    videos.forEach(v => {
      v.currentTime = 0;
      v.play().catch(() => {});
    });

    console.log(`Video comparison initialized with ${videos.length} videos`);
  });
}

function setupVideoSync(videos) {
  const master = videos[0];
  const slaves = videos.slice(1);

  // Sync on timeupdate
  master.addEventListener('timeupdate', () => {
    slaves.forEach(slave => {
      if (Math.abs(slave.currentTime - master.currentTime) > 0.2) {
        slave.currentTime = master.currentTime;
      }
    });
  });

  // Sync on loop restart
  master.addEventListener('seeked', () => {
    if (master.currentTime < 0.5) {
      slaves.forEach(slave => {
        slave.currentTime = 0;
      });
    }
  });
}

function addVideoControls(container, videos) {
  // Fix container layout - make it a column flex so controls go below
  container.style.flexWrap = 'wrap';

  // Create controls container - full width to force new row
  const controls = document.createElement('div');
  controls.className = 'video-comparison-controls';
  controls.style.width = '100%'; // Force to new row
  controls.innerHTML = `
    <button class="vc-btn vc-frame-back" title="Previous frame (←)">◀◀</button>
    <button class="vc-btn vc-play-pause" title="Play/Pause (Space)">⏸</button>
    <button class="vc-btn vc-frame-forward" title="Next frame (→)">▶▶</button>
    <div class="vc-progress">
      <div class="vc-progress-bar"></div>
    </div>
    <span class="vc-speed-label">Speed:</span>
    <select class="vc-speed-select">
      <option value="0.25">0.25x</option>
      <option value="0.5">0.5x</option>
      <option value="0.75">0.75x</option>
      <option value="1" selected>1x</option>
      <option value="1.5">1.5x</option>
      <option value="2">2x</option>
    </select>
  `;

  // Add styles
  addControlStyles();

  // Get control elements
  const playPauseBtn = controls.querySelector('.vc-play-pause');
  const frameBackBtn = controls.querySelector('.vc-frame-back');
  const frameForwardBtn = controls.querySelector('.vc-frame-forward');
  const progressBar = controls.querySelector('.vc-progress-bar');
  const progressContainer = controls.querySelector('.vc-progress');
  const speedSelect = controls.querySelector('.vc-speed-select');

  // Play/Pause
  playPauseBtn.onclick = () => togglePlayPause(videos, playPauseBtn);

  // Frame controls
  frameBackBtn.onclick = () => stepFrame(videos, -1, playPauseBtn);
  frameForwardBtn.onclick = () => stepFrame(videos, 1, playPauseBtn);

  // Speed control
  speedSelect.onchange = () => {
    const speed = parseFloat(speedSelect.value);
    videos.forEach(v => v.playbackRate = speed);
  };

  // Progress bar update
  videos[0].addEventListener('timeupdate', () => {
    const percent = (videos[0].currentTime / videos[0].duration) * 100;
    progressBar.style.width = percent + '%';
  });

  // Click to seek
  progressContainer.onclick = (e) => {
    const rect = progressContainer.getBoundingClientRect();
    const percent = (e.clientX - rect.left) / rect.width;
    const time = percent * videos[0].duration;
    videos.forEach(v => v.currentTime = time);
  };

  // Keyboard shortcuts
  const keyHandler = (e) => {
    // Only handle if this slide is active
    if (!container.closest('section.present')) return;

    if (e.code === 'Space' && !['BUTTON', 'SELECT', 'INPUT'].includes(e.target.tagName)) {
      e.preventDefault();
      e.stopPropagation();
      togglePlayPause(videos, playPauseBtn);
    } else if (e.code === 'ArrowLeft' && !e.ctrlKey && !e.metaKey) {
      e.preventDefault();
      e.stopPropagation();
      stepFrame(videos, -1, playPauseBtn);
    } else if (e.code === 'ArrowRight' && !e.ctrlKey && !e.metaKey) {
      e.preventDefault();
      e.stopPropagation();
      stepFrame(videos, 1, playPauseBtn);
    }
  };

  document.addEventListener('keydown', keyHandler);

  container.appendChild(controls);
}

function togglePlayPause(videos, btn) {
  if (videos[0].paused) {
    videos.forEach(v => v.play());
    btn.textContent = '⏸';
  } else {
    videos.forEach(v => v.pause());
    btn.textContent = '▶';
  }
}

function stepFrame(videos, direction, btn) {
  const frameTime = 0.033; // ~30fps
  videos.forEach(v => {
    v.pause();
    v.currentTime = Math.max(0, Math.min(v.duration, v.currentTime + (direction * frameTime)));
  });
  btn.textContent = '▶';
}

function addControlStyles() {
  if (document.getElementById('video-comparison-styles')) return;

  const style = document.createElement('style');
  style.id = 'video-comparison-styles';
  style.textContent = `
    .video-comparison-controls {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 1em;
      margin-top: 1em;
      padding: 1em 1.5em;
      background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
      border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    .vc-btn {
      font-size: 1.4em;
      background: white;
      border: 2px solid #dee2e6;
      border-radius: 8px;
      cursor: pointer;
      padding: 0.4em 0.8em;
      transition: all 0.2s;
      color: #333;
    }

    .vc-btn:hover {
      background: #0cc7d3;
      border-color: #0cc7d3;
      color: white;
      transform: scale(1.05);
    }

    .vc-btn:active {
      transform: scale(0.95);
    }

    .vc-progress {
      flex: 1;
      max-width: 400px;
      height: 12px;
      background: #dee2e6;
      border-radius: 6px;
      cursor: pointer;
      overflow: hidden;
    }

    .vc-progress-bar {
      height: 100%;
      background: linear-gradient(90deg, #0cc7d3 0%, #00a3e0 100%);
      border-radius: 6px;
      width: 0%;
      transition: width 0.1s linear;
    }

    .vc-speed-label {
      font-size: 0.95em;
      color: #666;
      font-weight: 500;
    }

    .vc-speed-select {
      font-size: 1em;
      padding: 0.5em 0.8em;
      border-radius: 6px;
      border: 2px solid #dee2e6;
      background: white;
      cursor: pointer;
      font-weight: 500;
    }

    .vc-speed-select:hover {
      border-color: #0cc7d3;
    }

    .vc-speed-select:focus {
      outline: none;
      border-color: #0cc7d3;
      box-shadow: 0 0 0 3px rgba(12, 199, 211, 0.2);
    }
  `;
  document.head.appendChild(style);
}
