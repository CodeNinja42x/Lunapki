// Set up the scene, camera, and renderer
var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
var renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('cosmic-scene').appendChild(renderer.domElement);

// Create a sphere (planet)
var geometry = new THREE.SphereGeometry(1, 32, 32);
var material = new THREE.MeshBasicMaterial({ color: 0x00b7eb });
var sphere = new THREE.Mesh(geometry, material);
scene.add(sphere);

// Set the camera position
camera.position.z = 5;

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    sphere.rotation.x += 0.01;
    sphere.rotation.y += 0.01;
    renderer.render(scene, camera);
}

animate();
