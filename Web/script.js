
next = document.getElementsByClassName("next")[0];
previous = document.getElementsByClassName("previous")[0];

document.addEventListener("keydown", e => {
  link = false;

  if (e.key === "ArrowLeft") {
    link = previous.getAttribute("href");
  } else if (e.key === "ArrowRight") {
    link = next.getAttribute("href");
  }

  console.log(`go to ${link} from press ${e.key}`);

  document.location = link;
  return false;
});
