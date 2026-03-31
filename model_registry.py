from opengradient.client.model_hub import ModelHub

print("Connecting to OpenGradient Model Hub...")

hub = ModelHub(
    email="YOUR_EMAIL",
    password="YOUR_PASSWORD"
)

print("Creating model...")

model = hub.create_model(
    model_name="verifiable-decision-engine",
    model_desc="A simple verifiable AI decision system with proof layer"
)

print("\nModel Created:")
print(model)

print("\nUploading dummy file...")

# create dummy file first manually: test.txt
hub.upload("test.txt", model.name, "1.00")

print("\nUpload complete ✅")