/**
 * Video Controller Module
 * Manages video backgrounds and inline videos in Reveal.js
 */

// Store video references
const videos = new Map();
let currentSlideVideos = [];

/**
 * Initialize video controller
 */
export function initVideoController() {
  // Find all videos in the presentation
  const allVideos = document.querySelectorAll('video');

  allVideos.forEach((video, index) => {
    const videoId = video.id || `video-${index}`;
    videos.set(videoId, video);

    // Set default properties
    video.playsInline = true;
    video.muted = true;  // Mute by default for autoplay

    // Preload metadata
    if (!video.preload) {
      video.preload = 'metadata';
    }
  });

  // Listen for slide changes
  if (window.Reveal) {
    Reveal.on('slidechanged', handleSlideChange);
    Reveal.on('ready', handleSlideChange);
  }

  console.log(`Video controller initialized with ${videos.size} videos`);

  // Expose global API
  window.videoController = {
    play: playVideo,
    pause: pauseVideo,
    pauseAll,
    getVideo: (id) => videos.get(id)
  };
}

/**
 * Handle slide change - manage video playback
 */
function handleSlideChange(event) {
  const slide = event?.currentSlide || Reveal.getCurrentSlide();

  // Pause all previous videos
  pauseAll();

  // Find videos in current slide
  currentSlideVideos = Array.from(slide.querySelectorAll('video'));

  // Also check for background videos
  const backgroundVideo = slide.slideBackgroundContentElement?.querySelector('video');
  if (backgroundVideo) {
    currentSlideVideos.push(backgroundVideo);
  }

  // Auto-play videos with autoplay attribute
  currentSlideVideos.forEach(video => {
    if (video.hasAttribute('data-autoplay') || video.hasAttribute('autoplay')) {
      playVideo(video);
    }
  });
}

/**
 * Play a video (by element or ID)
 */
export function playVideo(videoOrId) {
  const video = typeof videoOrId === 'string'
    ? videos.get(videoOrId)
    : videoOrId;

  if (!video) return;

  video.currentTime = 0;
  video.play().catch(err => {
    console.warn('Video autoplay blocked:', err.message);
    // Try muted autoplay
    video.muted = true;
    video.play().catch(() => {});
  });
}

/**
 * Pause a video
 */
export function pauseVideo(videoOrId) {
  const video = typeof videoOrId === 'string'
    ? videos.get(videoOrId)
    : videoOrId;

  if (video) {
    video.pause();
  }
}

/**
 * Pause all videos
 */
export function pauseAll() {
  videos.forEach(video => video.pause());

  // Also pause any background videos
  document.querySelectorAll('.slide-background video').forEach(v => v.pause());
}

/**
 * Create a video element with common settings
 */
export function createVideo(options) {
  const {
    src,
    poster,
    loop = true,
    muted = true,
    autoplay = false,
    controls = false
  } = options;

  const video = document.createElement('video');
  video.src = src;
  video.loop = loop;
  video.muted = muted;
  video.playsInline = true;
  video.preload = 'metadata';

  if (poster) video.poster = poster;
  if (controls) video.controls = true;
  if (autoplay) video.dataset.autoplay = '';

  return video;
}

/**
 * Create a video comparison (side by side)
 */
export function createVideoComparison(leftSrc, rightSrc, options = {}) {
  const container = document.createElement('div');
  container.className = 'video-comparison';
  container.style.cssText = `
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  `;

  const leftVideo = createVideo({ src: leftSrc, ...options });
  const rightVideo = createVideo({ src: rightSrc, ...options });

  // Sync playback
  leftVideo.addEventListener('play', () => rightVideo.play());
  leftVideo.addEventListener('pause', () => rightVideo.pause());
  leftVideo.addEventListener('seeked', () => {
    rightVideo.currentTime = leftVideo.currentTime;
  });

  const leftWrapper = document.createElement('div');
  leftWrapper.className = 'video-wrapper';
  leftWrapper.appendChild(leftVideo);
  if (options.leftLabel) {
    const label = document.createElement('div');
    label.className = 'video-label';
    label.textContent = options.leftLabel;
    leftWrapper.appendChild(label);
  }

  const rightWrapper = document.createElement('div');
  rightWrapper.className = 'video-wrapper';
  rightWrapper.appendChild(rightVideo);
  if (options.rightLabel) {
    const label = document.createElement('div');
    label.className = 'video-label';
    label.textContent = options.rightLabel;
    rightWrapper.appendChild(label);
  }

  container.appendChild(leftWrapper);
  container.appendChild(rightWrapper);

  // Add controls to sync play/pause
  container.play = () => {
    leftVideo.play();
    rightVideo.play();
  };

  container.pause = () => {
    leftVideo.pause();
    rightVideo.pause();
  };

  return container;
}

/**
 * Preload videos for smoother transitions
 */
export function preloadVideos(sources) {
  sources.forEach(src => {
    const link = document.createElement('link');
    link.rel = 'preload';
    link.as = 'video';
    link.href = src;
    document.head.appendChild(link);
  });
}

/**
 * Add play button overlay for user interaction requirement
 */
export function addPlayButton(video) {
  const wrapper = video.parentElement || document.body;
  const overlay = document.createElement('div');
  overlay.className = 'video-play-overlay';
  overlay.innerHTML = `
    <button class="play-button" aria-label="Play video">
      <svg viewBox="0 0 24 24" width="64" height="64">
        <polygon points="5,3 19,12 5,21" fill="white"/>
      </svg>
    </button>
  `;
  overlay.style.cssText = `
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0,0,0,0.3);
    cursor: pointer;
    transition: opacity 0.3s;
  `;

  overlay.addEventListener('click', () => {
    video.play();
    overlay.style.opacity = '0';
    setTimeout(() => overlay.remove(), 300);
  });

  wrapper.style.position = 'relative';
  wrapper.appendChild(overlay);
}
