(() => {
  "use strict";

  const COLORS = {
    "1": "var(--ocq-red)",
    "2": "var(--ocq-orange)",
    "3": "var(--ocq-yellow)",
    "4": "var(--ocq-green)",
    "5": "var(--ocq-cyan)",
    "6": "var(--ocq-purple)",
  };

  const SVG_NS = "http://www.w3.org/2000/svg";
  const FRAGMENT_CACHE = new Map();
  const PREVIEW_CACHE = new Map();
  const PREVIEW_DELAY = 280;
  const PREVIEW_WIDTH = 300;
  const PREVIEW_HEIGHT = 240;
  const PREVIEW_TARGET_INSET = 8;
  const MATHJAX_WAIT_MS = 10000;
  const MATHJAX_POLL_MS = 25;
  const MATH_TYPESET_STATE = new WeakMap();
  const DOUBLE_TAP_MS = 350;
  const TAP_MOVE_PX = 12;
  const DEFAULT_ZOOM_DURATION_MS = 300;
  const MAX_ZOOM_SPEED = 10;

  function element(tag, className, attributes = {}) {
    const item = document.createElement(tag);
    item.className = className;
    Object.entries(attributes).forEach(([key, value]) => item.setAttribute(key, value));
    return item;
  }

  function svgElement(tag, className, attributes = {}) {
    const item = document.createElementNS(SVG_NS, tag);
    item.setAttribute("class", className);
    Object.entries(attributes).forEach(([key, value]) => item.setAttribute(key, value));
    return item;
  }

  function color(value, fallback = "var(--ocq-edge)") {
    if (!value) return fallback;
    const identifier = String(value);
    if (Object.prototype.hasOwnProperty.call(COLORS, identifier)) {
      return `var(--ocq-color-${identifier}, ${COLORS[identifier]})`;
    }
    if (/^\d+$/.test(identifier)) {
      return `var(--ocq-color-${identifier}, ${fallback})`;
    }
    return identifier;
  }

  function applyItemColor(item, value, fallback = "var(--ocq-edge)") {
    if (value == null || value === "") return;
    const identifier = String(value);
    item.dataset.ocqColor = identifier;
    if (/^[a-zA-Z0-9_-]+$/.test(identifier)) {
      item.classList.add(`ocq-color-${identifier}`);
    }
    item.style.setProperty("--ocq-item-color", color(identifier, fallback));
  }

  function position(item, model) {
    item.style.left = `${model.x}px`;
    item.style.top = `${model.y}px`;
    item.style.width = `${model.width}px`;
    item.style.height = `${model.height}px`;
    applyItemColor(item, model.color);
  }

  function defaultSide(node, other) {
    const dx = other.x + other.width / 2 - (node.x + node.width / 2);
    const dy = other.y + other.height / 2 - (node.y + node.height / 2);
    if (Math.abs(dx) >= Math.abs(dy)) return dx >= 0 ? "right" : "left";
    return dy >= 0 ? "bottom" : "top";
  }

  function anchor(node, side) {
    const points = {
      top: [node.x + node.width / 2, node.y],
      right: [node.x + node.width, node.y + node.height / 2],
      bottom: [node.x + node.width / 2, node.y + node.height],
      left: [node.x, node.y + node.height / 2],
    };
    return points[side];
  }

  function edgeGeometry(source, target, sourceSide, targetSide, offset = 0) {
    const [sx, sy] = anchor(source, sourceSide);
    const [tx, ty] = anchor(target, targetSide);
    const distance = Math.max(55, Math.min(220, Math.hypot(tx - sx, ty - sy) * 0.42));
    const vectors = { top: [0, -1], right: [1, 0], bottom: [0, 1], left: [-1, 0] };
    const [sdx, sdy] = vectors[sourceSide];
    const [tdx, tdy] = vectors[targetSide];
    const length = Math.max(1, Math.hypot(tx - sx, ty - sy));
    const normalX = -(ty - sy) / length;
    const normalY = (tx - sx) / length;
    const c1x = sx + sdx * distance + normalX * offset;
    const c1y = sy + sdy * distance + normalY * offset;
    const c2x = tx + tdx * distance + normalX * offset;
    const c2y = ty + tdy * distance + normalY * offset;
    const midpoint = {
      x: (sx + 3 * c1x + 3 * c2x + tx) / 8,
      y: (sy + 3 * c1y + 3 * c2y + ty) / 8,
    };
    return {
      path: `M ${sx} ${sy} C ${c1x} ${c1y}, ${c2x} ${c2y}, ${tx} ${ty}`,
      midpoint,
      source: { x: sx, y: sy },
      target: { x: tx, y: ty },
      controls: [{ x: c1x, y: c1y }, { x: c2x, y: c2y }],
    };
  }

  function edgePath(source, target, sourceSide, targetSide) {
    return edgeGeometry(source, target, sourceSide, targetSide).path;
  }

  function parallelEdgeOffsets(edges, spacing = 14) {
    const groups = new Map();
    edges.forEach((edge) => {
      const key = [edge.source.node, edge.target.node].sort().join("\u0000");
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push(edge);
    });
    const offsets = new Map();
    groups.forEach((items) => {
      items.sort((first, second) => first.id.localeCompare(second.id));
      items.forEach((edge, index) => {
        offsets.set(edge.id, (index - (items.length - 1) / 2) * spacing);
      });
    });
    return offsets;
  }

  function fitTransform(bounds, viewportWidth, viewportHeight) {
    if (!bounds || bounds.width <= 0 || bounds.height <= 0) {
      return { x: 40, y: 40, scale: 1 };
    }
    const padding = 52;
    const availableWidth = Math.max(1, viewportWidth - padding * 2);
    const availableHeight = Math.max(1, viewportHeight - padding * 2);
    const scale = Math.min(1.5, Math.max(0.12, Math.min(availableWidth / bounds.width, availableHeight / bounds.height)));
    return {
      scale,
      x: (viewportWidth - bounds.width * scale) / 2 - bounds.x * scale,
      y: (viewportHeight - bounds.height * scale) / 2 - bounds.y * scale,
    };
  }

  function focusTransform(bounds, viewportWidth, viewportHeight) {
    if (!bounds || bounds.width <= 0 || bounds.height <= 0) {
      return { x: 24, y: 24, scale: 1 };
    }
    const padding = 24;
    const availableWidth = Math.max(1, viewportWidth - padding * 2);
    const availableHeight = Math.max(1, viewportHeight - padding * 2);
    const scale = Math.min(
      4,
      Math.max(0.12, Math.min(availableWidth / bounds.width, availableHeight / bounds.height)),
    );
    return {
      scale,
      x: (viewportWidth - bounds.width * scale) / 2 - bounds.x * scale,
      y: (viewportHeight - bounds.height * scale) / 2 - bounds.y * scale,
    };
  }

  function zoomTransform(state, factor, screenX, screenY) {
    const scale = Math.min(4, Math.max(0.12, state.scale * factor));
    const ratio = scale / state.scale;
    return {
      scale,
      x: screenX - (screenX - state.x) * ratio,
      y: screenY - (screenY - state.y) * ratio,
    };
  }

  function zoomDuration(value) {
    const speed = Number(value);
    if (!Number.isFinite(speed) || speed < 0 || speed > MAX_ZOOM_SPEED) {
      return DEFAULT_ZOOM_DURATION_MS;
    }
    return speed === 0 ? 0 : DEFAULT_ZOOM_DURATION_MS / speed;
  }

  function resetTransform(bounds, viewportWidth, viewportHeight) {
    if (!bounds || bounds.width <= 0 || bounds.height <= 0) {
      return { x: 40, y: 40, scale: 1 };
    }
    return {
      scale: 1,
      x: (viewportWidth - bounds.width) / 2 - bounds.x,
      y: (viewportHeight - bounds.height) / 2 - bounds.y,
    };
  }

  function shouldDrawArrow(end, defaultArrow = false) {
    return end === "arrow" || (end == null && defaultArrow);
  }

  function pinchTransform(state, startPoints, currentPoints) {
    const midpoint = (points) => ({
      x: (points[0].x + points[1].x) / 2,
      y: (points[0].y + points[1].y) / 2,
    });
    const distance = (points) => Math.max(
      1,
      Math.hypot(points[1].x - points[0].x, points[1].y - points[0].y),
    );
    const startMidpoint = midpoint(startPoints);
    const currentMidpoint = midpoint(currentPoints);
    const scale = Math.min(
      4,
      Math.max(0.12, state.scale * distance(currentPoints) / distance(startPoints)),
    );
    const world = {
      x: (startMidpoint.x - state.x) / state.scale,
      y: (startMidpoint.y - state.y) / state.scale,
    };
    return {
      scale,
      x: currentMidpoint.x - world.x * scale,
      y: currentMidpoint.y - world.y * scale,
    };
  }

  function fetchFragment(url) {
    if (!FRAGMENT_CACHE.has(url)) {
      FRAGMENT_CACHE.set(url, fetch(url).then((response) => {
        if (!response.ok) throw new Error(`request returned ${response.status}`);
        return response.text();
      }));
    }
    return FRAGMENT_CACHE.get(url);
  }

  function clearFragmentCache() {
    FRAGMENT_CACHE.clear();
  }

  function fetchPreviewIndex(url) {
    if (!PREVIEW_CACHE.has(url)) {
      PREVIEW_CACHE.set(url, fetch(url).then((response) => {
        if (!response.ok) throw new Error(`request returned ${response.status}`);
        return response.json();
      }));
    }
    return PREVIEW_CACHE.get(url);
  }

  function clearPreviewCache() {
    PREVIEW_CACHE.clear();
  }

  function previewPosition(anchorRect, previewSize, viewport) {
    const margin = 8;
    const gap = 8;
    const width = Math.min(previewSize.width, viewport.width - margin * 2);
    const height = Math.min(previewSize.height, viewport.height - margin * 2);
    const preferredLeft = anchorRect.left + anchorRect.width / 2 - width / 2;
    const left = Math.max(margin, Math.min(preferredLeft, viewport.width - width - margin));
    const below = anchorRect.bottom + gap;
    const top = below + height <= viewport.height - margin
      ? below
      : Math.max(margin, anchorRect.top - height - gap);
    return { left, top, width, height };
  }

  function scrollPreviewToHash(content, hash, namespace) {
    if (!hash || hash === "#") return false;
    let identifier;
    try {
      identifier = decodeURIComponent(hash.slice(1));
    } catch {
      identifier = hash.slice(1);
    }
    const targetId = `${namespace}-${identifier}`;
    const target = [...content.querySelectorAll("[id]")]
      .find((item) => item.id === targetId);
    if (!target) return false;
    const contentTop = content.getBoundingClientRect().top;
    const targetTop = target.getBoundingClientRect().top;
    content.scrollTop = Math.max(
      0,
      content.scrollTop + targetTop - contentTop - PREVIEW_TARGET_INSET,
    );
    return true;
  }

  function safeUrl(value, baseUrl) {
    try {
      const resolved = new URL(value, baseUrl);
      return ["http:", "https:", "mailto:"].includes(resolved.protocol) ? resolved.href : null;
    } catch {
      return null;
    }
  }

  function safeFragment(markup, baseUrl, namespace) {
    const parsed = new DOMParser().parseFromString(markup, "text/html");
    parsed.querySelectorAll("script, iframe, object, embed").forEach((item) => item.remove());
    const ids = new Map();
    parsed.querySelectorAll("[id]").forEach((item) => {
      const original = item.id;
      const namespaced = `${namespace}-${original}`;
      ids.set(original, namespaced);
      item.id = namespaced;
    });
    parsed.querySelectorAll("*").forEach((item) => {
      [...item.attributes].forEach((attribute) => {
        const name = attribute.name.toLowerCase();
        if (name.startsWith("on")) item.removeAttribute(attribute.name);
      });
      ["href", "src"].forEach((name) => {
        const value = item.getAttribute(name);
        if (!value) return;
        if (value.startsWith("#")) {
          const target = ids.get(value.slice(1));
          if (target) item.setAttribute(name, `#${target}`);
          return;
        }
        try {
          const resolved = new URL(value, baseUrl);
          if (!["http:", "https:", "mailto:"].includes(resolved.protocol)) {
            item.removeAttribute(name);
          } else {
            item.setAttribute(name, resolved.href);
          }
        } catch {
          item.removeAttribute(name);
        }
      });
    });
    const fragment = document.createDocumentFragment();
    [...parsed.body.childNodes].forEach((item) => fragment.append(document.importNode(item, true)));
    return fragment;
  }

  function hasMath(element) {
    return element.matches?.(".math") || Boolean(element.querySelector?.(".math"));
  }

  function mathJaxIsExpected() {
    if (window.MathJax) return true;
    return Boolean([...document.scripts].find((script) => /mathjax/i.test(script.src)));
  }

  async function waitForMathJax() {
    if (!mathJaxIsExpected()) return null;
    const deadline = Date.now() + MATHJAX_WAIT_MS;
    while (Date.now() <= deadline) {
      const mathJax = window.MathJax;
      if (mathJax?.startup?.promise) {
        await mathJax.startup.promise;
        return window.MathJax;
      }
      if (
        typeof mathJax?.typesetPromise === "function" ||
        typeof mathJax?.typeset === "function"
      ) return mathJax;
      await new Promise((resolve) => setTimeout(resolve, MATHJAX_POLL_MS));
    }
    throw new Error("MathJax did not become ready within 10 seconds");
  }

  async function runMathTypesetter(element) {
    const quartoTypeset = window.Quarto?.typesetMath;
    if (typeof quartoTypeset === "function") {
      if (mathJaxIsExpected()) await waitForMathJax();
      await quartoTypeset.call(window.Quarto, element);
      return "Quarto.typesetMath";
    }

    const mathJax = await waitForMathJax();
    if (typeof mathJax?.typesetPromise === "function") {
      await mathJax.typesetPromise([element]);
      return "MathJax.typesetPromise";
    }
    if (typeof mathJax?.typeset === "function") {
      await mathJax.typeset([element]);
      return "MathJax.typeset";
    }
    throw new Error("Quarto did not provide a math typesetter and MathJax is not available");
  }

  function typesetDynamicMath(element, context = "dynamic content") {
    if (!element || !hasMath(element)) return Promise.resolve(false);
    const existing = MATH_TYPESET_STATE.get(element);
    if (existing?.status === "complete") return Promise.resolve(false);
    if (existing?.status === "pending") return existing.promise;

    const renderer = typeof window.Quarto?.typesetMath === "function"
      ? "Quarto.typesetMath"
      : "the MathJax fallback";
    const promise = runMathTypesetter(element).then(() => {
      MATH_TYPESET_STATE.set(element, { status: "complete" });
      return true;
    }).catch((error) => {
      MATH_TYPESET_STATE.delete(element);
      console.warn(
        `[Obsidian Canvas] Mathematics typesetting failed for ${context} with ${renderer}. ` +
          "The original math markup remains available.",
        error,
      );
      return false;
    });
    MATH_TYPESET_STATE.set(element, { status: "pending", promise });
    return promise;
  }

  class CanvasViewer {
    constructor(root) {
      this.root = root;
      this.scale = 1;
      this.x = 0;
      this.y = 0;
      this.drag = null;
      this.data = null;
      this.canvasUrl = null;
      this.frame = null;
      this.previewEntries = new Map();
      this.activePreviewLink = null;
      this.pointers = new Map();
      this.pinch = null;
      this.spacePressed = false;
      this.nodeTouch = null;
      this.lastNodeTap = null;
      this.suppressDblClickUntil = 0;
      this.zoomDurationMs = DEFAULT_ZOOM_DURATION_MS;
      this.transformAnimationTimer = null;
    }

    async init() {
      try {
        this.canvasUrl = new URL(this.root.dataset.ocqPath, window.location.href);
        const response = await fetch(this.canvasUrl);
        if (!response.ok) throw new Error(`request returned ${response.status}`);
        this.data = await response.json();
        if (![1, 2].includes(this.data.schemaVersion)) throw new Error("unsupported canvas schema");
        this.zoomDurationMs = zoomDuration(this.data.options?.zoomSpeed ?? 1);
        this.root.style.setProperty("--ocq-zoom-duration", `${this.zoomDurationMs}ms`);
        this.render();
        this.loadPreviews();
      } catch (error) {
        this.root.replaceChildren();
        const message = element("div", "ocq-error", { role: "alert" });
        message.textContent = `Canvas unavailable: ${error.message}`;
        this.root.append(message);
      }
    }

    render() {
      this.root.replaceChildren();
      const instanceId = `ocq-${this.data.id}-${Math.random().toString(36).slice(2)}`;
      this.instructions = element("p", "ocq-sr-only", { id: `${instanceId}-instructions` });
      this.instructions.textContent = "Use arrow keys to pan, plus and minus to zoom, F to fit, zero for one-to-one view, and Shift F for fullscreen.";
      this.root.setAttribute("aria-describedby", this.instructions.id);
      this.root.append(this.instructions);
      if (this.root.dataset.ocqControls !== "false") this.root.append(this.toolbar());
      this.viewport = element("div", "ocq-viewport");
      this.world = element("div", "ocq-world");
      const finishAnimation = (event) => {
        if (event.target === this.world && event.propertyName === "transform") {
          this.endTransformAnimation();
        }
      };
      this.world.addEventListener("transitionend", finishAnimation);
      this.groups = element("div", "ocq-groups");
      this.edges = svgElement("svg", "ocq-edges", { "aria-hidden": "true" });
      this.edgeLabels = element("div", "ocq-edge-labels", { "aria-hidden": "true" });
      this.nodes = element("div", "ocq-nodes");
      this.world.append(this.groups, this.edges, this.edgeLabels, this.nodes);
      this.viewport.append(this.world);
      this.root.append(this.viewport);
      this.previewLayer = element("div", "ocq-preview-layer", {
        hidden: "",
        "data-ocq-preview-layer": "true",
      });
      this.root.append(this.previewLayer);
      this.zoomStatus = element("span", "ocq-sr-only", {
        role: "status",
        "aria-live": "polite",
      });
      this.root.append(this.zoomStatus);
      this.renderLinearList();

      this.renderGroups();
      this.renderEdges();
      this.renderNodes();
      this.bindInteractions();
      this.bindPreviews();
      this.observer = new ResizeObserver(() => {
        if (this.root.dataset.ocqInitialView === "fit" && !this.hasInteracted) this.fit();
      });
      this.observer.observe(this.viewport);
      requestAnimationFrame(() => {
        if (this.root.dataset.ocqInitialView === "reset") this.reset();
        else this.fit();
        this.root.classList.add("ocq-ready");
      });
    }

    async loadPreviews() {
      if (this.root.dataset.ocqPreviews === "false" || !this.data.previewsUrl) return;
      this.previewsUrl = new URL(this.data.previewsUrl, this.canvasUrl).href;
      try {
        const entries = await fetchPreviewIndex(this.previewsUrl);
        Object.values(entries).forEach((entry) => {
          const pageUrl = new URL(entry.pageUrl, this.previewsUrl).href;
          this.previewEntries.set(pageUrl, entry);
        });
      } catch {
        this.previewEntries.clear();
      }
    }

    previewForLink(link) {
      if (!link || link.closest(".ocq-preview-layer")) return null;
      try {
        const url = new URL(link.href, window.location.href);
        const hash = url.hash;
        url.hash = "";
        const entry = this.previewEntries.get(url.href);
        return entry ? { entry, hash } : null;
      } catch {
        return null;
      }
    }

    bindPreviews() {
      const activate = (event) => {
        const link = event.target.closest("a[href]");
        const match = this.previewForLink(link);
        if (match) this.schedulePreview(link, match.entry, match.hash);
      };
      const deactivate = (event) => {
        if (event.relatedTarget && (
          event.relatedTarget.closest?.(".ocq-preview-layer") ||
          event.relatedTarget === this.activePreviewLink
        )) return;
        this.schedulePreviewClose();
      };
      this.root.addEventListener("mouseover", activate);
      this.root.addEventListener("focusin", activate);
      this.root.addEventListener("mouseout", deactivate);
      this.root.addEventListener("focusout", deactivate);
      this.root.addEventListener("pointerup", (event) => {
        if (event.pointerType !== "touch") return;
        const link = event.target.closest("a[href]");
        const match = this.previewForLink(link);
        if (!match || this.activePreviewLink === link) return;
        event.preventDefault();
        this.suppressTouchClick = link;
        this.showPreview(link, match.entry, match.hash);
      });
      this.root.addEventListener("click", (event) => {
        const link = event.target.closest("a[href]");
        if (link && this.suppressTouchClick === link) {
          event.preventDefault();
          this.suppressTouchClick = null;
        }
      });
      this.root.addEventListener("pointerdown", (event) => {
        if (!this.activePreviewLink) return;
        if (event.target.closest(".ocq-preview-layer") || event.target === this.activePreviewLink) return;
        this.closePreview();
      });
      this.previewLayer.addEventListener("mouseenter", () => clearTimeout(this.previewCloseTimer));
      this.previewLayer.addEventListener("mouseleave", () => this.schedulePreviewClose());
    }

    schedulePreview(link, entry, hash) {
      clearTimeout(this.previewCloseTimer);
      clearTimeout(this.previewOpenTimer);
      this.previewOpenTimer = setTimeout(
        () => this.showPreview(link, entry, hash),
        PREVIEW_DELAY,
      );
    }

    schedulePreviewClose() {
      clearTimeout(this.previewOpenTimer);
      clearTimeout(this.previewCloseTimer);
      this.previewCloseTimer = setTimeout(() => this.closePreview(), 120);
    }

    showPreview(link, entry, hash = "") {
      clearTimeout(this.previewOpenTimer);
      clearTimeout(this.previewCloseTimer);
      this.activePreviewLink = link;
      this.previewLayer.replaceChildren();
      const preview = element("aside", "ocq-preview", {
        role: "dialog",
        "aria-label": `Preview: ${entry.title}`,
      });
      const header = element("header", "ocq-preview-header");
      const pageUrl = new URL(entry.pageUrl, this.previewsUrl);
      pageUrl.hash = hash;
      const title = element("a", "ocq-preview-title", {
        href: pageUrl.href,
      });
      title.textContent = entry.title;
      header.append(title);
      const content = element("div", "ocq-preview-content");
      const fragmentUrl = new URL(entry.fragmentUrl, this.previewsUrl).href;
      const namespace = `ocq-preview-${this.data.id}`;
      content.append(safeFragment(entry.html, fragmentUrl, namespace));
      preview.append(header, content);
      this.previewLayer.append(preview);
      this.previewLayer.hidden = false;
      const rect = link.getBoundingClientRect();
      const position = previewPosition(
        rect,
        { width: PREVIEW_WIDTH, height: PREVIEW_HEIGHT },
        { width: window.innerWidth, height: window.innerHeight },
      );
      Object.assign(this.previewLayer.style, {
        left: `${position.left}px`,
        top: `${position.top}px`,
        width: `${position.width}px`,
        maxHeight: `${position.height}px`,
      });
      scrollPreviewToHash(content, hash, namespace);
      typesetDynamicMath(content, `hover preview "${entry.title}"`).then(() => {
        scrollPreviewToHash(content, hash, namespace);
      });
    }

    closePreview() {
      clearTimeout(this.previewOpenTimer);
      clearTimeout(this.previewCloseTimer);
      this.activePreviewLink = null;
      this.previewLayer.hidden = true;
      this.previewLayer.replaceChildren();
    }

    toolbar() {
      const toolbar = element("div", "ocq-toolbar", {
        role: "toolbar",
        "aria-label": "Canvas view controls",
      });
      const controls = [
        ["−", "Zoom out", () => this.zoomAt(0.82)],
        ["+", "Zoom in", () => this.zoomAt(1.22)],
        ["Fit", "Fit canvas to view", () => this.fit(true)],
        ["1:1", "Reset canvas view", () => this.reset(true)],
        ["⛶", "Enter fullscreen", () => this.toggleFullscreen()],
      ];
      controls.forEach(([label, title, action]) => {
        const button = element("button", "ocq-control", { type: "button", "aria-label": title, title });
        button.textContent = label;
        button.addEventListener("click", action);
        toolbar.append(button);
        if (title === "Enter fullscreen") {
          button.classList.add("ocq-fullscreen-control");
          button.setAttribute("aria-pressed", "false");
          this.fullscreenButton = button;
        }
      });
      return toolbar;
    }

    renderLinearList() {
      const section = element("section", "ocq-sr-only ocq-linear", {
        "aria-label": "Linear canvas contents",
      });
      const list = element("ul", "ocq-linear-list");
      (this.data.nodes || []).forEach((node) => {
        const item = element("li", "ocq-linear-item");
        const label = node.title || node.source || node.text || node.url || node.id;
        const target = node.pageUrl || node.url;
        const href = target ? safeUrl(target, this.canvasUrl) : null;
        if (href) {
          const link = element("a", "ocq-linear-link", {
            href,
          });
          link.textContent = String(label).slice(0, 160);
          item.append(link);
        } else {
          item.textContent = String(label).slice(0, 160);
        }
        list.append(item);
      });
      section.append(list);
      this.root.append(section);
    }

    renderGroups() {
      (this.data.groups || []).forEach((group) => {
        const item = element("section", "ocq-group");
        position(item, group);
        if (group.label) {
          const label = element("div", "ocq-group-label");
          label.textContent = group.label;
          item.append(label);
        }
        this.groups.append(item);
      });
    }

    renderNodes() {
      (this.data.nodes || []).forEach((node) => {
        let item;
        if (node.type === "link") {
          const href = safeUrl(node.url, this.canvasUrl);
          item = href
            ? element("a", "ocq-node ocq-node-link", { href, target: "_blank", rel: "noopener noreferrer" })
            : element("article", "ocq-node ocq-node-link ocq-node-placeholder", { "aria-label": "Unsafe link unavailable" });
          item.textContent = node.url;
        } else {
          const accessibleName = node.title || node.source || node.text?.split("\n")[0] || "Canvas note";
          item = element("article", `ocq-node ocq-node-${node.type}`, { "aria-label": accessibleName });
          if (node.fragmentUrl) {
            item.classList.add("ocq-node-rich");
            if (node.type === "file") {
              const header = element("header", "ocq-node-header");
              const title = element("strong", "ocq-node-title");
              title.textContent = node.title || (node.source || "Note").split("/").pop();
              header.append(title);
              if (node.pageUrl) {
                const action = element("a", "ocq-node-page-link", {
                  href: new URL(node.pageUrl, this.canvasUrl).href,
                  "aria-label": `Open full note: ${title.textContent}`,
                });
                action.textContent = "Open note";
                header.append(action);
              }
              item.append(header);
            }
            const content = element("div", "ocq-node-content");
            const loading = element("span", "ocq-node-loading", { role: "status" });
            loading.textContent = "Loading note…";
            content.append(loading);
            item.append(content);
            this.loadNodeFragment(content, node);
          } else if (node.type === "text") {
            const text = element("div", "ocq-node-text");
            text.textContent = node.text;
            item.append(text);
          } else if (node.display === "image" && node.asset) {
            const image = element("img", "ocq-node-image", { alt: node.source || "Canvas image", loading: "lazy" });
            image.src = new URL(node.asset, this.canvasUrl).href;
            item.append(image);
          } else {
            const kind = element("span", "ocq-file-kind");
            kind.textContent = "FILE";
            const name = element("strong", "ocq-file-name");
            name.textContent = (node.source || "Unknown file").split("/").pop();
            const path = element("span", "ocq-file-path");
            path.textContent = node.source || "Unavailable source";
            item.append(kind, name, path);
          }
        }
        item.dataset.ocqNode = node.id;
        position(item, node);
        this.nodes.append(item);
      });
    }

    async loadNodeFragment(content, node) {
      const url = new URL(node.fragmentUrl, this.canvasUrl).href;
      try {
        const markup = await fetchFragment(url);
        content.replaceChildren(safeFragment(markup, url, `ocq-${this.data.id}-${node.id}`));
        await typesetDynamicMath(content, `canvas node "${node.id}"`);
      } catch (error) {
        const message = element("div", "ocq-node-error", { role: "alert" });
        message.textContent = `Note unavailable: ${error.message}`;
        content.replaceChildren(message);
      }
    }

    renderEdges() {
      const models = new Map([...(this.data.groups || []), ...(this.data.nodes || [])].map((node) => [node.id, node]));
      const defs = svgElement("defs", "ocq-defs");
      const marker = svgElement("marker", "ocq-arrow", { id: `ocq-arrow-${this.data.id}-${Math.random().toString(36).slice(2)}`, markerWidth: "8", markerHeight: "8", refX: "7", refY: "4", orient: "auto", markerUnits: "strokeWidth" });
      marker.append(svgElement("path", "ocq-arrow-shape", { d: "M 0 0 L 8 4 L 0 8 z" }));
      defs.append(marker);
      this.edges.append(defs);
      const offsets = parallelEdgeOffsets(this.data.edges || []);
      (this.data.edges || []).forEach((edge) => {
        const source = models.get(edge.source.node);
        const target = models.get(edge.target.node);
        if (!source || !target) return;
        const sourceSide = edge.source.side || defaultSide(source, target);
        const targetSide = edge.target.side || defaultSide(target, source);
        const geometry = edgeGeometry(
          source,
          target,
          sourceSide,
          targetSide,
          offsets.get(edge.id) || 0,
        );
        const path = svgElement("path", "ocq-edge", { d: geometry.path });
        applyItemColor(path, edge.color);
        if (shouldDrawArrow(edge.target.end, true)) path.setAttribute("marker-end", `url(#${marker.id})`);
        if (shouldDrawArrow(edge.source.end)) path.setAttribute("marker-start", `url(#${marker.id})`);
        this.edges.append(path);
        if (edge.label) {
          const label = element("span", "ocq-edge-label");
          label.textContent = edge.label;
          label.style.left = `${geometry.midpoint.x}px`;
          label.style.top = `${geometry.midpoint.y}px`;
          applyItemColor(label, edge.color);
          this.edgeLabels.append(label);
        }
      });
    }

    bindInteractions() {
      this.viewport.addEventListener("pointerdown", (event) => {
        if (event.button !== 0 && event.button !== 1) return;
        const overNode = event.target.closest(".ocq-node");
        const overInteractive = event.target.closest(
          "a, button, input, textarea, select, [contenteditable=true]",
        );
        if (
          event.pointerType === "touch" &&
          overNode &&
          !overInteractive &&
          !this.spacePressed
        ) {
          this.nodeTouch = {
            pointer: event.pointerId,
            node: overNode,
            x: event.clientX,
            y: event.clientY,
            started: Date.now(),
            moved: false,
          };
        } else if (event.pointerType === "touch") {
          this.nodeTouch = null;
          this.lastNodeTap = null;
        }
        if (overNode && !this.spacePressed && event.button !== 1) return;
        this.root.focus({ preventScroll: true });
        this.hasInteracted = true;
        if (event.pointerType === "touch") {
          this.pointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
          if (this.pointers.size === 2) {
            this.pinch = {
              state: { x: this.x, y: this.y, scale: this.scale },
              points: [...this.pointers.values()].map((point) => ({ ...point })),
            };
            this.drag = null;
          }
        }
        this.drag = { pointer: event.pointerId, x: event.clientX, y: event.clientY, originX: this.x, originY: this.y };
        if (this.pinch) this.drag = null;
        this.viewport.setPointerCapture(event.pointerId);
        this.viewport.classList.add("ocq-panning");
        event.preventDefault();
      });
      this.viewport.addEventListener("pointermove", (event) => {
        if (this.nodeTouch && this.nodeTouch.pointer === event.pointerId) {
          const distance = Math.hypot(
            event.clientX - this.nodeTouch.x,
            event.clientY - this.nodeTouch.y,
          );
          if (distance > TAP_MOVE_PX) this.nodeTouch.moved = true;
        }
        if (this.pointers.has(event.pointerId)) {
          this.pointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
        }
        if (this.pinch && this.pointers.size >= 2) {
          const transform = pinchTransform(
            this.pinch.state,
            this.pinch.points,
            [...this.pointers.values()].slice(0, 2),
          );
          this.x = transform.x;
          this.y = transform.y;
          this.scale = transform.scale;
          this.scheduleTransform(false);
          event.preventDefault();
          return;
        }
        if (!this.drag || event.pointerId !== this.drag.pointer) return;
        this.x = this.drag.originX + event.clientX - this.drag.x;
        this.y = this.drag.originY + event.clientY - this.drag.y;
        this.scheduleTransform(false);
      });
      const stop = (event, cancelled = false) => {
        if (this.nodeTouch && this.nodeTouch.pointer === event.pointerId) {
          const touch = this.nodeTouch;
          this.nodeTouch = null;
          if (!cancelled && !touch.moved && Date.now() - touch.started <= DOUBLE_TAP_MS) {
            const previous = this.lastNodeTap;
            const nodeId = touch.node.dataset.ocqNode;
            if (
              previous?.nodeId === nodeId &&
              Date.now() - previous.time <= DOUBLE_TAP_MS
            ) {
              this.lastNodeTap = null;
              if (this.focusNodeElement(touch.node)) {
                this.suppressDblClickUntil = Date.now() + DOUBLE_TAP_MS;
                event.preventDefault();
                event.stopPropagation();
              }
            } else {
              this.lastNodeTap = { nodeId, time: Date.now() };
            }
          } else if (touch.moved) {
            this.lastNodeTap = null;
          }
        }
        this.pointers.delete(event.pointerId);
        if (this.pointers.size < 2) this.pinch = null;
        if (this.drag && event.pointerId === this.drag.pointer) this.drag = null;
        if (!this.drag && !this.pinch) this.viewport.classList.remove("ocq-panning");
      };
      this.viewport.addEventListener("pointerup", stop);
      this.viewport.addEventListener("pointercancel", (event) => stop(event, true));
      this.viewport.addEventListener("dblclick", (event) => {
        if (Date.now() < this.suppressDblClickUntil) return;
        const node = event.target.closest(".ocq-node");
        if (!node || event.target.closest(
          "a, button, input, textarea, select, [contenteditable=true]",
        )) return;
        if (!this.focusNodeElement(node)) return;
        event.preventDefault();
        event.stopPropagation();
      });
      this.viewport.addEventListener("wheel", (event) => {
        if (event.target.closest(".ocq-node")) return;
        event.preventDefault();
        this.hasInteracted = true;
        if (event.ctrlKey || event.metaKey) {
          const rect = this.viewport.getBoundingClientRect();
          this.zoomAt(
            Math.exp(-event.deltaY * 0.005),
            event.clientX - rect.left,
            event.clientY - rect.top,
            false,
          );
        } else {
          this.x -= event.deltaX;
          this.y -= event.deltaY;
          this.scheduleTransform(false);
        }
      }, { passive: false });
      this.root.addEventListener("keydown", (event) => this.handleKeyDown(event));
      this.root.addEventListener("keyup", (event) => {
        if (event.code === "Space") this.spacePressed = false;
      });
      if (typeof document !== "undefined") {
        document.addEventListener("fullscreenchange", () => this.handleFullscreenChange());
      }
    }

    handleKeyDown(event) {
      if (event.code === "Escape") {
        if (!this.activePreviewLink) return;
        this.closePreview();
        event.preventDefault();
        event.stopPropagation();
        return;
      }
      if (event.target.closest("input, textarea, select, [contenteditable=true], a, button")) return;
      if (event.code === "Space") {
        this.spacePressed = true;
        event.preventDefault();
        event.stopPropagation();
        return;
      }
      const panStep = event.shiftKey ? 80 : 40;
      const actions = {
        ArrowLeft: () => { this.x += panStep; },
        ArrowRight: () => { this.x -= panStep; },
        ArrowUp: () => { this.y += panStep; },
        ArrowDown: () => { this.y -= panStep; },
      };
      if (actions[event.key]) {
        actions[event.key]();
        this.hasInteracted = true;
        this.scheduleTransform(false);
        event.preventDefault();
        event.stopPropagation();
      } else if (event.key === "+" || event.key === "=") {
        this.zoomAt(1.22);
        event.preventDefault();
        event.stopPropagation();
      } else if (event.key === "-" || event.key === "_") {
        this.zoomAt(0.82);
        event.preventDefault();
        event.stopPropagation();
      } else if (event.key === "0") {
        this.reset(true);
        event.preventDefault();
        event.stopPropagation();
      } else if (event.key.toLowerCase() === "f") {
        if (event.shiftKey) this.toggleFullscreen();
        else this.fit(true);
        event.preventDefault();
        event.stopPropagation();
      }
    }

    async toggleFullscreen() {
      try {
        if (document.fullscreenElement === this.root) {
          await document.exitFullscreen();
        } else if (typeof this.root.requestFullscreen === "function") {
          await this.root.requestFullscreen();
        } else {
          throw new Error("Fullscreen is not supported by this browser");
        }
      } catch (error) {
        if (this.zoomStatus) this.zoomStatus.textContent = error.message;
      }
    }

    handleFullscreenChange() {
      const active = document.fullscreenElement === this.root;
      this.root.classList.toggle("ocq-is-fullscreen", active);
      if (this.fullscreenButton) {
        this.fullscreenButton.setAttribute("aria-pressed", String(active));
        this.fullscreenButton.setAttribute("aria-label", active ? "Exit fullscreen" : "Enter fullscreen");
        this.fullscreenButton.title = active ? "Exit fullscreen" : "Enter fullscreen";
      }
      requestAnimationFrame(() => this.fit());
    }

    zoomAt(
      factor,
      screenX = this.viewport.clientWidth / 2,
      screenY = this.viewport.clientHeight / 2,
      animated = true,
    ) {
      this.hasInteracted = true;
      const transform = zoomTransform(this, factor, screenX, screenY);
      this.scale = transform.scale;
      this.x = transform.x;
      this.y = transform.y;
      this.scheduleTransform(animated);
    }

    focusNodeElement(element) {
      const node = (this.data.nodes || []).find((item) => item.id === element.dataset.ocqNode);
      if (!node) return false;
      this.focusNode(node);
      return true;
    }

    focusNode(node) {
      this.hasInteracted = true;
      if (this.activePreviewLink) this.closePreview();
      this.root.focus({ preventScroll: true });
      const transform = focusTransform(
        node,
        this.viewport.clientWidth,
        this.viewport.clientHeight,
      );
      this.scale = transform.scale;
      this.x = transform.x;
      this.y = transform.y;
      this.scheduleTransform(true);
    }

    fit(interacted = false) {
      if (interacted) this.hasInteracted = true;
      const bounds = this.data.bounds;
      const transform = fitTransform(bounds, this.viewport.clientWidth, this.viewport.clientHeight);
      this.scale = transform.scale;
      this.x = transform.x;
      this.y = transform.y;
      this.scheduleTransform(interacted);
    }

    reset(interacted = false) {
      if (interacted) this.hasInteracted = true;
      const transform = resetTransform(
        this.data.bounds,
        this.viewport.clientWidth,
        this.viewport.clientHeight,
      );
      this.scale = transform.scale;
      this.x = transform.x;
      this.y = transform.y;
      this.scheduleTransform(interacted);
    }

    shouldAnimateTransform() {
      const reducedMotion = typeof window !== "undefined" &&
        typeof window.matchMedia === "function" &&
        window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      return this.zoomDurationMs > 0 && !reducedMotion;
    }

    beginTransformAnimation() {
      clearTimeout(this.transformAnimationTimer);
      this.world.classList.add("ocq-zoom-animating");
      this.transformAnimationTimer = setTimeout(
        () => this.endTransformAnimation(),
        this.zoomDurationMs + 50,
      );
    }

    endTransformAnimation() {
      if (!this.world) return;
      this.world.classList.remove("ocq-zoom-animating");
      clearTimeout(this.transformAnimationTimer);
      this.transformAnimationTimer = null;
    }

    scheduleTransform(animated = false) {
      if (animated && this.shouldAnimateTransform()) this.beginTransformAnimation();
      else this.endTransformAnimation();
      if (this.frame) return;
      this.frame = requestAnimationFrame(() => {
        this.frame = null;
        this.world.style.transform = `translate(${this.x}px, ${this.y}px) scale(${this.scale})`;
        if (this.zoomStatus) this.zoomStatus.textContent = `Canvas zoom ${Math.round(this.scale * 100)} percent`;
      });
    }
  }

  if (typeof module !== "undefined" && module.exports) {
    module.exports = {
      CanvasViewer,
      anchor,
      defaultSide,
      edgePath,
      edgeGeometry,
      clearFragmentCache,
      clearPreviewCache,
      fetchFragment,
      fetchPreviewIndex,
      fitTransform,
      focusTransform,
      position,
      parallelEdgeOffsets,
      pinchTransform,
      previewPosition,
      scrollPreviewToHash,
      resetTransform,
      safeFragment,
      safeUrl,
      shouldDrawArrow,
      typesetDynamicMath,
      zoomDuration,
      zoomTransform,
    };
  }

  if (typeof document === "undefined") return;

  function start() {
    document.querySelectorAll(".ocq-canvas[data-ocq-path]").forEach((root) => {
      if (root.dataset.ocqStarted) return;
      root.dataset.ocqStarted = "true";
      new CanvasViewer(root).init();
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
