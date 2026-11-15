/**
 * NEVO TECH - 3D Interactive Cyber Neural Typing Experience
 * Inspired by tactile illuminated keyboard with 3D neural constellation graph,
 * floating cinematic bokeh, synaptic data pulses, and interactive typing ripples.
 * Built with Three.js (WebGL).
 */

(function () {
  const container = document.getElementById('hero-3d-canvas-container');
  if (!container) return;

  // -----------------------------------------------------------------
  // 1. SCENE, CAMERA, RENDERER
  // -----------------------------------------------------------------
  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x090e18, 0.016);

  const width = container.clientWidth || 600;
  const height = container.clientHeight || 540;

  const camera = new THREE.PerspectiveCamera(42, width / height, 0.1, 1000);
  camera.position.set(0, 13, 23);
  camera.lookAt(0, 2, -2);

  const renderer = new THREE.WebGLRenderer({
    antialias: true,
    alpha: true,
    powerPreference: 'high-performance'
  });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.3;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  const canvasElement = renderer.domElement;
  canvasElement.id = 'hero-3d-canvas';
  container.appendChild(canvasElement);

  // Main group for 3D elements
  const mainGroup = new THREE.Group();
  scene.add(mainGroup);

  // Group for the laptop and keyboard
  const laptopGroup = new THREE.Group();
  laptopGroup.position.set(0, -1.8, 0);
  laptopGroup.rotation.x = 0.28; // Tilted slightly towards camera like photo
  mainGroup.add(laptopGroup);

  // Group for the floating neural constellation
  const neuralGroup = new THREE.Group();
  mainGroup.add(neuralGroup);

  // Group for bokeh discs
  const bokehGroup = new THREE.Group();
  mainGroup.add(bokehGroup);

  // -----------------------------------------------------------------
  // 2. PROCEDURAL TEXTURES (GLOWING NODES & SOFT BOKEH)
  // -----------------------------------------------------------------
  function createRadialGlowTexture(colorInner, colorOuter) {
    const canvas = document.createElement('canvas');
    canvas.width = 128;
    canvas.height = 128;
    const ctx = canvas.getContext('2d');
    const grad = ctx.createRadialGradient(64, 64, 0, 64, 64, 64);
    grad.addColorStop(0.0, colorInner);
    grad.addColorStop(0.4, colorOuter);
    grad.addColorStop(1.0, 'rgba(0,0,0,0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 128, 128);
    const texture = new THREE.CanvasTexture(canvas);
    texture.generateMipmaps = false;
    texture.minFilter = THREE.LinearFilter;
    return texture;
  }

  const cyanGlowTexture = createRadialGlowTexture('rgba(255, 255, 255, 1)', 'rgba(56, 189, 248, 0.85)');
  const warmAmberGlowTexture = createRadialGlowTexture('rgba(255, 240, 200, 0.95)', 'rgba(245, 158, 11, 0.7)');
  const blueBokehTexture = createRadialGlowTexture('rgba(137, 227, 245, 0.8)', 'rgba(14, 165, 233, 0.45)');

  // -----------------------------------------------------------------
  // 3. LIGHTING (CYBER DUSK WITH WARM AMBER & CYAN BACKLIGHT)
  // -----------------------------------------------------------------
  const ambientLight = new THREE.AmbientLight(0x0e1726, 2.2);
  scene.add(ambientLight);

  // Directional key light
  const dirLight = new THREE.DirectionalLight(0x89e3f5, 2.4);
  dirLight.position.set(15, 25, 20);
  dirLight.castShadow = true;
  scene.add(dirLight);

  // Warm backlight matching golden bokeh in user photo
  const warmBackLight = new THREE.PointLight(0xf59e0b, 3.8, 35);
  warmBackLight.position.set(4, 10, -8);
  scene.add(warmBackLight);

  // Keyboard under-glow cyan point light
  const keyboardGlowLight = new THREE.PointLight(0x38bdf8, 4.0, 20);
  keyboardGlowLight.position.set(0, 1.5, 2);
  laptopGroup.add(keyboardGlowLight);

  // -----------------------------------------------------------------
  // 4. LAYERED CINEMATIC BACKDROP (REFERENCE PHOTO BLEND)
  // -----------------------------------------------------------------
  const textureLoader = new THREE.TextureLoader();
  textureLoader.load(
    'assets/hero-neural-typing.webp',
    function (tex) {
      tex.minFilter = THREE.LinearFilter;
      const bgGeo = new THREE.PlaneGeometry(42, 26);
      const bgMat = new THREE.MeshBasicMaterial({
        map: tex,
        transparent: true,
        opacity: 0.38,
        depthWrite: false,
        blending: THREE.NormalBlending
      });
      const bgMesh = new THREE.Mesh(bgGeo, bgMat);
      bgMesh.position.set(0, 5, -14);
      mainGroup.add(bgMesh);
    },
    undefined,
    function (err) {
      console.warn('Could not load hero backdrop texture:', err);
    }
  );

  // -----------------------------------------------------------------
  // 5. 3D CYBER LAPTOP BODY & KEYBOARD MATRIX
  // -----------------------------------------------------------------
  // Laptop Base Chassis
  const baseGeo = new THREE.BoxGeometry(22, 0.7, 14.5);
  const baseMat = new THREE.MeshStandardMaterial({
    color: 0x0c121e,
    roughness: 0.35,
    metalness: 0.8
  });
  const laptopBase = new THREE.Mesh(baseGeo, baseMat);
  laptopBase.position.y = -0.35;
  laptopBase.receiveShadow = true;
  laptopGroup.add(laptopBase);

  // Glowing Cyber Rim along the front edge of the chassis
  const rimGeo = new THREE.BoxGeometry(22.2, 0.1, 0.2);
  const rimMat = new THREE.MeshBasicMaterial({
    color: 0x38bdf8,
    transparent: true,
    opacity: 0.85
  });
  const rimMesh = new THREE.Mesh(rimGeo, rimMat);
  rimMesh.position.set(0, -0.05, 7.3);
  laptopGroup.add(rimMesh);

  // Trackpad
  const trackpadGeo = new THREE.PlaneGeometry(6.5, 4.2);
  const trackpadMat = new THREE.MeshStandardMaterial({
    color: 0x141d2e,
    roughness: 0.25,
    metalness: 0.65
  });
  const trackpad = new THREE.Mesh(trackpadGeo, trackpadMat);
  trackpad.rotation.x = -Math.PI / 2;
  trackpad.position.set(0, 0.02, 4.6);
  laptopGroup.add(trackpad);

  // Trackpad accent border
  const trackpadBorderGeo = new THREE.RingGeometry(3.3, 3.35, 4);
  const trackpadBorderMat = new THREE.MeshBasicMaterial({
    color: 0x38bdf8,
    transparent: true,
    opacity: 0.35,
    side: THREE.DoubleSide
  });
  const trackpadBorder = new THREE.Mesh(trackpadBorderGeo, trackpadBorderMat);
  trackpadBorder.rotation.x = -Math.PI / 2;
  trackpadBorder.rotation.z = Math.PI / 4;
  trackpadBorder.position.set(0, 0.03, 4.6);
  laptopGroup.add(trackpadBorder);

  // Open Screen in Background (angled at 112 deg)
  const screenGroup = new THREE.Group();
  screenGroup.position.set(0, 0, -7.2);
  screenGroup.rotation.x = -0.38; // Screen opened backwards
  laptopGroup.add(screenGroup);

  const screenLidGeo = new THREE.BoxGeometry(22, 13.5, 0.5);
  const screenLidMat = new THREE.MeshStandardMaterial({
    color: 0x080d16,
    roughness: 0.3,
    metalness: 0.85
  });
  const screenLid = new THREE.Mesh(screenLidGeo, screenLidMat);
  screenLid.position.y = 6.8;
  screenGroup.add(screenLid);

  // Display Panel with Holographic Code Interface
  const displayCanvas = document.createElement('canvas');
  displayCanvas.width = 512;
  displayCanvas.height = 320;
  const dCtx = displayCanvas.getContext('2d');

  function renderDisplayContent() {
    dCtx.fillStyle = '#050912';
    dCtx.fillRect(0, 0, 512, 320);

    // Glowing Header Bar
    dCtx.fillStyle = '#0f172a';
    dCtx.fillRect(0, 0, 512, 36);
    dCtx.fillStyle = '#38bdf8';
    dCtx.font = 'bold 14px monospace';
    dCtx.fillText('NEVO AI CORE v4.2 // SYNAPSE ENGINE ACTIVE', 20, 24);

    // Terminal Code Lines
    dCtx.fillStyle = '#89e3f5';
    dCtx.font = '12px monospace';
    const lines = [
      '> import { NeuralMesh, SynapseStream } from "@nevo/core";',
      '> const agent = new AutonomousAgent({ latency: "0.2ms" });',
      '> agent.synthesizeKnowledgeGraph({ nodes: 130, dense: true });',
      '> [OK] Holographic input vector initialized.',
      '> [SYNC] Cloud cluster latency: 12ms (Global Mesh)',
      '> await agent.executeWorkflow("Realtime Neural Typing");',
      '> ----------------------------------------------------',
      '> Status: READY // Listening for tactile input...'
    ];
    lines.forEach((line, i) => {
      dCtx.fillStyle = i % 2 === 0 ? '#38bdf8' : '#cbd5e1';
      dCtx.fillText(line, 20, 68 + i * 28);
    });
  }
  renderDisplayContent();

  const displayTex = new THREE.CanvasTexture(displayCanvas);
  const displayGeo = new THREE.PlaneGeometry(20.5, 12);
  const displayMat = new THREE.MeshBasicMaterial({
    map: displayTex,
    transparent: true,
    opacity: 0.92
  });
  const displayMesh = new THREE.Mesh(displayGeo, displayMat);
  displayMesh.position.set(0, 6.8, 0.28);
  screenGroup.add(displayMesh);

  // Keyboard Well (Recessed bed with under-glow)
  const wellGeo = new THREE.PlaneGeometry(19.6, 7.8);
  const wellMat = new THREE.MeshBasicMaterial({
    color: 0x050c18,
    side: THREE.DoubleSide
  });
  const wellMesh = new THREE.Mesh(wellGeo, wellMat);
  wellMesh.rotation.x = -Math.PI / 2;
  wellMesh.position.set(0, 0.015, -1.8);
  laptopGroup.add(wellMesh);

  // Glowing Backlight Bed underneath the keys
  const bedGlowGeo = new THREE.PlaneGeometry(19.2, 7.5);
  const bedGlowMat = new THREE.MeshBasicMaterial({
    color: 0x0ea5e9,
    transparent: true,
    opacity: 0.35,
    side: THREE.DoubleSide
  });
  const bedGlowMesh = new THREE.Mesh(bedGlowGeo, bedGlowMat);
  bedGlowMesh.rotation.x = -Math.PI / 2;
  bedGlowMesh.position.set(0, 0.02, -1.8);
  laptopGroup.add(bedGlowMesh);

  // -----------------------------------------------------------------
  // 6. INDIVIDUAL 3D KEYCAPS WITH TACTILE TYPING PHYSICS
  // -----------------------------------------------------------------
  const keyMeshList = [];
  const keyRows = [
    { count: 14, z: -4.8, width: 1.15, depth: 1.05, gap: 0.2 },
    { count: 14, z: -3.4, width: 1.15, depth: 1.05, gap: 0.2 },
    { count: 13, z: -2.0, width: 1.25, depth: 1.05, gap: 0.2 },
    { count: 12, z: -0.6, width: 1.35, depth: 1.05, gap: 0.2 },
    { count: 8,  z:  0.8, width: 1.4,  depth: 1.05, gap: 0.2, spacebarIdx: 3 }
  ];

  const keyCapGeoShared = new THREE.BoxGeometry(1, 0.32, 1);
  const keyMatDefault = new THREE.MeshStandardMaterial({
    color: 0x162032,
    roughness: 0.3,
    metalness: 0.7
  });

  const keyGlowMat = new THREE.MeshStandardMaterial({
    color: 0x0284c7,
    emissive: 0x38bdf8,
    emissiveIntensity: 0.9,
    roughness: 0.2,
    metalness: 0.5
  });

  keyRows.forEach((rowConfig, rowIndex) => {
    const totalRowWidth = rowConfig.count * (rowConfig.width + rowConfig.gap);
    const startX = -totalRowWidth / 2 + rowConfig.width / 2;

    for (let c = 0; c < rowConfig.count; c++) {
      let keyW = rowConfig.width;
      let keyD = rowConfig.depth;

      // Special key sizing (spacebar)
      if (rowIndex === 4 && c === rowConfig.spacebarIdx) {
        keyW = 5.6; // elongated spacebar
      }

      const keyGeo = new THREE.BoxGeometry(keyW, 0.32, keyD);
      const keyMesh = new THREE.Mesh(keyGeo, keyMatDefault.clone());
      const posX = startX + c * (rowConfig.width + rowConfig.gap);
      const posZ = rowConfig.z;

      keyMesh.position.set(posX, 0.18, posZ);
      keyMesh.castShadow = true;
      keyMesh.receiveShadow = true;

      // Key underside glow disc
      const underGlowGeo = new THREE.PlaneGeometry(keyW * 0.9, keyD * 0.9);
      const underGlowMat = new THREE.MeshBasicMaterial({
        color: 0x38bdf8,
        transparent: true,
        opacity: 0.45,
        side: THREE.DoubleSide
      });
      const underGlow = new THREE.Mesh(underGlowGeo, underGlowMat);
      underGlow.rotation.x = -Math.PI / 2;
      underGlow.position.y = -0.15;
      keyMesh.add(underGlow);

      // Interactive animation metadata
      keyMesh.userData = {
        homeY: 0.18,
        currentY: 0.18,
        targetY: 0.18,
        underGlowMat: underGlowMat,
        baseOpacity: 0.45,
        flashTimer: 0,
        row: rowIndex,
        col: c
      };

      laptopGroup.add(keyMesh);
      keyMeshList.push(keyMesh);
    }
  });

  // Function to depress a key and trigger dynamic cyber illumination
  function pressKey(key, intensity = 1.0) {
    if (!key) return;
    key.userData.targetY = key.userData.homeY - 0.22 * intensity;
    key.material.emissive.setHex(0x38bdf8);
    key.material.emissiveIntensity = 2.4 * intensity;
    key.userData.underGlowMat.opacity = 1.0;
    key.userData.flashTimer = 1.0;
  }

  // -----------------------------------------------------------------
  // 7. 3D STYLIZED CYBER HANDS (TACTILE TYPING PRESENCE)
  // -----------------------------------------------------------------
  const handsGroup = new THREE.Group();
  laptopGroup.add(handsGroup);

  function createStylizedHand(isRight = false) {
    const hand = new THREE.Group();
    const handMat = new THREE.MeshStandardMaterial({
      color: 0x0f1c2e,
      roughness: 0.45,
      metalness: 0.75,
      transparent: true,
      opacity: 0.88
    });

    // Palm / Hand Base
    const palmGeo = new THREE.BoxGeometry(3.6, 0.7, 4.2);
    const palm = new THREE.Mesh(palmGeo, handMat);
    palm.position.set(0, 1.4, 1.6);
    palm.rotation.x = -0.22;
    hand.add(palm);

    // Glowing Holographic Fingertips (4 typing fingers)
    const fingers = [];
    const fingerOffsets = [-1.3, -0.45, 0.45, 1.3];

    fingerOffsets.forEach((xOffset, fIdx) => {
      const fingerGroup = new THREE.Group();
      fingerGroup.position.set(xOffset, 1.2, 0.2);

      // Phalanx segment
      const phalGeo = new THREE.BoxGeometry(0.5, 0.45, 2.2);
      const phal = new THREE.Mesh(phalGeo, handMat);
      phal.position.set(0, -0.1, -1.0);
      phal.rotation.x = 0.35;
      fingerGroup.add(phal);

      // Glowing Fingertip Node (where cyber spark connects to keys)
      const tipGeo = new THREE.SphereGeometry(0.32, 16, 16);
      const tipMat = new THREE.MeshBasicMaterial({
        color: 0x89e3f5,
        transparent: true,
        opacity: 0.95
      });
      const tip = new THREE.Mesh(tipGeo, tipMat);
      tip.position.set(0, -0.45, -2.1);
      fingerGroup.add(tip);

      // Pulsing contact energy ring
      const contactRingGeo = new THREE.RingGeometry(0.2, 0.45, 16);
      const contactRingMat = new THREE.MeshBasicMaterial({
        color: 0x38bdf8,
        transparent: true,
        opacity: 0.0,
        side: THREE.DoubleSide
      });
      const contactRing = new THREE.Mesh(contactRingGeo, contactRingMat);
      contactRing.rotation.x = -Math.PI / 2;
      contactRing.position.set(0, -0.7, -2.1);
      fingerGroup.add(contactRing);

      fingerGroup.userData = {
        baseY: fingerGroup.position.y,
        tipY: tip.position.y,
        contactRingMat: contactRingMat,
        strikePhase: Math.random() * Math.PI * 2,
        speed: 3.5 + Math.random() * 2.5
      };

      hand.add(fingerGroup);
      fingers.push(fingerGroup);
    });

    hand.userData = { fingers: fingers };
    return hand;
  }

  // Left Hand positioned over ASDF region
  const leftHand = createStylizedHand(false);
  leftHand.position.set(-5.2, 0.4, 1.2);
  leftHand.rotation.y = 0.14;
  leftHand.rotation.z = -0.08;
  handsGroup.add(leftHand);

  // Right Hand positioned over JKL; region
  const rightHand = createStylizedHand(true);
  rightHand.position.set(5.2, 0.4, 1.2);
  rightHand.rotation.y = -0.14;
  rightHand.rotation.z = 0.08;
  handsGroup.add(rightHand);

  // -----------------------------------------------------------------
  // 8. 3D NEURAL CONSTELLATION GRAPH (CYBER SYNAPSE NETWORK)
  // -----------------------------------------------------------------
  const nodeCount = 130;
  const nodePositions = [];
  const nodeVelocities = [];
  const nodeOriginals = [];
  const nodePulses = [];

  // Generate constellation nodes hovering above the keyboard in 3D volume
  for (let i = 0; i < nodeCount; i++) {
    // Clustered more densely in center and floating upward
    const x = (Math.random() - 0.5) * 24;
    const y = 2.0 + Math.random() * 12.0;
    const z = -6.0 + (Math.random() - 0.5) * 16;

    nodePositions.push(new THREE.Vector3(x, y, z));
    nodeOriginals.push(new THREE.Vector3(x, y, z));
    nodeVelocities.push(
      new THREE.Vector3(
        (Math.random() - 0.5) * 0.008,
        (Math.random() - 0.5) * 0.008,
        (Math.random() - 0.5) * 0.008
      )
    );
    nodePulses.push(Math.random() * Math.PI * 2);
  }

  // Node Points Geometry & Material with Cyan Glow Sprite
  const nodeGeo = new THREE.BufferGeometry();
  const nodePosAttr = new Float32Array(nodeCount * 3);
  const nodeColorAttr = new Float32Array(nodeCount * 3);

  for (let i = 0; i < nodeCount; i++) {
    nodePosAttr[i * 3] = nodePositions[i].x;
    nodePosAttr[i * 3 + 1] = nodePositions[i].y;
    nodePosAttr[i * 3 + 2] = nodePositions[i].z;

    // Gradient of ice-blue to cyan to white
    const ratio = Math.random();
    if (ratio > 0.8) {
      nodeColorAttr[i * 3] = 1.0;
      nodeColorAttr[i * 3 + 1] = 1.0;
      nodeColorAttr[i * 3 + 2] = 1.0; // Crisp White
    } else if (ratio > 0.4) {
      nodeColorAttr[i * 3] = 0.54;
      nodeColorAttr[i * 3 + 1] = 0.89;
      nodeColorAttr[i * 3 + 2] = 0.96; // Ice Blue #89E3F5
    } else {
      nodeColorAttr[i * 3] = 0.22;
      nodeColorAttr[i * 3 + 1] = 0.74;
      nodeColorAttr[i * 3 + 2] = 0.97; // Cyan #38BDF8
    }
  }

  nodeGeo.setAttribute('position', new THREE.BufferAttribute(nodePosAttr, 3));
  nodeGeo.setAttribute('color', new THREE.BufferAttribute(nodeColorAttr, 3));

  const nodeMat = new THREE.PointsMaterial({
    size: 1.1,
    map: cyanGlowTexture,
    vertexColors: true,
    transparent: true,
    opacity: 0.95,
    blending: THREE.AdditiveBlending,
    depthWrite: false
  });

  const nodePoints = new THREE.Points(nodeGeo, nodeMat);
  neuralGroup.add(nodePoints);

  // Synaptic Connecting Lines (Lines between close nodes)
  const maxConnections = 450;
  const linePositions = new Float32Array(maxConnections * 2 * 3);
  const lineColors = new Float32Array(maxConnections * 2 * 3);
  const lineGeo = new THREE.BufferGeometry();
  lineGeo.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
  lineGeo.setAttribute('color', new THREE.BufferAttribute(lineColors, 3));

  const lineMat = new THREE.LineBasicMaterial({
    vertexColors: true,
    transparent: true,
    opacity: 0.7,
    blending: THREE.AdditiveBlending,
    depthWrite: false
  });

  const lineMesh = new THREE.LineSegments(lineGeo, lineMat);
  neuralGroup.add(lineMesh);

  // Synaptic Energy Packets (Electric data impulses shooting along lines)
  const pulseCount = 30;
  const pulses = [];
  const pulseGeo = new THREE.SphereGeometry(0.18, 12, 12);
  const pulseMat = new THREE.MeshBasicMaterial({
    color: 0xffffff,
    transparent: true,
    opacity: 1.0
  });

  for (let p = 0; p < pulseCount; p++) {
    const pMesh = new THREE.Mesh(pulseGeo, pulseMat);
    pMesh.userData = {
      fromIndex: Math.floor(Math.random() * nodeCount),
      toIndex: Math.floor(Math.random() * nodeCount),
      progress: Math.random(),
      speed: 0.015 + Math.random() * 0.02
    };
    neuralGroup.add(pMesh);
    pulses.push(pMesh);
  }

  // -----------------------------------------------------------------
  // 9. CINEMATIC BOKEH LIGHT DISCS (WARM AMBER & ICE BLUE FROM PHOTO)
  // -----------------------------------------------------------------
  const bokehCount = 28;
  const bokehSprites = [];

  for (let b = 0; b < bokehCount; b++) {
    const isAmber = b % 3 === 0; // Warm amber accents matching photo
    const map = isAmber ? warmAmberGlowTexture : blueBokehTexture;
    const color = isAmber ? 0xf59e0b : 0x38bdf8;
    const size = isAmber ? 4.5 + Math.random() * 6.5 : 2.5 + Math.random() * 4.0;

    const bMat = new THREE.SpriteMaterial({
      map: map,
      color: color,
      transparent: true,
      opacity: isAmber ? 0.35 + Math.random() * 0.3 : 0.25 + Math.random() * 0.35,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });

    const sprite = new THREE.Sprite(bMat);
    sprite.scale.set(size, size, 1);

    // Positioned across foreground and background for deep photographic blur
    const bx = (Math.random() - 0.5) * 34;
    const by = 1.0 + Math.random() * 16;
    const bz = b % 2 === 0 ? 10 + Math.random() * 8 : -8 - Math.random() * 8;

    sprite.position.set(bx, by, bz);
    sprite.userData = {
      baseY: by,
      floatSpeed: 0.6 + Math.random() * 1.2,
      phase: Math.random() * Math.PI * 2,
      baseOpacity: bMat.opacity
    };

    bokehGroup.add(sprite);
    bokehSprites.push(sprite);
  }

  // -----------------------------------------------------------------
  // 10. HOTSPOT 3D TRACKING
  // -----------------------------------------------------------------
  const hotspots = [
    {
      id: 'hotspot-1',
      worldPos: new THREE.Vector3(0, 7.5, 0), // Centered in Neural Mesh
      title: '✦ 3D Neural Constellation',
      desc: 'Deep synaptic graph connecting autonomous AI agents, LLM pipelines, and cognitive models.'
    },
    {
      id: 'hotspot-2',
      worldPos: new THREE.Vector3(-4.5, 0.5, 1.5), // Positioned on Illuminated Keyboard
      title: '⚡ Interactive Tactile Keybed',
      desc: 'Dynamic backlit keyboard architecture reacting in real-time to keystrokes and user events.'
    },
    {
      id: 'hotspot-3',
      worldPos: new THREE.Vector3(0, 5.8, -6.8), // Positioned on Cloud Uplink Screen
      title: '☁ Edge Cloud Distributed Sync',
      desc: 'Ultra-low latency microservices streaming live enterprise data across global clusters.'
    }
  ];

  function updateHotspotPositions() {
    const halfWidth = (container.clientWidth || 600) / 2;
    const halfHeight = (container.clientHeight || 540) / 2;

    hotspots.forEach((hs) => {
      const el = document.getElementById(hs.id);
      if (!el) return;

      const wp = hs.worldPos.clone();
      wp.applyMatrix4(mainGroup.matrixWorld);
      wp.project(camera);

      // Check if in front of camera
      if (wp.z > 1) {
        el.style.display = 'none';
        return;
      }
      el.style.display = 'flex';

      const screenX = wp.x * halfWidth + halfWidth;
      const screenY = -(wp.y * halfHeight) + halfHeight;
      el.style.left = `${screenX}px`;
      el.style.top = `${screenY}px`;
    });
  }

  // -----------------------------------------------------------------
  // 11. SCROLL REACTIVITY (SILKY & SMOOTH)
  // -----------------------------------------------------------------
  let currentScroll = 0;
  let targetScrollY = 0;

  window.update3dScroll = function (scroll, velocity) {
    currentScroll = scroll || 0;
    // Elegant subtle 3D translation with zero scroll resistance
    targetScrollY = -Math.min(currentScroll * 0.008, 4.5);
  };

  // -----------------------------------------------------------------
  // 12. INTERACTION CONTROLS (ROTATION, BOKEH LIGHTING, TYPE PULSE)
  // -----------------------------------------------------------------
  let mouseX = 0;
  let mouseY = 0;
  let isAutoRotate = true;
  let isDragging = false;
  let previousMouseX = 0;

  window.addEventListener('mousemove', (e) => {
    const rect = container.getBoundingClientRect();
    if (
      e.clientX >= rect.left &&
      e.clientX <= rect.right &&
      e.clientY >= rect.top &&
      e.clientY <= rect.bottom
    ) {
      const nx = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      const ny = -(((e.clientY - rect.top) / rect.height) * 2 - 1);
      if (!isDragging) {
        mouseX = nx;
        mouseY = ny;
      }
    }
  });

  container.addEventListener('mousedown', (e) => {
    isDragging = true;
    previousMouseX = e.clientX;
    isAutoRotate = false;
    updateCtrlButtonState();
  });

  window.addEventListener('mouseup', () => {
    isDragging = false;
  });

  window.addEventListener('mousemove', (e) => {
    if (isDragging) {
      const deltaX = e.clientX - previousMouseX;
      mainGroup.rotation.y += deltaX * 0.008;
      previousMouseX = e.clientX;
    }
  });

  // Interactive Typing Ripple Burst
  function triggerTypeBurst() {
    // Strike 5 random keys in rapid succession
    for (let i = 0; i < 5; i++) {
      setTimeout(() => {
        const randKey = keyMeshList[Math.floor(Math.random() * keyMeshList.length)];
        pressKey(randKey, 1.2);
      }, i * 75);
    }

    // Energize all synaptic pulses
    pulses.forEach((p) => {
      p.userData.speed *= 2.2;
      setTimeout(() => {
        p.userData.speed /= 2.2;
      }, 800);
    });

    // Flash screen display line
    renderDisplayContent();

    // Sound effect
    if (window.playSfx) {
      window.playSfx('click');
    }
  }

  // Click on container triggers typing burst
  container.addEventListener('click', (e) => {
    // Avoid clicking on overlay buttons
    if (e.target.closest('.ctrl-btn') || e.target.closest('.hotspot-badge') || e.target.closest('.hotspot-info-card')) {
      return;
    }
    triggerTypeBurst();
  });

  const btnAutoRotate = document.getElementById('btn-3d-rotate');
  const btnReset = document.getElementById('btn-3d-reset');
  const btnLighting = document.getElementById('btn-3d-lighting');
  const btnType = document.getElementById('btn-3d-type');

  function updateCtrlButtonState() {
    if (btnAutoRotate) {
      if (isAutoRotate) {
        btnAutoRotate.classList.add('active');
        btnAutoRotate.innerHTML = '<span>🔄 Rotating</span>';
      } else {
        btnAutoRotate.classList.remove('active');
        btnAutoRotate.innerHTML = '<span>⏸ Paused</span>';
      }
    }
  }

  if (btnAutoRotate) {
    btnAutoRotate.addEventListener('click', () => {
      isAutoRotate = !isAutoRotate;
      updateCtrlButtonState();
    });
  }

  if (btnReset) {
    btnReset.addEventListener('click', () => {
      mainGroup.rotation.y = 0;
      mainGroup.rotation.x = 0;
      camera.position.set(0, 13, 23);
      camera.lookAt(0, 2, -2);
      isAutoRotate = true;
      updateCtrlButtonState();
      closeHotspotCard();
    });
  }

  let isAmberMode = true;
  if (btnLighting) {
    btnLighting.addEventListener('click', () => {
      isAmberMode = !isAmberMode;
      if (isAmberMode) {
        btnLighting.classList.remove('active');
        btnLighting.innerHTML = '<span>💡 Amber Dusk</span>';
        warmBackLight.intensity = 3.8;
        warmBackLight.color.setHex(0xf59e0b);
        dirLight.color.setHex(0x89e3f5);
        scene.fog.color.setHex(0x090e18);
      } else {
        btnLighting.classList.add('active');
        btnLighting.innerHTML = '<span>⚡ Cyber Neon</span>';
        warmBackLight.intensity = 5.0;
        warmBackLight.color.setHex(0x00f0ff);
        dirLight.color.setHex(0x0284c7);
        scene.fog.color.setHex(0x040812);
      }
      if (window.playSfx) window.playSfx('hover');
    });
  }

  if (btnType) {
    btnType.addEventListener('click', () => {
      triggerTypeBurst();
    });
  }

  window.openHotspotDetails = function (index) {
    const hs = hotspots[index];
    if (!hs) return;
    const card = document.getElementById('hotspot-info-card');
    const titleEl = document.getElementById('hotspot-card-title');
    const descEl = document.getElementById('hotspot-card-desc');
    if (card && titleEl && descEl) {
      titleEl.textContent = hs.title;
      descEl.textContent = hs.desc;
      card.style.display = 'flex';
    }
    if (window.playSfx) window.playSfx('click');
  };

  window.closeHotspotCard = function () {
    const card = document.getElementById('hotspot-info-card');
    if (card) card.style.display = 'none';
  };

  // -----------------------------------------------------------------
  // 13. ANIMATION LOOP
  // -----------------------------------------------------------------
  const clock = new THREE.Clock();
  let typingClock = 0;

  function animate() {
    requestAnimationFrame(animate);

    const delta = clock.getDelta();
    const elapsedTime = clock.getElapsedTime();
    typingClock += delta;

    // 1. Auto Rotate Scene
    if (isAutoRotate && !isDragging) {
      mainGroup.rotation.y += 0.0028;
    }

    // 2. Smooth Scroll Translation
    mainGroup.position.y += (targetScrollY - mainGroup.position.y) * 0.08;

    // 3. Automated Cyber Typing Cadence (Typing 3-4 keys per second)
    if (typingClock > 0.28) {
      typingClock = 0;
      const randomKey = keyMeshList[Math.floor(Math.random() * keyMeshList.length)];
      pressKey(randomKey, 0.85 + Math.random() * 0.3);
    }

    // 4. Update Keycap Animations (Return to homeY and decay glow)
    keyMeshList.forEach((k) => {
      // Spring return
      k.position.y += (k.userData.targetY - k.position.y) * 0.35;
      k.userData.targetY += (k.userData.homeY - k.userData.targetY) * 0.2;

      // Decay flash
      if (k.userData.flashTimer > 0) {
        k.userData.flashTimer -= delta * 3.5;
        if (k.userData.flashTimer <= 0) {
          k.userData.flashTimer = 0;
          k.material.emissive.setHex(0x000000);
          k.userData.underGlowMat.opacity = k.userData.baseOpacity;
        } else {
          k.userData.underGlowMat.opacity = k.userData.baseOpacity + k.userData.flashTimer * 0.55;
        }
      }
    });

    // 5. Stylized Hands Typing Motion
    [leftHand, rightHand].forEach((hand, hIdx) => {
      const fingers = hand.userData.fingers;
      fingers.forEach((f, fIdx) => {
        const u = f.userData;
        u.strikePhase += delta * u.speed;
        const tap = Math.sin(u.strikePhase);
        // Fingertip moves gently down and touches key
        f.position.y = u.baseY + (tap < -0.2 ? tap * 0.35 : 0);

        // Contact ring pulses when finger touches key
        if (tap < -0.85) {
          u.contactRingMat.opacity = Math.min(u.contactRingMat.opacity + 0.3, 0.85);
        } else {
          u.contactRingMat.opacity *= 0.88;
        }
      });
      // Hand gentle natural breathing
      hand.position.y = 0.4 + Math.sin(elapsedTime * 2.0 + hIdx) * 0.06;
    });

    // 6. Animate Neural Constellation Nodes & Connecting Synapses
    let connectionIdx = 0;
    const connectThreshold = 4.2;

    for (let i = 0; i < nodeCount; i++) {
      // Node micro-drift
      nodePositions[i].x += Math.sin(elapsedTime * 1.5 + nodePulses[i]) * 0.008;
      nodePositions[i].y += Math.cos(elapsedTime * 1.2 + nodePulses[i]) * 0.008;

      nodePosAttr[i * 3] = nodePositions[i].x;
      nodePosAttr[i * 3 + 1] = nodePositions[i].y;
      nodePosAttr[i * 3 + 2] = nodePositions[i].z;

      // Find nearby nodes to connect with synaptic lines
      for (let j = i + 1; j < nodeCount; j++) {
        const dist = nodePositions[i].distanceTo(nodePositions[j]);
        if (dist < connectThreshold && connectionIdx < maxConnections) {
          const alpha = 1.0 - dist / connectThreshold;

          // Vertex 1
          linePositions[connectionIdx * 6] = nodePositions[i].x;
          linePositions[connectionIdx * 6 + 1] = nodePositions[i].y;
          linePositions[connectionIdx * 6 + 2] = nodePositions[i].z;
          lineColors[connectionIdx * 6] = 0.22 * alpha;
          lineColors[connectionIdx * 6 + 1] = 0.74 * alpha;
          lineColors[connectionIdx * 6 + 2] = 0.97 * alpha;

          // Vertex 2
          linePositions[connectionIdx * 6 + 3] = nodePositions[j].x;
          linePositions[connectionIdx * 6 + 4] = nodePositions[j].y;
          linePositions[connectionIdx * 6 + 5] = nodePositions[j].z;
          lineColors[connectionIdx * 6 + 3] = 0.22 * alpha;
          lineColors[connectionIdx * 6 + 4] = 0.74 * alpha;
          lineColors[connectionIdx * 6 + 5] = 0.97 * alpha;

          connectionIdx++;
        }
      }
    }

    nodeGeo.attributes.position.needsUpdate = true;

    // Clear unused line segments
    for (let k = connectionIdx; k < maxConnections; k++) {
      linePositions[k * 6] = 0;
      linePositions[k * 6 + 1] = 0;
      linePositions[k * 6 + 2] = 0;
      linePositions[k * 6 + 3] = 0;
      linePositions[k * 6 + 4] = 0;
      linePositions[k * 6 + 5] = 0;
    }
    lineGeo.attributes.position.needsUpdate = true;
    lineGeo.attributes.color.needsUpdate = true;

    // 7. Animate Synaptic Pulses (Data Packets)
    pulses.forEach((p) => {
      const u = p.userData;
      u.progress += u.speed;
      if (u.progress >= 1.0) {
        u.progress = 0;
        u.fromIndex = u.toIndex;
        u.toIndex = Math.floor(Math.random() * nodeCount);
      }
      const p1 = nodePositions[u.fromIndex];
      const p2 = nodePositions[u.toIndex];
      p.position.lerpVectors(p1, p2, u.progress);
    });

    // 8. Animate Floating Bokeh Discs
    bokehSprites.forEach((sp) => {
      const u = sp.userData;
      sp.position.y = u.baseY + Math.sin(elapsedTime * u.floatSpeed + u.phase) * 0.9;
      sp.position.x += Math.cos(elapsedTime * 0.5 + u.phase) * 0.008;
    });

    // 9. Camera Parallax Lerp
    if (!isDragging) {
      camera.position.x += (mouseX * 4.5 - camera.position.x) * 0.05;
      camera.position.y += (13 + mouseY * 3.0 - camera.position.y) * 0.05;
      camera.lookAt(0, 2, -2);
    }

    renderer.render(scene, camera);
    updateHotspotPositions();
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
