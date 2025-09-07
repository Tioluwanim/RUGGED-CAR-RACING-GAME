import os


def generate_readme(project_path, readme_name="README.md"):
    readme_path = os.path.join(project_path, readme_name)

    # Collect basic info about files in the project
    file_summary = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file != readme_name:  # Avoid including the README itself
                file_summary.append(os.path.relpath(
                    os.path.join(root, file), project_path))

    # Write README content
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("# Project Overview\n\n")
        f.write("This project was auto-scanned and a README was generated.\n\n")

        f.write("## File Structure\n")
        f.write("```\n")
        for file in file_summary:
            f.write(file + "\n")
        f.write("```\n\n")

        f.write("## Usage\n")
        f.write("Describe how to run the project here.\n\n")

        f.write("## Requirements\n")
        f.write("List dependencies here (e.g., from requirements.txt).\n\n")

    print(f"README.md created at: {readme_path}")


# Example usage:
if __name__ == "__main__":
    project_directory = os.getcwd()  # current project folder
    generate_readme(project_directory)
