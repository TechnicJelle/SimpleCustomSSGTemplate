import os
from shutil import copytree

import markdown

# == Copy static files to the build directory ==
copytree("static/", "build/", dirs_exist_ok=True)

# == Load the template ==
template: str
with open("templates/index.html") as file:
	template = file.read()

# == Loop over all content files ==
for post in os.listdir("content"):
	# == Load the content of the post ==
	content: str
	with open("content/" + post) as file:
		content = file.read()

	# == Convert the markdown to HTML ==
	html = markdown.markdown(content)

	# == Insert the HTML content into the template ==
	output: str = template.replace("{{content}}", html)

	# == Write the output to the build directory ==
	with open("build/" + post.replace(".md", ".html"), "w") as file:
		file.write(output)
