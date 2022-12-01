# Clients
<script src="gallery.js" type=module></script>
<link rel="stylesheet" href="styles/gallery.css">

<script>
let galleries = {{ site.data.discography | jsonify }};
window.client_listing = true;
</script>

<p>Click on any project below for details and gallery view or for a full visual discography, <a href="discography.html">click here</a>.</p>

<div id=gallery></div>

{% for year in site.data.discography %}
  {% for project in year[1] %}
  <script type="application/ld+json">
{
  "@context" : "https://schema.org",
  "@type": "MusicGroup",
  "name" : "{{ project.artist }}"
}
</script>
  {% endfor %}
{% endfor %}
