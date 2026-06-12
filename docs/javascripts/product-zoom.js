(() => {
  const image = document.querySelector("#wild-zoom-device");
  const label = document.querySelector("#wild-zoom-label");
  const title = document.querySelector("#wild-zoom-title");
  const description = document.querySelector("#wild-zoom-description");
  const steps = Array.from(document.querySelectorAll(".wild-zoom-step"));

  if (!image || !label || !title || !description || steps.length === 0) return;

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const parsePercent = (value, fallback) => {
    const parsed = Number.parseFloat(String(value || "").replace("%", ""));
    return Number.isFinite(parsed) ? parsed : fallback;
  };
  const clamp = (value, min, max) => Math.min(Math.max(value, min), max);
  const ease = (value) => value * value * (3 - 2 * value);

  const views = steps.map((step) => ({
    step,
    x: parsePercent(step.dataset.zoomX, 50),
    y: parsePercent(step.dataset.zoomY, 50),
    scale: Number.parseFloat(step.dataset.zoomScale || "1") || 1,
    title: step.dataset.zoomTitle || "",
    description: step.dataset.zoomDescription || "",
    label: step.dataset.zoomLabel || step.dataset.zoomTitle || "",
  }));

  let activeIndex = -1;
  let animationFrame = 0;

  const setImageView = ({ x, y, scale }) => {
    image.style.setProperty("--wild-zoom-x", `${x}%`);
    image.style.setProperty("--wild-zoom-y", `${y}%`);
    image.style.setProperty("--wild-zoom-scale", scale.toFixed(3));
  };

  const setActiveText = (index) => {
    if (index === activeIndex) return;

    const view = views[index];
    steps.forEach((candidate) => {
      candidate.classList.toggle("is-active", candidate === view.step);
    });
    title.textContent = view.title;
    description.textContent = view.description;
    label.textContent = view.label;
    activeIndex = index;
  };

  const interpolate = (from, to, progress) => ({
    x: from.x + (to.x - from.x) * progress,
    y: from.y + (to.y - from.y) * progress,
    scale: from.scale + (to.scale - from.scale) * progress,
  });

  const measureCenters = () =>
    steps.map((step) => {
      const rect = step.getBoundingClientRect();
      return window.scrollY + rect.top + rect.height / 2;
    });

  const updateZoom = () => {
    animationFrame = 0;

    const centers = measureCenters();
    const anchor = window.scrollY + window.innerHeight * 0.52;
    const lastIndex = views.length - 1;
    let nearestIndex = 0;

    centers.forEach((center, index) => {
      if (Math.abs(center - anchor) < Math.abs(centers[nearestIndex] - anchor)) {
        nearestIndex = index;
      }
    });
    setActiveText(nearestIndex);

    if (reducedMotion.matches || anchor <= centers[0]) {
      setImageView(views[nearestIndex]);
      return;
    }

    if (anchor >= centers[lastIndex]) {
      setImageView(views[lastIndex]);
      return;
    }

    const segmentIndex = centers.findIndex((center, index) => {
      return index < lastIndex && anchor >= center && anchor <= centers[index + 1];
    });
    const startIndex = Math.max(segmentIndex, 0);
    const segmentLength = centers[startIndex + 1] - centers[startIndex];
    const rawProgress = segmentLength === 0 ? 0 : (anchor - centers[startIndex]) / segmentLength;
    const progress = ease(clamp(rawProgress, 0, 1));

    setImageView(interpolate(views[startIndex], views[startIndex + 1], progress));
  };

  const requestZoomUpdate = () => {
    if (animationFrame) return;
    animationFrame = window.requestAnimationFrame(updateZoom);
  };

  setActiveText(0);
  setImageView(views[0]);
  requestZoomUpdate();

  window.addEventListener("scroll", requestZoomUpdate, { passive: true });
  window.addEventListener("resize", requestZoomUpdate);
  reducedMotion.addEventListener?.("change", requestZoomUpdate);
})();
