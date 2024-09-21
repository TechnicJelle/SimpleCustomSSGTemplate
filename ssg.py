import os
from shutil import copytree
from urllib.parse import urlsplit, urlunsplit
from xml.etree.ElementTree import Element

import markdown
from markdown import Extension, Markdown
from markdown.treeprocessors import Treeprocessor

# From https://github.com/venthur/blag/blob/0c606c7673695b1622e0588cac2fe400e88a586f/blag/markdown.py#L93-L133
class LinkFixerFunc(Treeprocessor):
	def run(self, root: Element) -> Element:
		for element in root.iter():
			if element.tag == "a":
				url = str(element.get("href"))
				converted = self.convert(url)
				element.set("href", converted)
		return root

	@staticmethod
	def convert(url):
		scheme, netloc, path, query, fragment = urlsplit(url)
		if scheme or netloc or not path:
			return url
		if path.endswith(".md"):
			path = path[:-3] + ".html"
		url = urlunsplit((scheme, netloc, path, query, fragment))
		return url


class LinkFixerExt(Extension):
	def extendMarkdown(self, md: Markdown) -> None:
		md.treeprocessors.register(LinkFixerFunc(md), "mdlink", 0)


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
	html = markdown.markdown(content, extensions=[LinkFixerExt()])

	# == Insert the HTML content into the template ==
	output: str = template.replace("{{content}}", html)

	# == Write the output to the build directory ==
	with open("build/" + post.replace(".md", ".html"), "w") as file:
		file.write(output)
