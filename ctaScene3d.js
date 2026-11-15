/**
 * NEVO TECH - 3D WebGL Fluid Wave Ribbons for CTA Banner
 * Interactive glowing 3D wave mesh matching the design specification
 */

(function () {
  const container = document.getElementById('cta-3d-wrapper');
  if (!container) return;

  const scene = new THREE.Scene();
  const width = container.clientWidth || 500;
  const height = container.clientHeight || 300;

  const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 100);
  camera.position.set(0, 15, 25);
  camera.lookAt(0, 0, 0);

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  const canvas = renderer.domElement;
  canvas.id = 'cta-ribbon-canvas';
  container.appendChild(canvas);

  // Create undulating ribbon wave grid
  const cols = 55;
  const rows = 35;
  const planeGeo = new THREE.PlaneGeometry(38, 22, cols, rows);

  // Wireframe / glowing lines material
  const wireMat = new THREE.MeshBasicMaterial({
    color: 0x89e3f5,
    wireframe: true,
    transparent: true,
    opacity: 0.65,
    blending: THREE.AdditiveBlending
  });

  const waveMesh = new THREE.Mesh(planeGeo, wireMat);
  waveMesh.rotation.x = -Math.PI / 2.6;
  waveMesh.rotation.z = -0.3;
  waveMesh.position.set(2, 0, 0);
  scene.add(waveMesh);

  // Second layer wave with deep cyan for depth
  const wireMat2 = new THREE.MeshBasicMaterial({
    color: 0x0284c7,
    wireframe: true,
    transparent: true,
    opacity: 0.45,
    blending: THREE.AdditiveBlending
  });
  const waveMesh2 = new THREE.Mesh(planeGeo.clone(), wireMat2);
  waveMesh2.rotation.copy(waveMesh.rotation);
  waveMesh2.position.set(2, -1.2, 0);
  scene.add(waveMesh2);

  // Mouse interaction
  let mouse = { x: 0, y: 0 };
  window.addEventListener('mousemove', (e) => {
    const rect = container.getBoundingClientRect();
    if (e.clientX >= rect.left && e.clientX <= rect.right &&
        e.clientY >= rect.top && e.clientY <= rect.bottom) {
      mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -(((e.clientY - rect.top) / rect.height) * 2 - 1);
    }
  });

  const clock = new THREE.Clock();

  function animate() {
    requestAnimationFrame(animate);

    const time = clock.getElapsedTime() * 1.8;
    const positions = waveMesh.geometry.attributes.position;
    const positions2 = waveMesh2.geometry.attributes.position;

    for (let i = 0; i <= rows; i++) {
      for (let j = 0; j <= cols; j++) {
        const index = i * (cols + 1) + j;
        const u = j / cols;
        const v = i / rows;

        // Wave formula with multiple sine harmonics
        const wave = Math.sin(u * 5.0 + time) * 1.8 +
                     Math.cos(v * 4.0 + time * 0.8) * 1.4 +
                     Math.sin((u + v) * 3.0 + time * 1.2) * 1.0 +
                     (mouse.x * 2.0 * Math.sin(u * Math.PI));

        positions.setZ(index, wave);
        positions2.setZ(index, wave * 0.85);
      }
    }

    positions.needsUpdate = true;
    positions2.needsUpdate = true;

    // Gentle camera parallax
    camera.position.x += (mouse.x * 3.0 - camera.position.x) * 0.05;
    camera.position.y += ((15 + mouse.y * 2.0) - camera.position.y) * 0.05;
    camera.lookAt(0, 0, 0);

    renderer.render(scene, camera);
  }

  animate();

  // Resize handler
  window.addEventListener('resize', () => {
    const newW = container.clientWidth;
    const newH = container.clientHeight;
    camera.aspect = newW / newH;
    camera.updateProjectionMatrix();
    renderer.setSize(newW, newH);
  });
})();
