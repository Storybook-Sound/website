# Clients
<script src="gallery.js" type=module></script>
<link rel="stylesheet" href="styles/gallery.css">

<script>
let galleries = {{ site.data.discography | jsonify }};
window.client_listing = true;
</script>
<div id=gallery></div>
