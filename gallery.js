// --------------------- Created By InCoder ---------------------
import {choc, set_content, on, DOM, fix_dialogs} from "https://rosuav.github.io/choc/factory.js";
const {DIV, IMG, H1, H2, A, DIALOG, FIGURE, FIGCAPTION, BUTTON, P, SECTION} = choc; //autoimport

let selected_item = 0;
let selected_set = 0;

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
  return "coming soon.";
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
  DOM("#gallerydlg img").src = item.image.url;
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

/*
let image_boxes = document.querySelectorAll('.disc-image'),
lightBoxOverlay = document.querySelector('.lightBoxOverlay'),
containerBody = document.querySelector('.lightBoxOverlay .body'),
containerBodyH1 = document.querySelector('.lightBoxOverlay .body h1'),
containerBodyH2 = document.querySelector('.lightBoxOverlay .body h2'),
containerBodyH3 = document.querySelector('.lightBoxOverlay .body h3'),
containerBodyNotes = document.querySelector('.lightBoxOverlay .body .notes'),
containerBodyRoles = document.querySelector('.lightBoxOverlay .body .roles'),
containerBodyLinkButton = document.querySelector('.lightBoxOverlay .body .card .link_button'),
visualRepresentation = document.getElementById('visual_representation'),
largeProjectImage = document.getElementById('large_project_image');

let nextBtn = document.querySelector('.next'),
preBtn = document.querySelector('.pre'),
wrapper = document.querySelector('.wrapper'),
closeBtn = document.querySelector('.closeBtn'),
totalImg = document.querySelector('.total'),
currentImg = document.querySelector('.current'),
fullSizeImages = document.createElement('div');

let newindex, current_set, imagePlaceholder, image;

function openPreview() {
  let id = image_boxes[newindex].dataset.id;
  let current_project = galleries[current_set.replace("dg-", "")][id];
  let fullimage = current_project.fullimage;

  if (fullimage) {
    set_content(visualRepresentation, IMG({src: fullimage}));
  } else {
    set_content(visualRepresentation, DIV({class: 'disc-placeholder-large ' + current_project.placeholder_color, }, DIV([
      H1(current_project.title),
      H2(current_project.artists),
    ])));
  }

  containerBodyH1.innerText = current_project.title;
  containerBodyH2.innerText = current_project.artists;
  containerBodyH3.innerText = current_project.roles;

  set_content(containerBodyLinkButton, "");
  if (current_project.url && current_project.url.url) {
    set_content(containerBodyLinkButton,
                A({href: current_project.url.url, target: current_project.url.target, class: 'btn'}, current_project.url.title)
    );
  }

  containerBodyNotes.innerHTML = current_project.additional_notes;


  preBtn.style.display = 'grid';
  nextBtn.style.display = 'grid';
  preBtn.style.visibility = 'visible';
  nextBtn.style.visibility = 'visible';
  if ((newindex == 0) ||
  // Inspect previous item
(current_set != image_boxes[newindex - 1].closest('.discography-grid').id)) {
    preBtn.style.visibility = 'hidden';
  }
  if ((newindex >= image_boxes.length - 1) ||
  // Inspect following item
  (current_set != image_boxes[newindex + 1].closest('.discography-grid').id)) {
    nextBtn.style.visibility = 'hidden';
  }
  lightBoxOverlay.classList.add('show')
}

function storybook_preload_images() {
  // preload all full size disc images on page load.
  for (let i = 0; i < image_boxes.length; i++) {
    let current_index = i;
    if (image_boxes[i].dataset.fullimage) {
      let tempImage = document.createElement('img');
      tempImage.src = image_boxes[i].dataset.fullimage;
      fullSizeImages.appendChild(tempImage);
    }
  } // end loop
}

if (document.readyState !== "loading") storybook_preload_images();
else window.addEventListener("DOMContentLoaded", storybook_preload_images);

for (let i = 0; i < image_boxes.length; i++) {
  let current_index = i;

  image_boxes[i].addEventListener('click', () => {
    newindex = current_index;
    current_set = image_boxes[newindex].closest('.discography-grid').id;
    openPreview();
  })
} // end loop


preBtn.addEventListener('click', () => {
  newindex--;
  openPreview();
});

nextBtn.addEventListener('click', () => {
  newindex++;
  openPreview();
});

closeBtn.addEventListener('click', () => {
  lightBoxOverlay.classList.remove('show')
});

lightBoxOverlay.addEventListener('click', (e) => {
  if (e.target.closest("#left-button,#right-button")) return;
  lightBoxOverlay.classList.remove('show');
});
*/
