# Hello, music.
<script src="gallery.js" type=module></script>
<link rel="stylesheet" href="styles/gallery.css">

<script>const gallery = {{ site.data.discography | jsonify }};</script>
<div id=gallery></div>
