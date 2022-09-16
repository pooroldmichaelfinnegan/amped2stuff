import * as THREE from 'three';

let posbuf = await fetch('nz1_all_verts')
    .then(response => response.arrayBuffer())
let indbuf = await fetch('nz1_indices_adjusted.hex')
    .then(response => response.arrayBuffer())

// console.log({ posbuf, indbuf });


let position = [];
let colors = [];
let col;
let uv = [];

function rgba2rgb(r, g, b, a) {
    let falpha = a/255;
    // console.log(falpha, r, r*falpha);
    return new THREE.Color(r/255*falpha, g/255*falpha, b/255*falpha);
}
let indices = new Uint32Array(indbuf);

for (let i = 0; i <= posbuf.byteLength-28;) {
    //vertex position
    position.push(...new Float32Array(posbuf, i, 3));
    
    //vertex diffuse color
    let rgba = new Uint8Array(posbuf, i+12, 4);
    col = rgba2rgb(...rgba);
    colors.push(col.r, col.g, col.b);

    //vertex something
    uv.push(...new Float32Array(posbuf, i+16, 3));

    i += 28;
}

export { position, colors, indices };
