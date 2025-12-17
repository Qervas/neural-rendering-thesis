# Neural Rendering Dataset Collection

**Master's Thesis** | Linköping University | 2025

**Author:** Shaoxuan Yin

**Supervisor:** Sergey Ignatenko

**Examiner:** Jonas Unger

**Programme:** Computer Science, Master's Programme (6MICS)

**Course:** TQDV30 - Degree Project (30 hp)

---

## Abstract

This thesis investigates multi-view capture systems for neural rendering, comparing traditional photogrammetry with modern neural rendering methods (NeRF and 3D Gaussian Splatting). Two datasets were created: a controlled studio dataset of 10 objects with 432 images each, and a large-scale outdoor dataset of Gränsö Castle with 5,262 images. The work addresses how neural rendering handles view-dependent effects (reflections, transparency) and examines scalability limits for large scenes.

---

## Download

| Resource | Link |
|----------|------|
| **Thesis PDF** | [Download](Neural_Rendering_Dataset_Collection.pdf) |
| **Capture Software** | [CamMatrixCapture](https://github.com/Qervas/CamMatrixCapture) |
| **Studio Objects Dataset** | [Internet Archive](https://archive.org/details/captured_objects_dataset) |

---

## Datasets

### Studio Objects Dataset
- 10 objects captured with a 12-camera synchronized rig
- 432 images per object (12 cameras × 36 turntable positions)
- Includes challenging materials: glass, metal, fur, translucent objects
- ArUco marker-based geometric alignment

### Gränsö Castle Dataset
- Large-scale outdoor heritage site
- 5,262 images (drone + SLR photography)
- Multi-scale reconstruction from aerial to ground-level detail

---

## Software

The [CamMatrixCapture](https://github.com/Qervas/CamMatrixCapture) software was developed for this thesis to control the multi-camera capture system. Features include:
- Synchronized capture from 12 Teledyne FLIR cameras
- Parallel image transfer (1.85× speedup)
- Automated turntable control
- Real-time preview and camera configuration

---

## Citation

```bibtex
@mastersthesis{yin2025neural,
  author  = {Yin, Shaoxuan},
  title   = {Neural Rendering Dataset Collection},
  school  = {Linköping University},
  year    = {2025},
  type    = {Master's thesis},
  number  = {LiU-ITN-TEK-A--25/070--SE},
  address = {Norrköping, Sweden}
}
```

---

## License

The thesis document is available for academic and educational purposes.
The dataset is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
