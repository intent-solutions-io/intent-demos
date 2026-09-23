const controls = [...document.querySelectorAll("[data-skill-filter]")];
const skills = [...document.querySelectorAll(".sc-skill")];
const count = document.querySelector("#skill-count");

for (const control of controls) {
  control.addEventListener("click", () => {
    const filter = control.dataset.skillFilter;
    let visible = 0;
    for (const skill of skills) {
      const show = filter === "all" || skill.dataset.group === filter;
      skill.hidden = !show;
      if (show) visible += 1;
    }
    for (const button of controls) {
      button.setAttribute("aria-pressed", String(button === control));
    }
    count.textContent = String(visible);
  });
}
