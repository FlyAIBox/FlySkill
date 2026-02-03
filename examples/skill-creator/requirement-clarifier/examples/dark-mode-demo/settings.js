/**
 * 设置页面专用脚本
 * 处理设置页面的交互逻辑
 */

// 等待 DOM 加载完成
document.addEventListener('DOMContentLoaded', function() {
    initializeSettings();
});

/**
 * 初始化设置页面
 */
function initializeSettings() {
    // 初始化夜间模式开关
    initializeDarkModeToggle();

    // 初始化其他设置项（示例）
    initializeNotificationToggle();
    initializeAutoSaveToggle();
}

/**
 * 初始化夜间模式开关
 */
function initializeDarkModeToggle() {
    const darkModeToggle = document.getElementById('darkModeToggle');

    if (darkModeToggle) {
        // 根据当前主题设置开关状态
        darkModeToggle.checked = themeManager.isDarkMode();

        // 监听开关变化
        darkModeToggle.addEventListener('change', function() {
            if (this.checked) {
                themeManager.enableDarkMode();
                showNotification('已开启夜间模式 🌙');
            } else {
                themeManager.disableDarkMode();
                showNotification('已关闭夜间模式 ☀️');
            }
        });
    }
}

/**
 * 初始化通知开关（示例）
 */
function initializeNotificationToggle() {
    const notificationToggle = document.getElementById('notificationToggle');

    if (notificationToggle) {
        // 从 localStorage 读取设置
        const notificationEnabled = localStorage.getItem('notification') === 'true';
        notificationToggle.checked = notificationEnabled;

        // 监听变化
        notificationToggle.addEventListener('change', function() {
            localStorage.setItem('notification', this.checked);
            showNotification(this.checked ? '已开启通知' : '已关闭通知');
        });
    }
}

/**
 * 初始化自动保存开关（示例）
 */
function initializeAutoSaveToggle() {
    const autoSaveToggle = document.getElementById('autoSaveToggle');

    if (autoSaveToggle) {
        // 从 localStorage 读取设置
        const autoSaveEnabled = localStorage.getItem('autoSave') !== 'false'; // 默认开启
        autoSaveToggle.checked = autoSaveEnabled;

        // 监听变化
        autoSaveToggle.addEventListener('change', function() {
            localStorage.setItem('autoSave', this.checked);
            showNotification(this.checked ? '已开启自动保存' : '已关闭自动保存');
        });
    }
}

/**
 * 显示通知提示
 * @param {string} message - 通知消息
 */
function showNotification(message) {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = 'notification-toast';
    notification.textContent = message;

    // 添加到页面
    document.body.appendChild(notification);

    // 触发动画
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);

    // 3秒后移除
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}
