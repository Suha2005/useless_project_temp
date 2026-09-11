/**
 * EXCUSE.AI // Global Application Logic
 * Audio Synthesizer (Web Audio API), Toast System, and UI Helpers
 */

class SoundEffects {
  constructor() {
    this.audioCtx = null;
    this.enabled = localStorage.getItem("excuse_sound_enabled") !== "false";
    this.updateToggleButton();
  }

  init() {
    if (!this.audioCtx && (window.AudioContext || window.webkitAudioContext)) {
      this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
  }

  toggle() {
    this.enabled = !this.enabled;
    localStorage.setItem("excuse_sound_enabled", this.enabled);
    this.updateToggleButton();
    if (this.enabled) {
      this.playBlip(600, 0.08);
      showToast("Audio feedback enabled", "success");
    } else {
      showToast("Audio feedback muted", "info");
    }
  }

  updateToggleButton() {
    const btn = document.getElementById("soundToggleBtn");
    if (btn) {
      btn.innerHTML = this.enabled ? "🔊 AUDIO ON" : "🔇 AUDIO OFF";
      btn.setAttribute("aria-label", this.enabled ? "Mute audio" : "Enable audio");
    }
  }

  playBlip(freq = 440, duration = 0.05, type = "sine") {
    if (!this.enabled) return;
    try {
      this.init();
      if (!this.audioCtx) return;
      if (this.audioCtx.state === "suspended") this.audioCtx.resume();

      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();

      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(freq * 1.5, this.audioCtx.currentTime + duration);

      gain.gain.setValueAtTime(0.04, this.audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.audioCtx.currentTime + duration);

      osc.connect(gain);
      gain.connect(this.audioCtx.destination);

      osc.start();
      osc.stop(this.audioCtx.currentTime + duration);
    } catch (e) {
      // Audio autoplay policy fallback
    }
  }

  playChime(score = 50) {
    if (!this.enabled) return;
    try {
      this.init();
      if (!this.audioCtx) return;
      if (this.audioCtx.state === "suspended") this.audioCtx.resume();

      const baseFreq = score >= 80 ? 523.25 : score >= 60 ? 392 : 220; // C5, G4, A3
      const notes = score >= 80 ? [baseFreq, baseFreq * 1.25, baseFreq * 1.5] : [baseFreq, baseFreq * 0.9];

      notes.forEach((freq, idx) => {
        const osc = this.audioCtx.createOscillator();
        const gain = this.audioCtx.createGain();

        osc.type = "triangle";
        osc.frequency.setValueAtTime(freq, this.audioCtx.currentTime + idx * 0.1);

        gain.gain.setValueAtTime(0.05, this.audioCtx.currentTime + idx * 0.1);
        gain.gain.exponentialRampToValueAtTime(0.001, this.audioCtx.currentTime + idx * 0.1 + 0.35);

        osc.connect(gain);
        gain.connect(this.audioCtx.destination);

        osc.start(this.audioCtx.currentTime + idx * 0.1);
        osc.stop(this.audioCtx.currentTime + idx * 0.1 + 0.35);
      });
    } catch (e) {}
  }
}

const SFX = new SoundEffects();

// Toast Notifications System
function showToast(message, type = "info") {
  let container = document.getElementById("toastContainer");
  if (!container) {
    container = document.createElement("div");
    container.id = "toastContainer";
    container.className = "toast-container";
    document.body.appendChild(container);
  }

  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  
  const icon = type === "error" ? "⚠" : type === "success" ? "✓" : "ℹ";
  toast.innerHTML = `<span>${icon}</span><span>${message}</span>`;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(-10px)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// Mobile Nav Toggle
document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("mobileToggle");
  const navLinks = document.getElementById("navLinks");

  if (toggleBtn && navLinks) {
    toggleBtn.addEventListener("click", () => {
      navLinks.classList.toggle("mobile-open");
      SFX.playBlip(500, 0.04);
    });
  }

  const soundBtn = document.getElementById("soundToggleBtn");
  if (soundBtn) {
    soundBtn.addEventListener("click", () => SFX.toggle());
  }

  // Interactive buttons sound trigger
  document.querySelectorAll(".btn, .prompt-chip").forEach(el => {
    el.addEventListener("mouseenter", () => SFX.playBlip(800, 0.02));
  });

  const prefill = sessionStorage.getItem("prefill_prompt");
  if (prefill) {
    const input = document.getElementById("roastInput");
    if (input) {
      input.value = prefill;
      input.dispatchEvent(new Event("input"));
    }
    sessionStorage.removeItem("prefill_prompt");
  }
});
