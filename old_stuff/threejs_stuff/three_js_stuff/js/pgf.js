import * as THREE from 'three';

let pgf = await fetch('nz1.pgf_model_all')
    .then(resolve => resolve.arrayBuffer())

let pgf_header = {
    vertex_buffer_length: 0,
    index_buffer_length: 0,
    _: 0, _: 0, _: 0, _: 0,
    _: 0, _: 0, _: 0, _: 0,
    vertex_slice_count: 0,
    index_slice_count: 0,
    _: 0, _: 0, _: 0, _: 0
}

const zip = (a, b) => a.map((k, i) => [k, b[i]]);

let i = 0;
let z = zip(pgf_header, new Uint32Array(pgf, i, 16));

export { z };

// for (let i = 0;;) {
//     zip(pgf_header, new Uint32Array(pgf, i, 16));
// }

// var c = a.map(function(e, i) {
//     return [e, b[i]];
// });
