/**
 * Provena Digital Assets - Theme Manager
 * Handles light/dark theme switching with system preference detection
 * and localStorage persistence
 *
 * Version: 1.0.0
 */

(function() {
  'use strict';

  // Configuration
  const CONFIG = {
    STORAGE_KEY: 'provena-theme',
    DARK_CLASS: 'dark',
    THEME_ATTRIBUTE: 'data-theme',
    DEFAULT_THEME: 'light', // Default to light theme, user can toggle to dark
    TOGGLE_SELECTOR: '#theme-toggle',
    SUN_ICON_CLASS: '.sun-icon',
    MOON_ICON_CLASS: '.moon-icon',
    TRANSITION_DURATION: 300
  };

  // State
  let currentTheme = null;
  let isInitialized = false;

  /**
   * Get system color scheme preference
   * @returns {string} 'dark' or 'light'
   */
  function getSystemPreference() {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    return 'light';
  }

  /**
   * Get saved theme from localStorage
   * @returns {string|null}
   */
  function getSavedTheme() {
    try {
      return localStorage.getItem(CONFIG.STORAGE_KEY);
    } catch (e) {
      console.warn('ProvenaTheme: Unable to access localStorage', e);
      return null;
    }
  }

  /**
   * Save theme preference to localStorage
   * @param {string} theme - 'dark' or 'light'
   */
  function saveTheme(theme) {
    try {
      localStorage.setItem(CONFIG.STORAGE_KEY, theme);
    } catch (e) {
      console.warn('ProvenaTheme: Unable to save to localStorage', e);
    }
  }

  /**
   * Apply theme to document
   * @param {string} theme - 'dark' or 'light'
   * @param {boolean} animate - Whether to animate the transition
   */
  function applyTheme(theme, animate = true) {
    const body = document.body;
    const html = document.documentElement;

    // Prevent transition on initial load
    if (!animate) {
      body.style.transition = 'none';
      html.style.transition = 'none';
    }

    if (theme === 'dark') {
      body.classList.add(CONFIG.DARK_CLASS);
      html.classList.add(CONFIG.DARK_CLASS);
      html.setAttribute(CONFIG.THEME_ATTRIBUTE, 'dark');
    } else {
      body.classList.remove(CONFIG.DARK_CLASS);
      html.classList.remove(CONFIG.DARK_CLASS);
      html.setAttribute(CONFIG.THEME_ATTRIBUTE, 'light');
    }

    currentTheme = theme;

    // Update toggle button icons
    updateToggleIcon(theme);

    // Handle INSPIRO framework dark theme (for data-dark-src images)
    handleINSPIROTheme(theme);

    // Re-enable transitions
    if (!animate) {
      requestAnimationFrame(() => {
        body.style.transition = '';
        html.style.transition = '';
      });
    }

    // Dispatch custom event for other scripts to listen to
    window.dispatchEvent(new CustomEvent('themechange', {
      detail: { theme: theme }
    }));
  }

  /**
   * Update toggle button icon visibility
   * @param {string} theme - 'dark' or 'light'
   */
  function updateToggleIcon(theme) {
    const toggles = document.querySelectorAll(CONFIG.TOGGLE_SELECTOR);

    toggles.forEach(toggle => {
      const sunIcon = toggle.querySelector(CONFIG.SUN_ICON_CLASS);
      const moonIcon = toggle.querySelector(CONFIG.MOON_ICON_CLASS);

      if (theme === 'dark') {
        // In dark mode, show sun icon (to switch to light)
        if (sunIcon) sunIcon.style.display = 'block';
        if (moonIcon) moonIcon.style.display = 'none';
        toggle.setAttribute('aria-label', 'Switch to light mode');
        toggle.setAttribute('title', 'Switch to light mode');
      } else {
        // In light mode, show moon icon (to switch to dark)
        if (sunIcon) sunIcon.style.display = 'none';
        if (moonIcon) moonIcon.style.display = 'block';
        toggle.setAttribute('aria-label', 'Switch to dark mode');
        toggle.setAttribute('title', 'Switch to dark mode');
      }
    });
  }

  /**
   * Handle INSPIRO framework theme integration
   * Swaps images with data-dark-src attribute
   * @param {string} theme - 'dark' or 'light'
   */
  function handleINSPIROTheme(theme) {
    // Handle images with data-dark-src attribute
    const darkImages = document.querySelectorAll('[data-dark-src]');

    darkImages.forEach(img => {
      const darkSrc = img.getAttribute('data-dark-src');
      const lightSrc = img.getAttribute('data-light-src') || img.getAttribute('data-original-src');

      // Store original src if not already stored
      if (!img.getAttribute('data-original-src')) {
        img.setAttribute('data-original-src', img.src);
      }

      if (theme === 'dark' && darkSrc) {
        img.src = darkSrc;
      } else if (theme === 'light' && lightSrc) {
        img.src = lightSrc;
      } else if (theme === 'light') {
        img.src = img.getAttribute('data-original-src');
      }
    });

    // Integrate with existing INSPIRO darkTheme function if available
    if (window.INSPIRO && INSPIRO.core && typeof INSPIRO.core.darkTheme === 'function') {
      // INSPIRO uses cookies, we use localStorage - sync them
      if (typeof Cookies !== 'undefined') {
        Cookies.set('darkColorScheme', theme === 'dark' ? 'true' : 'false');
      }
    }
  }

  /**
   * Toggle between light and dark themes
   */
  function toggleTheme() {
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme, true);
    saveTheme(newTheme);
  }

  /**
   * Set up event listeners for toggle buttons
   */
  function setupToggleListeners() {
    const toggles = document.querySelectorAll(CONFIG.TOGGLE_SELECTOR);

    toggles.forEach(toggle => {
      // Remove existing listeners to prevent duplicates
      toggle.removeEventListener('click', toggleTheme);
      toggle.addEventListener('click', toggleTheme);

      // Keyboard accessibility
      toggle.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          toggleTheme();
        }
      });
    });
  }

  /**
   * Set up system preference change listener
   */
  function setupSystemPreferenceListener() {
    if (window.matchMedia) {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

      const handleChange = (e) => {
        // Only auto-switch if user hasn't manually set a preference
        if (!getSavedTheme()) {
          applyTheme(e.matches ? 'dark' : 'light', true);
        }
      };

      // Modern browsers
      if (mediaQuery.addEventListener) {
        mediaQuery.addEventListener('change', handleChange);
      } else if (mediaQuery.addListener) {
        // Older browsers
        mediaQuery.addListener(handleChange);
      }
    }
  }

  /**
   * Initialize the theme manager
   */
  function init() {
    if (isInitialized) return;

    // Determine initial theme
    const savedTheme = getSavedTheme();
    const initialTheme = savedTheme || CONFIG.DEFAULT_THEME;

    // Apply theme immediately without animation to prevent flash
    applyTheme(initialTheme, false);

    // Set up listeners when DOM is ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => {
        setupToggleListeners();
        setupSystemPreferenceListener();
      });
    } else {
      setupToggleListeners();
      setupSystemPreferenceListener();
    }

    isInitialized = true;
  }

  // Initialize immediately to prevent flash of wrong theme
  init();

  // Re-initialize toggle listeners after AJAX content loads
  document.addEventListener('contentLoaded', setupToggleListeners);
  document.addEventListener('ajaxComplete', setupToggleListeners);

  // Expose public API
  window.ProvenaTheme = {
    /**
     * Toggle between light and dark themes
     */
    toggle: toggleTheme,

    /**
     * Set a specific theme
     * @param {string} theme - 'dark' or 'light'
     */
    setTheme: function(theme) {
      if (theme === 'dark' || theme === 'light') {
        applyTheme(theme, true);
        saveTheme(theme);
      }
    },

    /**
     * Get the current theme
     * @returns {string} 'dark' or 'light'
     */
    getTheme: function() {
      return currentTheme;
    },

    /**
     * Check if dark mode is active
     * @returns {boolean}
     */
    isDark: function() {
      return currentTheme === 'dark';
    },

    /**
     * Check if light mode is active
     * @returns {boolean}
     */
    isLight: function() {
      return currentTheme === 'light';
    },

    /**
     * Clear saved preference and use system preference
     */
    useSystemPreference: function() {
      try {
        localStorage.removeItem(CONFIG.STORAGE_KEY);
      } catch (e) {}
      applyTheme(getSystemPreference(), true);
    },

    /**
     * Re-initialize toggle button listeners
     * Useful after dynamically adding content
     */
    refresh: setupToggleListeners
  };

})();

/**
 * Language Selector Dropdown
 */
(function() {
  'use strict';

  function initLanguageDropdown() {
    const langToggle = document.getElementById('lang-toggle');
    const langDropdown = langToggle ? langToggle.closest('.language-dropdown') : null;
    const langMenu = document.getElementById('lang-menu');

    if (!langToggle || !langDropdown || !langMenu) return;

    // Toggle dropdown
    langToggle.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      langDropdown.classList.toggle('open');
    });

    // Close on click outside
    document.addEventListener('click', function(e) {
      if (!langDropdown.contains(e.target)) {
        langDropdown.classList.remove('open');
      }
    });

    // Close on Escape key
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        langDropdown.classList.remove('open');
      }
    });

    // Close after language selection
    langMenu.querySelectorAll('a').forEach(function(link) {
      link.addEventListener('click', function() {
        langDropdown.classList.remove('open');
        // Update label to show selected language
        const langLabel = langToggle.querySelector('.lang-label');
        if (langLabel) {
          const langMap = {
            'en|en': 'EN',
            'en|fr': 'FR',
            'en|de': 'DE',
            'en|es': 'ES',
            'en|it': 'IT',
            'en|pt': 'PT',
            'en|ru': 'RU',
            'en|zh-CN': '中文',
            'en|ar': 'AR'
          };
          const onclick = link.getAttribute('onclick') || '';
          const match = onclick.match(/doGTranslate\('([^']+)'\)/);
          if (match && langMap[match[1]]) {
            langLabel.textContent = langMap[match[1]];
          }
        }
      });
    });
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLanguageDropdown);
  } else {
    initLanguageDropdown();
  }
})();
