# Markdown-based Website

## will run using Jekyll
[notes](https://github.com/gsarchive/markdown/blob/master/README.md)

Files in this repository are considered authoritative. The corresponding HTML
files will be rebuilt as needed, and should not be manually edited. Any file
in the main web site directory which does NOT have a corresponding Markdown
file here is its own entity and is authoritative.

To build and test locally:

* Install Ruby
* `gem install bundler`
* `bundle install` (or `bundle install --path vendor/bundle`)
* `bundle exec jekyll serve`

It should auto-detect changes to Markdown or layout files.
