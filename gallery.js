// --------------------- Created By InCoder ---------------------
import {choc, set_content, on, DOM, fix_dialogs} from "https://rosuav.github.io/choc/factory.js";
const {DIV, IMG, H1, H2, A, DIALOG, FIGURE, FIGCAPTION, BUTTON, P, SECTION} = choc; //autoimport

let selected_item = 0;
let selected_set = 0;
const placeholder_colors = ['red', 'gold', 'green', 'blue', 'teal', 'azure'];

const sets = Object.keys(galleries);
sets.sort((a, b) => b.localeCompare(a)); // reverse sort

document.body.appendChild(DIALOG({id: "gallerydlg"}, [
  DIV({id: "dialog_header"}, [
    DIV([BUTTON({id: "prev"}, "previous"), BUTTON({id: "next"}, "next")]),
    BUTTON({type: "button", class: "dialog_cancel"}, 'x')]),
  FIGURE([
    IMG(),
    FIGCAPTION()
  ])
]));

// Support for older browsers
fix_dialogs({close_selector: ".dialog_cancel,.dialog_close", click_outside: "formless"});

function image_cover(item) {
  if (item.image) return IMG({src: item.image.url, title: item.image.title, alt: item.image.title});
  let color = placeholder_colors[Math.floor(Math.random() * 5)];
  return DIV({class: 'disc-placeholder ' + color, style: "min-width:220;min-height:220;"}, [P("coming soon.")]);
}

set_content("#gallery",
  sets.map((set, idx )=> SECTION({'data-set': idx}, [
    H2(set),
    DIV({class: "gallery_set"}, galleries[set].map((item, idx) => DIV({"data-idx": idx}, image_cover(item) )))
  ]))
);

function display_item(set, idx) {
  selected_item = +idx; // cast as number
  selected_set = +set;
  console.log(selected_item, selected_set);
  const item = galleries[sets[set]][idx];
  // Do we have an image?
  if (item.image.url) {
    DOM("#gallerydlg img").src = item.image.url;
  } else {
    // TODO
  }
  set_content("#gallerydlg figcaption", [
    item.project && H1(item.project),
    item.artist && H2(item.artist),
    item.roles && P(item.roles.join(", ")),
    item.notes && item.notes.split("\n\n").map(p => P({".innerHTML": p})),
    // Using .innerHTML is a cheat that Choc Factory makes "work".
    // TODO LINK
  ]);
}

on("click", ".gallery_set > div", e => {
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
