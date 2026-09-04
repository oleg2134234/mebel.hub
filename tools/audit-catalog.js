const fs = require("fs");
const path = require("path");
const vm = require("vm");

const root = path.resolve(__dirname, "..");
const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
const script = html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
if (!script) throw new Error("Inline script not found");

const dataBlock = script.slice(0, script.indexOf("  const CATS ="))
  .replace(/\bconst PRODUCTS\b/, "var PRODUCTS")
  .replace(/\bconst IMAGES\b/, "var IMAGES")
  .replace(/\bconst GALLERIES\b/, "var GALLERIES");
const context = {};
vm.createContext(context);
vm.runInContext(dataBlock, context);

const { PRODUCTS, IMAGES, GALLERIES } = context;
const issues = [];
const add = (severity, code, product, detail) => issues.push({ severity, code, product, detail });
const productById = new Map(PRODUCTS.map((p) => [String(p.id), p]));
const idCounts = PRODUCTS.reduce((m, p) => m.set(String(p.id), (m.get(String(p.id)) || 0) + 1), new Map());

for (const [id, count] of idCounts) {
  if (count > 1) add("critical", "duplicate-id", productById.get(id)?.title || id, `ID ${id} встречается ${count} раза`);
}

const canonical = [
  [/^В интерьере$/, 10], [/^Уют(?:ный вечер)?$/, 20], [/^Размеры$/, 30], [/^Разрез$/, 40],
  [/^Видео:/, 50], [/^Общий вид(?: \(студия\))?$/, 60], [/^Вид спереди$/, 61],
  [/^Ракурс 3\/4$/, 62], [/^Вид сбоку$/, 63], [/^Вид сзади$/, 64],
  [/^В разложенном виде$/, 70], [/^Раскладка$/, 71], [/^Спальное место$/, 72],
  [/^Бельевой (?:ящик|короб)/, 80], [/^Практичность$/, 90],
];
const rank = (name) => canonical.find(([re]) => re.test(name))?.[1];

for (const p of PRODUCTS) {
  const id = String(p.id);
  const label = `${id} ${p.title}`;
  const dims = String(p.dims || "").split("×");
  if (dims.length < 2 || !/\d/.test(dims[0]) || !/\d/.test(dims[1])) {
    add("critical", "dims", label, `Некорректные обязательные габариты: ${p.dims || "пусто"}`);
  }
  if (!p.desc) add("warning", "description", label, "Описание отсутствует");
  if (!IMAGES[id]) add("critical", "hero", label, "Нет главного изображения");
  else if (!fs.existsSync(path.join(root, IMAGES[id]))) add("critical", "missing-file", label, `Нет файла ${IMAGES[id]}`);

  const gallery = GALLERIES[id];
  if (!gallery?.slides?.length) {
    add("critical", "gallery", label, "Галерея отсутствует или пуста");
    continue;
  }
  if (gallery.slides[0].name !== "В интерьере") add("warning", "first-slide", label, `Первый слайд: ${gallery.slides[0].name}`);
  const practical = gallery.slides.findIndex((s) => s.name === "Практичность");
  if (practical >= 0 && practical !== gallery.slides.length - 1) add("critical", "practicality-order", label, "«Практичность» не последний слайд");

  let previous = 0;
  for (const slide of gallery.slides) {
    const current = rank(slide.name);
    if (current == null) add("info", "noncanonical-name", label, `Нестандартное имя: ${slide.name}`);
    else {
      if (current < previous) add("critical", "slide-order", label, `Нарушение порядка перед «${slide.name}»`);
      previous = Math.max(previous, current);
    }
    const mediaPath = path.join(root, slide.src);
    if (!fs.existsSync(mediaPath)) add("critical", "missing-file", label, `Нет файла ${slide.src}`);
    else if (fs.statSync(mediaPath).size > 5 * 1024 * 1024) add("warning", "large-media", label, `${slide.src}: ${(fs.statSync(mediaPath).size / 1048576).toFixed(1)} МБ`);
  }
}

for (const id of Object.keys(GALLERIES)) {
  if (!productById.has(id)) add("warning", "orphan-gallery", id, "Галерея без товара");
}

const summary = {
  generatedAt: new Date().toISOString(),
  products: PRODUCTS.length,
  galleries: Object.keys(GALLERIES).length,
  referencedMedia: new Set(Object.values(GALLERIES).flatMap((g) => g.slides.map((s) => s.src))).size,
  issues: {
    critical: issues.filter((i) => i.severity === "critical").length,
    warning: issues.filter((i) => i.severity === "warning").length,
    info: issues.filter((i) => i.severity === "info").length,
  },
};

console.log(JSON.stringify({ summary, issues }, null, 2));
process.exitCode = summary.issues.critical ? 1 : 0;
