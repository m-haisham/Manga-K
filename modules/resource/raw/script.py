script = """
next = document.getElementsByClassName("next")[0];

previous = document.getElementsByClassName("previous")[0];

document.addEventListener("keydown", e => {
  if (e.key === "ArrowLeft") {
    document.location = previous.getAttribute("href");
  } else if (e.key === "ArrowRight") {
    document.location = next.getAttribute("href");
  }
});

"""