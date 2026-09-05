# AI Model Selection — SecureAttend AI

## Decision (Phase 0)

**Selected Model:** InsightFace `buffalo_sc` via ONNX Runtime  
**Embedding:** 512-dimensional ArcFace embeddings (float32)  
**Status:** Recommended — pending validation during Phase 4 implementation

## Evaluation Criteria

| Criterion | Weight | buffalo_sc | deepface (Facenet512) | face_recognition (dlib) |
|-----------|--------|-----------|----------------------|------------------------|
| CPU performance | High | Good (~200ms/frame) | Moderate (~500ms) | Good (~300ms) |
| Installation reliability | High | Good (pip + onnx) | Moderate (many deps) | Poor (dlib build) |
| Model size | Medium | ~16 MB | ~90 MB | ~100 MB |
| Accuracy (LFW) | High | ~99.5% | ~99.6% | ~99.3% |
| Python ecosystem | High | Good (insightface) | Good (deepface) | Good |
| Licensing | High | MIT (code), model check needed | MIT | MIT |
| Detection included | Medium | Yes (RetinaFace) | Via backend | Via dlib |
| Replaceability | High | Adapter pattern | Adapter pattern | Adapter pattern |

## Rationale

1. **CPU-friendly:** `buffalo_sc` is the smallest InsightFace bundle, suitable for student laptops without GPU.
2. **All-in-one:** Includes face detection (RetinaFace), alignment, and embedding in one pipeline.
3. **ONNX Runtime:** Cross-platform, no CUDA required, reliable pip installation.
4. **512-dim embeddings:** Industry-standard ArcFace dimension, good discrimination for 1:1 verification.
5. **Upgrade path:** Can swap to `buffalo_l` for better accuracy if laptop hardware allows.

## Alternative Considered

### buffalo_l

- Better accuracy (~+0.5% LFW)
- Larger model (~300 MB)
- Slower on CPU (~400ms/frame)
- **Decision:** Use as upgrade option, not default

### deepface + Facenet512

- Higher-level API, easier prototyping
- Heavier dependencies (TensorFlow/Keras options)
- Slower cold start
- **Decision:** Rejected for default due to dependency weight

### face_recognition (dlib)

- Simple API
- dlib compilation issues on Windows
- 128-dim embeddings (lower discrimination)
- **Decision:** Rejected due to installation reliability

## Adapter Interface

```python
class FaceModelAdapter(Protocol):
    name: str
    version: str
    embedding_dim: int

    def detect_faces(self, image: np.ndarray) -> list[FaceDetection]: ...
    def generate_embedding(self, aligned_face: np.ndarray) -> np.ndarray: ...
    def compare(self, embedding_a: np.ndarray, embedding_b: np.ndarray) -> float: ...
```

Implementations:
- `InsightFaceAdapter` (default)
- Future: `BuffaloLAdapter`, `MiniFASNetAdapter`

## Preprocessing Version

Version `1.0`:
1. BGR → RGB conversion
2. Face detection + 5-point landmark alignment
3. Crop to 112×112
4. Normalize: `(pixel - 127.5) / 128.0`
5. L2-normalize output embedding

## Threshold Selection

ArcFace cosine similarity threshold:

| Threshold | Use Case |
|-----------|----------|
| 0.40 | Lenient (more false accepts) |
| 0.45 | **Default recommended** |
| 0.50 | Strict (more false rejects) |

Configurable via Admin system settings. Will be tuned with demo data in Phase 4.

## Installation (Phase 4)

```bash
pip install insightface onnxruntime opencv-python-headless
```

Models auto-download on first use (~16 MB for buffalo_sc).

## Unresolved Questions

1. Exact threshold tuning requires demo enrollment data (Phase 4)
2. InsightFace model license for academic use — verify before publication
3. Windows ONNX Runtime performance vs Linux — benchmark in Phase 4

## References

- InsightFace: https://github.com/deepinsight/insightface
- ArcFace paper: Deng et al., CVPR 2019
- ONNX Runtime: https://onnxruntime.ai/
