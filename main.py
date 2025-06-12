from ultralytics import YOLO

if __name__ == '__main__':
    # Load a pretrained YOLO model (recommended for training)
    model = YOLO("yolov8x.pt")

    # Train the model using the 'coco8.yaml' dataset for 3 epochs
    # Fix Windows DataLoader issue by setting workers=0
    results = model.train(
        data="mydata.yaml",
        epochs=50,
        device='0',
        workers=0,  # Fix for Windows DataLoader issue
        batch=8     # Reduce batch size if memory issues
    )

