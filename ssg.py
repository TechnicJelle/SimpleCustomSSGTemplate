from shutil import copytree

import markdown

# == Copy static files to the build directory ==
copytree("static/", "build/", dirs_exist_ok=True)

# == Load the template and content ==
template: str
content: str

with open("templates/index.html") as file:
	template = file.read()

with open("content/index.md") as file:
	content = file.read()

# == Convert the markdown to HTML ==
html = markdown.markdown(content)

# == Insert the HTML content into the template ==
output: str = template.replace("{{content}}", html)

# == Write the output to the build directory ==
with open("build/index.html", "w") as file:
	file.write(output)
