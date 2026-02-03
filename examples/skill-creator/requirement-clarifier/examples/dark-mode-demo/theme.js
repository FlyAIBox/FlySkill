/**
 * 主题管理模块
 * 负责处理夜间模式的初始化、切换和状态持久化
 */

// Theme Manager Class
class ThemeManager {
    constructor() {
        this.storageKey = 'theme';
        this.darkModeClass = 'dark-mode';
        this.init();
    }

    /**
     * 初始化主题
     * 从 localStorage 读取用户偏好，如果没有则默认为浅色模式
     */
    init() {
        const savedTheme = this.getSavedTheme();

        if (savedTheme === 'dark') {
            this.enableDarkMode();
        } else {
            this.disableDarkMode();
        }

        // 更新所有页面的主题状态显示
        this.updateThemeStatus();
    }

    /**
     * 从 localStorage 获取保存的主题
     * @returns {string} 'dark' 或 'light'
     */
    getSavedTheme() {
        try {
            return localStorage.getItem(this.storageKey) || 'light';
        } catch (error) {
            console.error('无法读取主题设置:', error);
            return 'light';
        }
    }

    /**
     * 保存主题到 localStorage
     * @param {string} theme - 'dark' 或 'light'
     */
    saveTheme(theme) {
        try {
            localStorage.setItem(this.storageKey, theme);
        } catch (error) {
            console.error('无法保存主题设置:', error);
        }
    }

    /**
     * 启用深色模式
     */
    enableDarkMode() {
        document.body.classList.add(this.darkModeClass);
        this.saveTheme('dark');
        this.updateThemeStatus();

        // 更新 toggle 开关状态（如果在设置页面）
        const toggle = document.getElementById('darkModeToggle');
        if (toggle) {
            toggle.checked = true;
        }
    }

    /**
     * 禁用深色模式
     */
    disableDarkMode() {
        document.body.classList.remove(this.darkModeClass);
        this.saveTheme('light');
        this.updateThemeStatus();

        // 更新 toggle 开关状态（如果在设置页面）
        const toggle = document.getElementById('darkModeToggle');
        if (toggle) {
            toggle.checked = false;
        }
    }

    /**
     * 切换主题
     */
    toggleTheme() {
        if (document.body.classList.contains(this.darkModeClass)) {
            this.disableDarkMode();
        } else {
            this.enableDarkMode();
        }
    }

    /**
     * 更新主题状态显示
     */
    updateThemeStatus() {
        const statusElement = document.getElementById('currentTheme');
        if (statusElement) {
            const isDark = document.body.classList.contains(this.darkModeClass);
            statusElement.textContent = isDark ? '深色模式' : '浅色模式';
        }
    }

    /**
     * 获取当前主题状态
     * @returns {boolean} 是否为深色模式
     */
    isDarkMode() {
        return document.body.classList.contains(this.darkModeClass);
    }
}

// 创建全局主题管理器实例
const themeManager = new ThemeManager();

// 导出供其他模块使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ThemeManager, themeManager };
}
