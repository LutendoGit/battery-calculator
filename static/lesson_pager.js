(function () {
  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function parseStepIndex(paramName, stepCount) {
    try {
      var params = new URLSearchParams(window.location.search);
      var raw = params.get(paramName);
      if (!raw) return 0;
      var step = parseInt(raw, 10);
      if (!Number.isFinite(step)) return 0;
      return clamp(step - 1, 0, Math.max(0, stepCount - 1));
    } catch (e) {
      return 0;
    }
  }

  function writeStepIndex(paramName, index) {
    try {
      var params = new URLSearchParams(window.location.search);
      params.set(paramName, String(index + 1));
      var nextUrl = window.location.pathname + "?" + params.toString();
      window.history.replaceState(null, "", nextUrl);
    } catch (e) {
      // ignore
    }
  }

  function init(options) {
    options = options || {};

    var paramName = options.paramName || "step";
    var doneUrl = options.doneUrl || "";
    var nextLabel = options.nextLabel || "Next";
    var prevLabel = options.prevLabel || "Previous";
    var doneLabel = options.doneLabel || "Done";
    var lessonKey = options.lessonKey || "";
    var progressEndpoint = options.progressEndpoint || "";
    var trackedSteps = Object.create(null);

    var steps = Array.prototype.slice.call(document.querySelectorAll("[data-lesson-step]"));
    if (!steps.length) return;

    var prevBtn = document.querySelector("[data-lesson-prev]");
    var nextBtn = document.querySelector("[data-lesson-next]");
    var titleEl = document.querySelector("[data-lesson-title]");
    var counterEl = document.querySelector("[data-lesson-counter]");
    var stageEl = document.querySelector("[data-lesson-stage]");

    if (prevBtn) prevBtn.textContent = prevLabel;

    var index = parseStepIndex(paramName, steps.length);

    function trackCurrentStep() {
      if (!lessonKey || !progressEndpoint) return;

      var stepNumber = index + 1;
      if (trackedSteps[stepNumber]) return;
      trackedSteps[stepNumber] = true;

      try {
        fetch(progressEndpoint, {
          method: "POST",
          credentials: "same-origin",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            lesson_key: lessonKey,
            step: stepNumber,
            total_steps: steps.length,
          }),
          keepalive: true,
        }).then(function (resp) {
          if (!resp.ok) trackedSteps[stepNumber] = false;
        }).catch(function () {
          trackedSteps[stepNumber] = false;
        });
      } catch (e) {
        trackedSteps[stepNumber] = false;
      }
    }

    function render() {
      for (var i = 0; i < steps.length; i++) {
        var active = i === index;
        steps[i].hidden = !active;
        steps[i].setAttribute("aria-hidden", active ? "false" : "true");
      }

      if (titleEl) {
        titleEl.textContent = steps[index].getAttribute("data-step-title") || "";
      }

      if (counterEl) {
        counterEl.textContent = String(index + 1) + " / " + String(steps.length);
      }

      if (prevBtn) prevBtn.disabled = index === 0;

      if (nextBtn) {
        if (index >= steps.length - 1) {
          nextBtn.textContent = doneLabel;
        } else {
          nextBtn.textContent = nextLabel;
        }
      }

      trackCurrentStep();

      if (stageEl) stageEl.scrollTop = 0;
      window.scrollTo(0, 0);
    }

    function go(toIndex) {
      index = clamp(toIndex, 0, steps.length - 1);
      writeStepIndex(paramName, index);
      render();
    }

    var controller = {
      get stepCount() {
        return steps.length;
      },
      get index() {
        return index;
      },
      goToIndex: function (toIndex) {
        go(toIndex);
      },
      goToStep: function (step1Based) {
        var n = parseInt(step1Based, 10);
        if (!Number.isFinite(n)) return;
        go(n - 1);
      },
      next: function () {
        go(index + 1);
      },
      prev: function () {
        go(index - 1);
      },
    };

    function isEditableTarget(target) {
      try {
        if (!target) return false;
        var tag = (target.tagName || "").toLowerCase();
        if (tag === "input" || tag === "textarea" || tag === "select") return true;
        if (target.isContentEditable) return true;
        return false;
      } catch (e) {
        return false;
      }
    }

    function handleKeydown(e) {
      if (!e) return;
      if (e.defaultPrevented) return;
      if (e.altKey || e.ctrlKey || e.metaKey) return;
      if (isEditableTarget(e.target)) return;

      var key = e.key;
      var code = e.code;

      // Next
      if (
        key === "ArrowRight" ||
        key === "PageDown" ||
        key === "BrowserForward" ||
        code === "ArrowRight" ||
        code === "PageDown"
      ) {
        e.preventDefault();
        controller.next();
        return;
      }

      // Previous
      if (
        key === "ArrowLeft" ||
        key === "PageUp" ||
        key === "BrowserBack" ||
        code === "ArrowLeft" ||
        code === "PageUp"
      ) {
        e.preventDefault();
        controller.prev();
        return;
      }
    }

    if (prevBtn) {
      prevBtn.addEventListener("click", function () {
        go(index - 1);
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", function () {
        if (index >= steps.length - 1) {
          if (doneUrl) window.location.href = doneUrl;
          return;
        }
        go(index + 1);
      });
    }

    // Keyboard navigation (works across all lesson pages)
    document.addEventListener("keydown", handleKeydown);

    // Ensure URL is normalized to include step=1 on first load
    writeStepIndex(paramName, index);
    render();

    window.LessonPager._controller = controller;
    return controller;
  }

  window.LessonPager = {
    init: init,
    get controller() {
      return window.LessonPager._controller;
    },
  };
})();
