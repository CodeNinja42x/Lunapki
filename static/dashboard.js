import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.140.0/build/three.module.js';

// Create scene
const scene = new THREE.Scene();

// Create camera
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

// Create renderer
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('cosmic-scene').appendChild(renderer.domElement);

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

// Function to fetch real-time data
async function fetchRealTimeData() {
    try {
        const response = await fetch('/api/realtime_data');
        const data = await response.json();
        console.log('Real-time data:', data);

        // Update the 3D scene color based on real-time data
        const newColor = new THREE.Color(`hsl(${Math.floor(data.value)}, 100%, 50%)`);
        sphere.material.color.set(newColor);

        // Display the real-time data value
        document.getElementById('data-value').textContent = data.value.toFixed(2);

    } catch (error) {
        console.error('Error fetching real-time data:', error);
    }
}

// Fetch real-time data every 2 seconds
setInterval(fetchRealTimeData, 2000);

// Fetch Binance data
async function fetchBinanceData() {
    try {
        const response = await fetch('/api/binance_data');
        const data = await response.json();
        console.log('Binance data:', data);

        // Update the 3D scene based on Binance data
        const price = parseFloat(data.price);
        const newColor = new THREE.Color(`hsl(${Math.floor(price % 360)}, 100%, 50%)`);
        sphere.material.color.set(newColor);

        // Display the Binance data value
        document.getElementById('data-value').textContent = `BTC Price: $${price.toFixed(2)}`;

    } catch (error) {
        console.error('Error fetching Binance data:', error);
    }
}

// Fetch Binance data every 2 seconds
setInterval(fetchBinanceData, 2000);
