/**
 * NEVO TECH - Cinematic Normal Video Player with Interactive Scroll Effort Physics
 * 
 * Features:
 * - Normal high-definition video player displaying neural typing footage
 * - Interactive Scroll Effort Physics Engine:
 *   - Video frame resists scrolling with spring-damper inertia and elastic perspective tilt
 *   - Live Scroll Effort Telemetry HUD gauge (0% - 100% Tension)
 *   - Glowing kinetic tension border reacting to scroll acceleration
 *   - Scroll-driven scrubber acceleration
 * - Video Controls: Play/Pause, Live Scrubber, Timecode, Audio FX, Fullscreen
 * - Subtle live 2D neural particle sparkle overlay over the video
 */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', () => {
    const videoContainer = document.getElementById('hero-video-container');
    const videoFrame = document.getElementById('video-frame');
    const videoImg = document.getElementById('hero-video-img');
    const particleCanvas = document.getElementById('video-particle-canvas');
    const centerPlayBtn = document.getElementById('video-center-play-btn');
    const playPauseBtn = document.getElementById('vid-play-pause-btn');
    const playIcon = document.getElementById('vid-play-icon');
    const timecodeEl = document.getElementById('vid-timecode');
    const scrubberTrack = document.getElementById('vid-scrubber-track');
    const scrubberProgress = document.getElementById('vid-scrubber-progress');
    const scrubberHandle = document.getElementById('vid-scrubber-handle');
    const audioBtn = document.getElementById('vid-audio-btn');
    const audioIcon = document.getElementById('vid-audio-icon');
    const fullscreenBtn = document.getElementById('vid-fullscreen-btn');
    const effortGaugeFill = document.getElementById('effort-gauge-fill');
    const effortLabelText = document.getElementById('effort-label-text');
    const effortPercentageText = document.getElementById('effort-percentage-text');
    const videoEffortBorder = document.getElementById('video-effort-border');

    if (!videoContainer || !videoFrame) return;

    // -------------------------------------------------------------
    // 1. VIDEO PLAYBACK STATE
    // -------------------------------------------------------------
    let isPlaying = true;
    let currentTime = 14.5; // Start at realistic mid-time
    const duration = 84.0; // 1m 24s total video
    let isAudioActive = false;
    let lastTimeUpdate = performance.now();

    function formatTime(seconds) {
      const mins = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    function updateTimecodeUI() {
      if (timecodeEl) {
        timecodeEl.textContent = `${formatTime(currentTime)} / ${formatTime(duration)}`;
      }
      const progressPercent = (currentTime / duration) * 100;
      if (scrubberProgress) scrubberProgress.style.width = `${progressPercent}%`;
      if (scrubberHandle) scrubberHandle.style.left = `${progressPercent}%`;
    }

    function togglePlayPause() {
      isPlaying = !isPlaying;
      if (isPlaying) {
        if (playIcon) playIcon.textContent = '❚❚';
        if (centerPlayBtn) centerPlayBtn.classList.remove('paused');
        if (videoImg) videoImg.classList.remove('paused');
        if (window.playSfx) window.playSfx('click');
      } else {
        if (playIcon) playIcon.textContent = '▶';
        if (centerPlayBtn) centerPlayBtn.classList.add('paused');
        if (videoImg) videoImg.classList.add('paused');
        if (window.playSfx) window.playSfx('click');
      }
    }

    if (centerPlayBtn) centerPlayBtn.addEventListener('click', togglePlayPause);
    if (playPauseBtn) playPauseBtn.addEventListener('click', togglePlayPause);

    // Click on video frame toggles play/pause
    videoFrame.addEventListener('click', (e) => {
      // Ignore if clicking on bottom controls bar or buttons
      if (e.target.closest('.video-controls-bar') || e.target.closest('.video-center-play-btn')) {
        return;
      }
      togglePlayPause();
    });

    // Scrubber click seeking
    if (scrubberTrack) {
      scrubberTrack.addEventListener('click', (e) => {
        const rect = scrubberTrack.getBoundingClientRect();
        const clickRatio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
        currentTime = clickRatio * duration;
        updateTimecodeUI();
        if (window.playSfx) window.playSfx('hover');
      });
    }

    // Audio SFX Toggle
    if (audioBtn) {
      audioBtn.addEventListener('click', () => {
        isAudioActive = !isAudioActive;
        if (isAudioActive) {
          if (audioIcon) audioIcon.textContent = '🔊';
          audioBtn.classList.add('active');
          if (window.showToast) window.showToast('Video Typing Audio Active');
          if (window.playSfx) window.playSfx('success');
        } else {
          if (audioIcon) audioIcon.textContent = '🔇';
          audioBtn.classList.remove('active');
          if (window.showToast) window.showToast('Video Audio Muted');
        }
      });
    }

    // Fullscreen Toggle
    if (fullscreenBtn) {
      fullscreenBtn.addEventListener('click', () => {
        if (!document.fullscreenElement) {
          videoContainer.requestFullscreen().catch(err => {
            console.warn('Fullscreen error:', err);
          });
        } else {
          document.exitFullscreen();
        }
      });
    }

    // -------------------------------------------------------------
    // 2. SCROLL EFFORT PHYSICS ENGINE
    // -------------------------------------------------------------
    // Spring-mass variables
    let effortTension = 0;       // Current tension 0.0 to 1.0
    let targetTension = 0;       // Target tension accumulating from scroll
    let effortTilt = 0;          // Current degrees of tilt
    let targetTilt = 0;          // Target degrees
    let effortY = 0;             // Vertical displacement
    let targetY = 0;
    let effortScale = 1.0;

    /**
     * Called whenever page scrolls or wheel is turned
     * @param {number} velocity Scroll velocity or delta
     * @param {number} direction 1 for scroll down, -1 for scroll up
     */
    window.applyVideoScrollEffort = function (velocity, direction = 1, currentScroll = 0) {
      const absVel = Math.min(Math.abs(velocity) || 1.0, 18.0);

      // Accumulate tension based on physical scrolling effort
      targetTension = Math.min(targetTension + absVel * 0.08, 1.0);

      // Tilt resistance: scrolling down pushes the top away; scrolling up pulls it forward
      if (direction >= 0) {
        targetTilt = -Math.min(absVel * 0.42, 6.5); // Tilt back (resistance)
        targetY = Math.min(absVel * 0.75, 12.0);    // Push down
      } else {
        targetTilt = Math.min(absVel * 0.42, 6.5);  // Tilt forward
        targetY = -Math.min(absVel * 0.75, 12.0);   // Pull up
      }

      // Slightly scrub the video forward under scrolling effort!
      if (isPlaying) {
        currentTime = (currentTime + absVel * 0.04) % duration;
      }
    };

    // Native wheel listener to guarantee immediate scroll effort response
    window.addEventListener('wheel', (e) => {
      const dir = Math.sign(e.deltaY);
      const intensity = Math.abs(e.deltaY) * 0.04;
      window.applyVideoScrollEffort(intensity, dir, window.scrollY);
    }, { passive: true });

    // -------------------------------------------------------------
    // 3. LIVE 2D NEURAL SPARKLE OVERLAY CANVAS
    // -------------------------------------------------------------
    let pCtx = null;
    const particles = [];
    const pCount = 38;

    if (particleCanvas) {
      pCtx = particleCanvas.getContext('2d');

      function resizeCanvas() {
        if (!particleCanvas || !videoFrame) return;
        particleCanvas.width = videoFrame.clientWidth || 600;
        particleCanvas.height = videoFrame.clientHeight || 480;
      }
      resizeCanvas();
      window.addEventListener('resize', resizeCanvas);

      for (let i = 0; i < pCount; i++) {
        particles.push({
          x: Math.random() * (particleCanvas.width || 600),
          y: Math.random() * (particleCanvas.height || 480),
          radius: 1.0 + Math.random() * 2.2,
          vx: (Math.random() - 0.5) * 0.6,
          vy: -0.2 - Math.random() * 0.6,
          alpha: 0.2 + Math.random() * 0.7,
          pulse: Math.random() * Math.PI * 2,
          isWarm: Math.random() > 0.75 // Warm amber or electric cyan
        });
      }
    }

    function renderParticles(delta, tension) {
      if (!pCtx || !particleCanvas) return;
      const w = particleCanvas.width;
      const h = particleCanvas.height;
      pCtx.clearRect(0, 0, w, h);

      const speedFactor = 1.0 + tension * 2.8;

      particles.forEach(p => {
        p.x += p.vx * speedFactor;
        p.y += p.vy * speedFactor;
        p.pulse += delta * 3.0 * speedFactor;

        // Wrap around
        if (p.y < 0) p.y = h;
        if (p.x < 0) p.x = w;
        if (p.x > w) p.x = 0;

        const currentAlpha = Math.max(0.1, Math.min(1.0, p.alpha + Math.sin(p.pulse) * 0.25 + tension * 0.3));

        pCtx.beginPath();
        pCtx.arc(p.x, p.y, p.radius * (1 + tension * 0.4), 0, Math.PI * 2);

        if (p.isWarm) {
          pCtx.fillStyle = `rgba(245, 158, 11, ${currentAlpha * 0.7})`;
        } else {
          pCtx.fillStyle = `rgba(56, 189, 248, ${currentAlpha})`;
        }
        pCtx.shadowBlur = 8 + tension * 12;
        pCtx.shadowColor = p.isWarm ? '#f59e0b' : '#38bdf8';
        pCtx.fill();
      });

      // Reset shadow for performance
      pCtx.shadowBlur = 0;
    }

    // -------------------------------------------------------------
    // 4. ANIMATION & TENSION PHYSICS LOOP
    // -------------------------------------------------------------
    let soundCooldown = 0;

    function physicsLoop(now) {
      requestAnimationFrame(physicsLoop);

      const delta = Math.min((now - lastTimeUpdate) / 1000, 0.1);
      lastTimeUpdate = now;

      // 1. Advance Video Timecode
      if (isPlaying) {
        // Under scroll effort, video playback accelerates slightly
        const playRate = 1.0 + effortTension * 1.5;
        currentTime = (currentTime + delta * playRate) % duration;
        updateTimecodeUI();

        // 2. Periodic Audio Typing Clicks (if audio unmuted)
        if (isAudioActive && window.playSfx) {
          soundCooldown += delta * playRate;
          if (soundCooldown > 0.22) {
            soundCooldown = 0;
            window.playSfx('click');
          }
        }
      }

      // 3. Spring Physics Calculation
      // Tension decays smoothly back to 0 when scrolling stops
      effortTension += (targetTension - effortTension) * 0.12;
      targetTension *= 0.91;
      if (effortTension < 0.002) effortTension = 0;

      // Elastic Tilt & Displacement
      effortTilt += (targetTilt - effortTilt) * 0.14;
      targetTilt *= 0.88;

      effortY += (targetY - effortY) * 0.14;
      targetY *= 0.88;

      // Squash and stretch under tension
      effortScale = 1.0 - Math.min(Math.abs(effortTilt) * 0.005, 0.035);

      // 4. Apply 3D Elastic Effort Transform to Video Frame
      videoFrame.style.transform = `perspective(1200px) rotateX(${effortTilt.toFixed(2)}deg) translateY(${effortY.toFixed(2)}px) scale(${effortScale.toFixed(3)})`;

      // 5. Update Telemetry HUD Gauge
      const tensionPct = Math.round(effortTension * 100);
      if (effortGaugeFill) {
        effortGaugeFill.style.width = `${tensionPct}%`;
      }
      if (effortPercentageText) {
        effortPercentageText.textContent = `${tensionPct}%`;
      }

      if (effortLabelText) {
        if (effortTension < 0.05) {
          effortLabelText.textContent = 'SCROLL EFFORT: IDLE';
          if (effortGaugeFill) effortGaugeFill.style.background = 'var(--color-highlight)';
        } else if (effortTension < 0.40) {
          effortLabelText.textContent = 'SCROLL EFFORT: RESISTANCE';
          if (effortGaugeFill) effortGaugeFill.style.background = 'linear-gradient(90deg, #38bdf8, #89e3f5)';
        } else if (effortTension < 0.75) {
          effortLabelText.textContent = 'SCROLL EFFORT: KINETIC TENSION';
          if (effortGaugeFill) effortGaugeFill.style.background = 'linear-gradient(90deg, #38bdf8, #00f0ff)';
        } else {
          effortLabelText.textContent = 'SCROLL EFFORT: MAXIMUM DRAG';
          if (effortGaugeFill) effortGaugeFill.style.background = 'linear-gradient(90deg, #f59e0b, #00f0ff)';
        }
      }

      // 6. Glowing Tension Border Intensity
      if (videoEffortBorder) {
        videoEffortBorder.style.opacity = Math.min(1.0, 0.15 + effortTension * 0.85);
        const glowRadius = Math.round(15 + effortTension * 35);
        videoEffortBorder.style.boxShadow = `inset 0 0 ${glowRadius}px rgba(56, 189, 248, ${0.15 + effortTension * 0.5}), 0 0 ${glowRadius}px rgba(56, 189, 248, ${0.2 + effortTension * 0.6})`;
      }

      // 7. Render Particle Sparkles
      renderParticles(delta, effortTension);
    }

    requestAnimationFrame(physicsLoop);
    updateTimecodeUI();
  });
})();
