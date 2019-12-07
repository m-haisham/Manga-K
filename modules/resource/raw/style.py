style = """
body {
  padding: 0;
  margin: 0;
  font: Helvetica, Arial, sans-serif;
}
h3 {
  margin: 0;
}
* {
  box-sizing: border-box;
  background-color: #24252a;
}
li,
a,
button,
h3,
div {
  color: #ffffff;
  text-decoration: none;
}
nav,
.chapter_nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.1em 10%;
}
.footer {
  display: flex;
  justify-content: center;
  padding: 2em;
  margin-top: 2em;
  text-align: center;
  font-size: large;
  background-color: #1e1f24;
  box-shadow: inset 0 -0.6em 0 -0.35em rgba(0, 0, 0, 0.17);
}
.footer .content {
  display: flex;
  justify-content: center;
  padding: 1em 1.4em;
  transition: all 0.3s ease 0s;
}
.footer .content:hover {
  transition: all 0.3s ease 0s;
  box-shadow: inset 0 -5em 0 -2em rgba(0, 0, 0, 0.17);
}
.footer .content div {
  margin-right: 0.4em;
}
.footer a,
.footer div {
  background-color: transparent;
}
.container {
  padding: 0px 10%;
}
.list li {
  list-style: none;
}
.list .header {
  display: inline-block;
  border-radius: 0.3em;
  text-transform: uppercase;
  padding: 0.6em 1.2em;
  margin-top: 1em;
  margin-bottom: 0.5em;
  background-color: rgba(0, 0, 0, 0.17);
  box-shadow: inset 0 -0.6em 0 -0.35em #383838;
}
.mt-2 {
  margin-top: 1.4em;
}
.divider {
  margin: 0px 9%;
  padding: 0.1em;
  box-shadow: inset 0 -0.6em 0 -0.35em rgba(0, 0, 0, 0.17);
}
.title {
  text-transform: uppercase;
  font-weight: bold;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.nav_links,
.chap_links {
  min-width: 21em;
  list-style: none;
}
.nav_links li,
.chap_links li {
  display: inline-block;
  padding: 0px 0.5em;
}
.nav_links li a {
  border-radius: 0.3em;
  text-transform: uppercase;
  padding: 0.6em 1.2em;
  transition: all 0.3s ease 0s;
  box-shadow: inset 0 -0.6em 0 -0.35em #3369ff;
}
.nav_links li a:hover {
  transition: all 0.3s ease 0s;
  color: #3369ff;
  box-shadow: inset 0 -5em 0 -2.5em #121c3b;
}
.nav_links li a:active {
  transition: all 0.1s ease 0s;
  color: #3369ff;
  box-shadow: inset 0 -5em 0 -2.5em rgba(0, 0, 0, 0.17);
}
a.btn {
  display: inline-block;
  padding: 0.7em 1.4em;
  margin: 0 0.3em 0.3em 0;
  border-radius: 0.15em;
  box-sizing: border-box;
  text-decoration: none;
  font-family: "Roboto", sans-serif;
  text-transform: uppercase;
  font-weight: 400;
  color: #ffffff;
  background-color: #3369ff;
  box-shadow: inset 0 -0.6em 0 -0.35em rgba(0, 0, 0, 0.17);
  text-align: center;
  position: relative;
}
a.btn:active {
  top: 0.1em;
}
.page {
  max-width: 100%;
  display: block;
  margin: 0 auto 5px;
  z-index: 1 !important;
}
@media all and (max-width: 30em) {
  a.btn {
    display: block;
    max-width: 0.4em auto;
  }
}

"""