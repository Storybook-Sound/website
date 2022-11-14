// --------------------- Created By InCoder ---------------------
import {choc, set_content, on, DOM, fix_dialogs} from "https://rosuav.github.io/choc/factory.js";
const {DIV, IMG, H1, H2, H3, H4, A, DIALOG, FIGURE, FIGCAPTION, BUTTON, P, SECTION, UL, LI, SPAN} = choc; //autoimport

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

const placeholder_colors = ['red', 'gold', 'green', 'blue', 'teal', 'azure'];

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
  if (item.image) return DIV({class: 'gallery-image', style: `background-image: url("${item.image.url}")`, title: item.project + ' ' + item.artist});
  let color = placeholder_colors[Math.floor(Math.random() * 5)];
  return DIV({class: 'placeholder gallery-image ' + color}, DIV([H1(item.project),H2(item.artist)]));
}


if (window.client_listing === true) {
  set_content("#gallery", UL(
    sets.map((set, idx) => LI({'data-set': idx},
      [set, SPAN([
        " (",
          galleries[set].map((item, idx) => [idx && ", ", A({href: "#", "data-idx": idx, class: "gallery_entry"}, item.project || item.year)]),
        ")"])]
        )
      )
    )
  );

} else {
  set_content("#gallery",
    sets.map((set, idx )=> SECTION({'data-set': idx}, [
      H2(set),
      DIV({class: "gallery_set"}, galleries[set].map((item, idx) => DIV({"data-idx": idx, class: "gallery_entry"}, gallery_image(item) )))
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
    item.artist && H2(item.artist),
    item.roles && H4(item.roles.join(", ")),
    item.notes && item.notes.split("\n\n").map(p => P({".innerHTML": p})),
    // Using .innerHTML is a cheat that Choc Factory makes "work".
    // TODO LINK,
    item.project_url && A({class: "artist-link", href: item.project_url.url, target: "_blank"}, item.project_url.title),
    item.year && H3(item.year),
  ]);
}

on("click", ".gallery_entry", e => {
  display_item(e.match.closest("[data-set]").dataset.set, e.match.closest("[data-idx]").dataset.idx);
  DOM("#gallerydlg").showModal();
});

on("click", "#prev", e => {
  if (selected_item) {
    display_item(selected_set, selected_item - 1);
  } else {
    const set = selected_set ? selected_set - 1 : sets.length - 1;
    display_item(set, galleries[sets[set]].length - 1);
  }
});

on("click", "#next", e => {
  if (selected_item < galleries[sets[selected_set]].length - 1) {
    display_item(selected_set, selected_item + 1);
  } else {
    display_item((selected_set + 1) % sets.length, 0);
  }
});
