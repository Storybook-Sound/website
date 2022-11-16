import {choc, set_content, on, DOM, fix_dialogs} from "https://rosuav.github.io/choc/factory.js";
const {DIV, IMG, H1, H2, H3, H4, A, DIALOG, FIGURE, FIGCAPTION, BUTTON, P, SECTION, UL, LI, SPAN, BLOCKQUOTE} = choc; //autoimport

let selected_item = 0;
let selected_set = 0;

if (window.client_listing === true) {
  // Make a new object for text version, client listing
  const artists = {};
  Object.values(galleries).forEach(gallery => gallery.forEach(info => {
    if (artists[info.artist]) {
      artists[info.artist].push(info);
    } else {
      artists[info.artist] = [info]
    }
  }));
  galleries = artists;
}

const sets = Object.keys(galleries);
if (window.client_listing === true) {
  sets.sort((a, b) => a.localeCompare(b)); // normal sort for name
} else {
  sets.sort((a, b) => b.localeCompare(a)); // reverse sort for year
}

document.body.appendChild(DIALOG({id: "gallerydlg"}, [
  DIV({id: "dialog_header"}, [
    DIV([BUTTON({id: "prev"}, "previous"), BUTTON({id: "next"}, "next")]),
    BUTTON({type: "button", class: "dialog_cancel"}, 'x')]),
  FIGURE([
    DIV({class: 'gallery-image'}),
    FIGCAPTION()
  ])
]));

// Support for older browsers
fix_dialogs({close_selector: ".dialog_cancel,.dialog_close", click_outside: "formless"});

function gallery_image(item) {
  return DIV({class: 'gallery-image', style: `background-image: url("${item.image.url}")`, title: item.project + ' ' + item.artist});
}


if (window.client_listing === true) {
  set_content("#gallery", UL(
    sets.map((set, idx) => LI({'data-set': idx},
      [set, SPAN([
        " (",
        galleries[set].map((item, idx) => [
          idx &&
          ", ", item.image ?
            A({href: "#", "data-idx": idx, class: "gallery_entry"}, item.project || item.year)
            : item.project || item.year]),
        ")"])]
        )
      )
    )
  );

} else {
  set_content("#gallery",
    sets.map((set, idx )=> SECTION({'data-set': idx}, [
      H2(set),
      DIV({class: "gallery_set"}, galleries[set].map((item, idx) => item.image && DIV({"data-idx": idx, class: "gallery_entry"}, gallery_image(item)))),
      P(UL(galleries[set].map((item, idx) => !item.image &&
        LI([
          item.artist, ", ", item.project,
          item.roles && " (" + item.roles.join(", ") + ") ",
          item.project_url && A({href: item.project_url['url'], target: "_blank"}, item.project_url['title']),
          item.notes && BLOCKQUOTE(item.notes),
        ]))))
    ]))
  );
}

function display_item(set, idx) {
  selected_item = +idx; // cast as number
  selected_set = +set;
  const item = galleries[sets[set]][idx];
  DOM("#gallerydlg .gallery-image").replaceWith(gallery_image(item));
  set_content("#gallerydlg figcaption", [
    item.project && H1(item.project),
    item.artist && H2(item.artist),,
    item.image.caption && P({style: "width:100%"}, item.image.caption),
    item.roles && H4(item.roles.join(", ")),
    item.notes && item.notes.split("\n\n").map(p => P({".innerHTML": p})),
    // Using .innerHTML is a cheat that Choc Factory makes "work".
    // TODO LINK,
    item.project_url && A({class: "artist-link", href: item.project_url.url, target: "_blank"}, item.project_url.title),
    item.year && H3(item.year),
  ]);
}

on("click", ".gallery_entry", e => {
  e.preventDefault();
  display_item(e.match.closest("[data-set]").dataset.set, e.match.closest("[data-idx]").dataset.idx);
  DOM("#gallerydlg").showModal();
});

on("click", "#prev", e => {
  let set = selected_set, item = selected_item;
  do {
    if (item) --item; else {
      set = set ? set - 1 : sets.length - 1;
      item = galleries[sets[set]].length - 1;
    }
    if (galleries[sets[set]][item].image) break;
  } while (item != selected_item || set !== selected_set);

  display_item(set, item);

});

on("click", "#next", e => {
  let set = selected_set, item = selected_item;
  do {
    if (item < galleries[sets[set]].length - 1) ++item; else {
      set = (set + 1) % sets.length;
      item = 0;
    }
    if (galleries[sets[set]][item].image) break;
  } while (item != selected_item || set !== selected_set);

  display_item(set, item);
});
