const track = document.getElementById("book");
const pages = [...track.querySelectorAll(":scope > .page")];
const N = pages.length;
const prevBtn = document.querySelector('[data-dir="prev"]');
const nextBtn = document.querySelector('[data-dir="next"]');
const posNum = document.getElementById("posNum");
const posTitle = document.getElementById("posTitle");
const status = document.getElementById("pageStatus");
const spread = matchMedia("(min-width: 1000px) and (min-aspect-ratio: 4/3)");
const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)");

let pending = null;      // page index a click/key is scrolling to
let settled = null;      // last settled page index
let rafQueued = false;

const step = () => (spread.matches ? 2 : 1);
const align = (i) => (spread.matches ? i - (i % 2) : i);
const clamp = (i) => Math.max(0, Math.min(N - 1, i));

function nearest() {
  const x = track.scrollLeft;
  let best = 0, dist = Infinity;
  for (let i = 0; i < N; i += step()) {
    const d = Math.abs(pages[i].offsetLeft - x);
    if (d < dist) { dist = d; best = i; }
  }
  return best;
}

function paint(i) {
  posNum.textContent = spread.matches && i + 1 < N ? `${i + 1}–${i + 2}` : String(i + 1);
  posTitle.textContent = pages[i].dataset.title;
  const atStart = i === 0;
  const atEnd = i + step() > N - 1;
  // keep focus on a usable control when one end disables the button that had it
  if (atStart && document.activeElement === prevBtn) nextBtn.focus();
  if (atEnd && document.activeElement === nextBtn) prevBtn.focus();
  prevBtn.disabled = atStart;
  nextBtn.disabled = atEnd;
}

function goTo(i, { instant = false, focus = false } = {}) {
  i = align(clamp(i));
  pending = i;
  paint(i);
  track.scrollTo({ left: pages[i].offsetLeft, behavior: instant || reduceMotion.matches ? "instant" : "smooth" });
  if (focus) pages[i].focus({ preventScroll: true });
  if (instant) settle();
}

function settle() {
  const i = nearest();
  pending = null;
  paint(i);
  if (settled !== null && i !== settled) {
    status.textContent = `第 ${i + 1} 页，共 ${N} 页：${pages[i].dataset.title}`;
  }
  settled = i;
  history.replaceState(null, "", `#${pages[i].id}`);
}

prevBtn.addEventListener("click", () => goTo((pending ?? nearest()) - step()));
nextBtn.addEventListener("click", () => goTo((pending ?? nearest()) + step()));

// in-book links (contents page, cross references) flip instead of jumping
document.addEventListener("click", (e) => {
  const a = e.target.closest('a[href^="#p-"]');
  if (!a) return;
  const i = pages.findIndex((p) => `#${p.id}` === a.getAttribute("href"));
  if (i < 0) return;
  e.preventDefault();
  goTo(i, { focus: true });
});

// arrow keys flip pages, but never steal keys from links, buttons or the hourly table
document.addEventListener("keydown", (e) => {
  if (e.altKey || e.ctrlKey || e.metaKey) return;
  if (e.target.closest("a, button, input, select, textarea, .hourly-wrap")) return;
  if (e.key === "ArrowRight") { e.preventDefault(); goTo((pending ?? nearest()) + step()); }
  if (e.key === "ArrowLeft") { e.preventDefault(); goTo((pending ?? nearest()) - step()); }
});

// live position while swiping; skipped during scripted scrolls
track.addEventListener("scroll", () => {
  if (pending !== null || rafQueued) return;
  rafQueued = true;
  requestAnimationFrame(() => { rafQueued = false; if (pending === null) paint(nearest()); });
}, { passive: true });

if ("onscrollend" in window) {
  track.addEventListener("scrollend", settle);
} else {
  let t;
  track.addEventListener("scroll", () => { clearTimeout(t); t = setTimeout(settle, 140); }, { passive: true });
}

// re-align when switching between single page and spread
spread.addEventListener("change", () => goTo(settled ?? 0, { instant: true }));
addEventListener("resize", () => { if (settled !== null) track.scrollLeft = pages[align(settled)].offsetLeft; });

// open at the page in the URL, silently
const start = pages.findIndex((p) => `#${p.id}` === location.hash);
goTo(start < 0 ? 0 : start, { instant: true });
