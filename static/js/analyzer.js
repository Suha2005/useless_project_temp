/**
 * AWKWARD OPPOSITE // Interactive Frontend Controller
 * 100% Real-Time AI Generation Engine
 */

document.addEventListener('DOMContentLoaded', () => {
  const textarea = document.getElementById('awkwardInput');
  const charCounter = document.getElementById('charCounter');
  const submitBtn = document.getElementById('submitBtn');
  const validationAlert = document.getElementById('validationAlert');
  const loader = document.getElementById('awkwardLoader');
  const loaderText = document.getElementById('loaderText');
  const resultSection = document.getElementById('resultSection');

  // Result display elements
  const diagBadge = document.getElementById('diagBadge');
  const silenceText = document.getElementById('silenceText');
  const awkwardOutput = document.getElementById('awkwardOutput');
  const oppositePlanOutput = document.getElementById('oppositePlanOutput');
  const valCringe = document.getElementById('valCringe');
  const valRuin = document.getElementById('valRuin');
  const barCringe = document.getElementById('barCringe');
  const barRuin = document.getElementById('barRuin');

  // Escalation elements
  const escalateBtn = document.getElementById('escalateBtn');
  const escalateBox = document.getElementById('escalateBox');
  const escalateAnswer = document.getElementById('escalateAnswer');
  const escalateAdvice = document.getElementById('escalateAdvice');

  // Action buttons
  const copyBtn = document.getElementById('copyBtn');
  const newBtn = document.getElementById('newBtn');
  const shameBtn = document.getElementById('shameBtn');
  const shameModal = document.getElementById('shameModal');
  const closeShameModalBtn = document.getElementById('closeShameModalBtn');
  const confirmShameBtn = document.getElementById('confirmShameBtn');
  const shameAlias = document.getElementById('shameAlias');

  let currentAnalysisId = null;
  let lastPrompt = '';
  let lastAwkwardAnswer = '';
  let loaderInterval = null;

  const loadingPhrases = [
    "Inverting social norms...",
    "Consulting the socially broken oracle...",
    "Calculating maximum eye-contact avoidance...",
    "Engineering uncomfortable silence...",
    "Discarding conventional human wisdom...",
    "Formulating the worst possible advice..."
  ];

  // Character counter
  if (textarea && charCounter) {
    textarea.addEventListener('input', () => {
      const count = textarea.value.length;
      charCounter.textContent = `${count} / 1000`;
      if (validationAlert.style.display !== 'none') {
        validationAlert.style.display = 'none';
      }
    });

    // Keyboard submit: Cmd+Enter or Ctrl+Enter
    textarea.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
        e.preventDefault();
        submitBtn.click();
      }
    });
  }

  // Submit action
  if (submitBtn) {
    submitBtn.addEventListener('click', handleAwkwardSubmit);
  }

  async function handleAwkwardSubmit() {
    const text = (textarea.value || '').trim();

    if (!text) {
      showError("You said nothing. While socially safe, it gives the Oracle nothing to invert.");
      textarea.focus();
      return;
    }

    if (text.length < 3) {
      showError("Give me a dilemma, question, or confession with slightly more detail.");
      textarea.focus();
      return;
    }

    hideError();
    startLoading();

    lastPrompt = text;

    try {
      const response = await fetch('/api/awkward', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: text })
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.error || 'Failed to generate awkward answer.');
      }

      renderResult(data);
    } catch (err) {
      showError(err.message || 'An unexpected glitch occurred.');
    } finally {
      stopLoading();
    }
  }

  function renderResult(data) {
    currentAnalysisId = data.analysis_id;
    lastAwkwardAnswer = data.awkward_answer;

    // Badges & text
    diagBadge.textContent = data.awkward_diagnosis || 'TERMINALLY AWKWARD';
    silenceText.textContent = data.awkward_silence || '14.2s of unblinking eye contact';
    awkwardOutput.textContent = data.awkward_answer;
    oppositePlanOutput.textContent = data.opposite_advice;

    // Meters
    const cringe = data.cringe_score || 94;
    const ruin = data.social_ruin || 98;

    animateValue(valCringe, 0, cringe, 1000, '%');
    animateValue(valRuin, 0, ruin, 1000, '%');

    barCringe.style.width = '0%';
    barRuin.style.width = '0%';
    setTimeout(() => {
      barCringe.style.width = `${cringe}%`;
      barRuin.style.width = `${ruin}%`;
    }, 50);

    // Reset escalation box
    escalateBox.style.display = 'none';
    escalateBtn.disabled = false;
    escalateBtn.innerHTML = '<span>💥</span> Make It Even More Awkward';

    // Show section
    resultSection.classList.add('active');
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  // Escalation: Make It Even More Awkward (Live Gemini AI)
  if (escalateBtn) {
    escalateBtn.addEventListener('click', async () => {
      escalateBtn.disabled = true;
      escalateBtn.innerHTML = '<span>⏳</span> Summoning Extinction-Level Awkwardness...';

      try {
        const response = await fetch('/api/escalate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            prompt: lastPrompt,
            previous_answer: lastAwkwardAnswer
          })
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
          throw new Error(data.error || 'Escalation failed.');
        }

        escalateAnswer.textContent = data.awkward_answer;
        escalateAdvice.textContent = data.opposite_advice;
        escalateBox.style.display = 'block';
        escalateBtn.innerHTML = '<span>💀</span> Maximum Awkwardness Reached';
        escalateBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      } catch (err) {
        showToast(err.message || 'Escalation failed.', 4000);
        escalateBtn.disabled = false;
        escalateBtn.innerHTML = '<span>💥</span> Try Escalating Again';
      }
    });
  }

  // Copy opposite plan
  if (copyBtn) {
    copyBtn.addEventListener('click', () => {
      const planText = `[AWKWARD OPPOSITE]\n\nSituation: "${lastPrompt}"\n\nOpposite Reaction:\n${awkwardOutput.textContent}\n\nBackwards Action Plan:\n${oppositePlanOutput.textContent}\n\n— via Awkward Opposite AI`;
      navigator.clipboard.writeText(planText).then(() => {
        showToast('📋 Copied awkward action plan to clipboard!');
      }).catch(() => {
        showToast('Failed to copy to clipboard.');
      });
    });
  }

  // New Dilemma
  if (newBtn) {
    newBtn.addEventListener('click', () => {
      textarea.value = '';
      charCounter.textContent = '0 / 1000';
      resultSection.classList.remove('active');
      window.scrollTo({ top: 0, behavior: 'smooth' });
      textarea.focus();
    });
  }

  // Hall of Cringe Modal
  if (shameBtn && shameModal) {
    shameBtn.addEventListener('click', () => {
      shameModal.classList.add('open');
    });

    closeShameModalBtn.addEventListener('click', () => {
      shameModal.classList.remove('open');
    });

    confirmShameBtn.addEventListener('click', async () => {
      const alias = (shameAlias.value || 'Anonymous Overthinker').trim();
      if (!currentAnalysisId) {
        showToast('No active awkward answer to publish.');
        shameModal.classList.remove('open');
        return;
      }

      confirmShameBtn.disabled = true;
      confirmShameBtn.textContent = 'Publishing...';

      try {
        const resp = await fetch('/api/wall-of-shame/submit', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            analysis_id: currentAnalysisId,
            display_name: alias
          })
        });

        const resData = await resp.json();
        if (resData.success) {
          showToast('🏆 Inducted into the Hall of Cringe!');
          shameModal.classList.remove('open');
        } else {
          showToast(resData.error || 'Failed to submit.');
        }
      } catch (err) {
        showToast('Submission error.');
      } finally {
        confirmShameBtn.disabled = false;
        confirmShameBtn.textContent = 'Publish Cringe';
      }
    });
  }

  function startLoading() {
    submitBtn.disabled = true;
    submitBtn.style.opacity = '0.6';
    resultSection.classList.remove('active');
    loader.classList.add('active');

    let idx = 0;
    loaderText.textContent = loadingPhrases[0];
    loaderInterval = setInterval(() => {
      idx = (idx + 1) % loadingPhrases.length;
      loaderText.textContent = loadingPhrases[idx];
    }, 1800);
  }

  function stopLoading() {
    submitBtn.disabled = false;
    submitBtn.style.opacity = '1';
    loader.classList.remove('active');
    if (loaderInterval) {
      clearInterval(loaderInterval);
      loaderInterval = null;
    }
  }

  function showError(msg) {
    validationAlert.textContent = msg;
    validationAlert.style.display = 'block';
  }

  function hideError() {
    validationAlert.style.display = 'none';
  }

  function animateValue(obj, start, end, duration, suffix = '') {
    let startTimestamp = null;
    const step = (timestamp) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);
      obj.innerHTML = Math.floor(progress * (end - start) + start) + suffix;
      if (progress < 1) {
        window.requestAnimationFrame(step);
      }
    };
    window.requestAnimationFrame(step);
  }

  function showToast(message, duration = 3000) {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, duration);
  }
});
