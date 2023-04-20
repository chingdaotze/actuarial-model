# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from os.path import abspath

project_dir = abspath(
	r'../..'
)

print(
	f'Setting Project Dir: {project_dir}'
)

sys.path.append(
	project_dir
)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

master_doc = 'index'
project = 'actuarial-model'
copyright = '2023, Michael Ching'
author = 'Michael Ching'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
	'sphinx.ext.autodoc',
	'sphinx.ext.autosummary',
	'sphinx_toolbox.collapse',
	'sphinx.ext.graphviz',
	'sphinx.ext.inheritance_diagram'
]
autosummary_generate = True
templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_material'
html_title = 'Actuarial Model'
html_static_path = ['_static']
html_logo = 'images/mu_logo.png'
html_favicon = 'images/mu_favicon.png'
html_theme_options = {
	'nav_title': 'Actuarial Model',
	'repo_url': 'https://github.com/chingdaotze/actuarial-model',
	'repo_type': 'github',
	'repo_name': 'actuarial-model',
	'base_url': 'https://actuarial-model.readthedocs.io/en/latest/',
	'globaltoc_depth': -1,
	'globaltoc_collapse': True,
	'globaltoc_includehidden': True,
	'color_primary': 'deep-purple',
	'color_accent': 'deep-purple',
	'master_doc': False,
	'nav_links': [
		{
			'href': 'index',
			'title': 'Home',
			'internal': True
		},
		{
			'href': 'tutorial_pt1',
			'title': 'Tutorial',
			'internal': True
		},
		{
			'href': 'system_doc',
			'title': 'API',
			'internal': True
		},
		{
			'href': 'about_me',
			'title': 'About Me',
			'internal': True
		}
	],
	# 'heroes': {
	# 	'index': 'Home'
	# }
}
html_sidebars = {
	'**': [
		'logo-text.html',
		'globaltoc.html',
		'localtoc.html',
		'searchbox.html'
	]
}
