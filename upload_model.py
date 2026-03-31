from opengradient.client.model_hub import ModelHub

print("=== Uploading to OpenGradient Model Hub ===")

email = input("Enter OG email: ")
password = input("Enter OG password: ")

hub = ModelHub(email=email, password=password)

repo = hub.create_model(
    model_name="truthlayer-ai",
    model_desc="AI Trust Score verifier"
)

with open("truthlayer.txt", "w") as f:
    f.write("TruthLayer AI Trust Score Model")

hub.upload("truthlayer.txt", repo.name, repo.version)

print("\n✅ Uploaded to OpenGradient Model Hub!")