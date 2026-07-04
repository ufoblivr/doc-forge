from huggingface_hub import HfApi

api = HfApi()
repo_id = "ufoblivr/docforge-codet5-base-v1"

# Create the repository on your Hugging Face account
api.create_repo(repo_id=repo_id, repo_type="model", exist_ok=True)

# Upload the entire folder
print("Uploading model... this will take a few minutes.")
api.upload_folder(
    folder_path="./docforge-codet5-base-v1",
    repo_id=repo_id,
    repo_type="model",
)
print("Upload complete!")