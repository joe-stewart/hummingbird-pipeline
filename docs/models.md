# Models

## Active Model
| Field    | Value |
|----------|-------|
| Name     | TBD   |
| Version  | TBD   |
| Source   | TBD   |
| Checksum | TBD   |

## Training Notes
- Do not commit .pt / .onnx / .trt files
- Target: fine-tuned YOLOv8 on hummingbird detections
- Minimum dataset: 200-500 images to validate, 1000-2000 for robust model
- Collect from varied positions/angles/lighting during data collection phase
- Lock camera position for production after training
- Public datasets: iNaturalist hummingbird images useful for augmentation

## Confidence Threshold
- Current: no minimum (all detections saved)
- Baseline not yet established — collecting frames for calibration
- Revisit after accumulating frames across varied conditions
