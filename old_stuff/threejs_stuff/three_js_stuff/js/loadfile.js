import * as THREE from "three";
// import * as THREE from "../build/three.module.js";

import { Float32BufferAttribute, Material, PointsMaterial, Uint32BufferAttribute, Vector3 } from "three";
import { OrbitControls } from "OrbitControls";

import { position, colors, indices } from "./file.js";
// import { z } from './pgf.js';


const scene = new THREE.Scene();
const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );


const camera = new THREE.PerspectiveCamera( 40, window.innerWidth / window.innerHeight, 0.01, 10000 );
camera.position.set(0, 1200, 0 );
scene.add(camera);

console.log({ colors });


const geommetry = new THREE.BufferGeometry();

let newIndices = [];

for (let i = 0; i < indices.length; i ++) {
    if (i % 2 === 0) { newIndices.push(indices[i]);
                       newIndices.push(indices[i+1]);
                       newIndices.push(indices[i+2]); }
    else { newIndices.push(indices[i+2]);
           newIndices.push(indices[i+1]);
           newIndices.push(indices[i]); }
}

geommetry.setIndex(newIndices);
geommetry.setAttribute('position', new THREE.Float32BufferAttribute(position, 3));
geommetry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3))


// const material = new THREE.PointsMaterial({ vertexColors: true });
// material.vertexColors = geommetry.hasAttribute( 'color' );
// let mesh = new THREE.Points( geommetry, material );
// scene.add(mesh);

// const material = new THREE.LineBasicMaterial({ vertexColors: true });
// let mesh = new THREE.Line( geommetry, material );
// scene.add(mesh);

const material = new THREE.MeshBasicMaterial({ vertexColors: true, side: THREE.DoubleSide });//{ vertexColors: true });
let mesh = new THREE.Mesh( geommetry, material );
scene.add(mesh);

console.log({ geommetry }, { mesh } );

const controls = new OrbitControls( camera, renderer.domElement );
controls.target.set( 700, 1200, 1200 );
controls.update();
controls.enablePan = true;
controls.enableDamping = false;

console.log({ scene })

function animate() {
    requestAnimationFrame( animate );

    renderer.render( scene, camera );
}

animate();
