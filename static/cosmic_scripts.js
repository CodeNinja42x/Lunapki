console.log("Starting 3D scene setup");

// Create scene
const scene = new THREE.Scene();

// Create camera
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

// Create renderer
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('cosmic-scene').appendChild(renderer.domElement);

// Create geometry
const geometry = new THREE.SphereGeometry(1, 32, 32);
const material = new THREE.MeshBasicMaterial({ color: 0x0077ff });
const sphere = new THREE.Mesh(geometry, material);
scene.add(sphere);

// Set camera position
camera.position.z = 5;

// Add OrbitControls
const controls = new OrbitControls(camera, renderer.domElement);

// Render loop
function animate() {
    requestAnimationFrame(animate);

    // Rotate the sphere for some animation
    sphere.rotation.x += 0.01;
    sphere.rotation.y += 0.01;

    controls.update();

    renderer.render(scene, camera);
}

animate();
