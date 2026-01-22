/**
 * AcidWiki Configuration
 * Customize your wiki by changing the values below.
 */
const CONFIG = {
    // Project Information
    projectName: "ACIDWIKI",
    projectSubtitle: "WIKI NODE",
    description: "Official Documentation and Wiki Template",

    // Versioning Settings
    // type: "github" (automatic from API) or "local" (manual)
    versioning: {
        type: "github",
        manualVersion: "v1.0.0",
        manualDate: "2026-01-21"
    },

    // GitHub Repository (for version checking when type is "github")
    // Format: "username/repo"
    repo: "infinition/Bjorn",
    branch: "wiki",

    // Theme Settings
    themes: [
        { id: "dark", name: "Dark Mode", file: "themes/dark.css", isDark: true },
        { id: "dim", name: "Dim Mode", file: "themes/light.css", isDark: true },
        { id: "electric-blue", name: "Electric Blue", file: "themes/electric-blue.css", isDark: true },
        { id: "cyberpunk", name: "Cyberpunk", file: "themes/cyberpunk.css", isDark: true },
        { id: "forest", name: "Forest", file: "themes/forest.css", isDark: true },
        { id: "monochrome", name: "Monochrome", file: "themes/monochrome.css", isDark: true },
        { id: "retro-hackers", name: "Retro Hackers", file: "themes/retro-hackers.css", isDark: true },
        { id: "retro-hackers-w", name: "Retro Hackers White", file: "themes/retro-hackers-w.css", isDark: false },
        { id: "retro-acid-burn", name: "Retro Acid Burn", file: "themes/retro-acid-burn.css", isDark: true },
        { id: "paper", name: "Paper", file: "themes/paper.css", isDark: false },
        { id: "solarized-light", name: "Solarized Light", file: "themes/solarized-light.css", isDark: false },
        { id: "nord-light", name: "Nord Light", file: "themes/nord-light.css", isDark: false },
        { id: "paper-sepia", name: "Sepia Paper", file: "themes/paper-sepia.css", isDark: false },
        { id: "paper-cool", name: "Cool Paper", file: "themes/paper-cool.css", isDark: false },
        { id: "retro-irc", name: "Retro IRC", file: "themes/retro-irc.css", isDark: false },
        { id: "nature", name: "Nature", file: "themes/nature.css", isDark: false },
        { id: "glassmorphism", name: "Glassmorphism", file: "themes/glassmorphism.css", isDark: true }
    ],
    defaultTheme: "dark",

    // Feature Toggles
    features: {
        showChangelog: true,
        showSearch: true,
        showSocialBadges: true,
        showThemeToggle: true,
        pageTransitions: true,
        autoCollapseSidebar: false
    },

    // Custom Navigation Links
    // Inserted at the top or bottom of the sidebar
    links: {
        top: [
            { name: "Main Site", url: "https://example.com", icon: "external-link" }
        ],
        bottom: [
            { name: "Portfolio", url: "https://portfolio.example.com", icon: "briefcase" },
            { name: "Store", url: "https://store.example.com", icon: "shopping-cart" }
        ]
    },

    // Footer Customization
    footerText: "© 2026 ACIDWIKI - All rights reserved",

    // UI Strings (Custom labels for the interface)
    ui: {
        joinUsTitle: ":: JOIN US ::",
        onThisPageTitle: "On this page",
        changelogTitle: "Changelog",
        searchPlaceholder: "Search (Ctrl+K)...",
        lastUpdatedText: "Updated",
        readingTimePrefix: "~",
        readingTimeSuffix: "min read",
        noResultsText: "No results found.",
        noSectionsText: "No sections",
        fetchingReleasesText: "Fetching GitHub releases...",
        checkingVersionText: "checking...",
        initializingText: "Initializing...",
        themeChangedText: "Theme changed to: ",
        menuText: "Menu",
        onThisPageMobile: "On this page"
    },

    // Logo Settings
    logoPath: "assets/bjorn.png",
    logoPlaceholder: "https://placehold.co/40x40/111214/22c55e?text=A",

    // Social Links
    // Set to null or empty string to hide the link
    social: {
        discord: "https://discord.gg/B3ZH9taVfT",
        reddit: "https://www.reddit.com/r/Bjorn_CyberViking/",
        github: "https://github.com/infinition/Bjorn",
        buyMeACoffee: "https://buymeacoffee.com/infinition"
    },

    // Badge Labels (Optional customization for shields.io)
    badges: {
        discordLabel: "COMMUNITY",
        redditLabel: "r/ACIDWIKI",
        githubLabel: "ACIDWIKI"
    }
};
