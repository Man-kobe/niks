import os

# Function to create a new directory
def create_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Directory '{path}' created successfully")
    except Exception as e:
        print(f"Failed to create directory '{path}': {e}")

# Function to list files in a directory
def list_files(path):
    try:
        files = os.listdir(path)
        print(f"Files in '{path}': {files}")
    except Exception as e:
        print(f"Failed to list files in '{path}': {e}")

# Function to delete a file
def delete_file(path):
    try:
        os.remove(path)
        print(f"File '{path}' deleted successfully")
    except Exception as e:
        print(f"Failed to delete file '{path}': {e}")

# Example usage
if __name__ == "__main__":
    dir_path = "./new_directory"
    file_path = "./new_directory/sample.txt"

    # Create a new directory
    create_directory(dir_path)

    # List files in the new directory
    list_files(dir_path)

    # Create a sample file in the new directory
    with open(file_path, "w") as f:
        f.write("This is a sample file.")

    # List files again to see the new file
    list_files(dir_path)

    # Delete the sample file
    delete_file(file_path)

    # List files again to see the updated directory
    list_files(dir_path)