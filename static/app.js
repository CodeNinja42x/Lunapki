// Create scene
const scene = new THREE.Scene();

// Create camera
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

// Create renderer
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);  // Append renderer directly to body

// Create geometry (sphere)
const geometry = new THREE.SphereGeometry(1, 32, 32);
const material = new THREE.MeshBasicMaterial({ color: 0x0077ff });
const sphere = new THREE.Mesh(geometry, material);
scene.add(sphere);

// Set camera position
camera.position.z = 5;

// Render loop
function animate() {
    requestAnimationFrame(animate);
    sphere.rotation.x += 0.01;
    sphere.rotation.y += 0.01;
    renderer.render(scene, camera);
}

animate();

// Resize listener for responsive canvas
window.addEventListener('resize', () => {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
});

// Fetch real-time data
async function fetchRealTimeData() {
    try {
        const response = await fetch('/api/realtime_data');
        const data = await response.json();
        document.getElementById('data-value').textContent = data.value.toFixed(2);
    } catch (error) {
        console.error('Error fetching real-time data:', error);
    }
}

// Fetch data every 2 seconds
setInterval(fetchRealTimeData, 2000);
