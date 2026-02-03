# 夜间模式演示项目

这是一个使用原生 HTML/CSS/JavaScript 实现的完整夜间模式演示项目。

## 功能特性

✅ **全局主题切换** - 通过 CSS Dark Class 实现，一键切换深色/浅色模式
✅ **状态持久化** - 使用 localStorage 保存用户偏好，刷新页面后保持
✅ **平滑过渡动画** - 所有主题切换都有流畅的过渡效果
✅ **响应式设计** - 支持桌面和移动设备
✅ **纯原生实现** - 不依赖任何框架或库

## 文件结构

```
dark-mode-demo/
├── index.html      # 首页
├── settings.html   # 设置页面（包含夜间模式开关）
├── about.html      # 关于页面
├── styles.css      # 全局样式（包含深色/浅色主题）
├── theme.js        # 主题管理模块
└── settings.js     # 设置页面交互逻辑
```

## 使用方法

1. 在浏览器中打开 `index.html`
2. 点击导航栏的"设置"进入设置页面
3. 点击"夜间模式"开关切换主题
4. 刷新页面，主题设置会保持

## 技术实现

### CSS Dark Class 方案

通过切换 `body` 元素的 `dark-mode` class 来控制全局主题：

```css
/* 浅色模式 */
body {
    --bg-primary: #ffffff;
    --text-primary: #333333;
}

/* 深色模式 */
body.dark-mode {
    --bg-primary: #1a1a1a;
    --text-primary: #e0e0e0;
}
```

### localStorage 持久化

```javascript
// 保存主题
localStorage.setItem('theme', 'dark');

// 读取主题
const theme = localStorage.getItem('theme');
```

## 验收标准

- [x] 设置页面正常显示，包含夜间模式 Toggle 开关
- [x] 点击开关时，页面所有元素立即切换到深色/浅色主题
- [x] 刷新页面后，保持用户上次选择的主题
- [x] 深色模式下，所有文字、背景、边框等元素对比度良好
- [x] Toggle 开关状态与当前主题同步

## 浏览器兼容性

- Chrome/Edge: ✅ 完全支持
- Firefox: ✅ 完全支持
- Safari: ✅ 完全支持
- Opera: ✅ 完全支持

## 核心代码说明

### ThemeManager 类

`theme.js` 文件中定义了 `ThemeManager` 类，负责：

- 初始化主题（从 localStorage 读取）
- 启用/禁用深色模式
- 切换主题
- 更新主题状态显示
- 保存主题设置到 localStorage

### Toggle 开关

设置页面使用纯 CSS 实现的 Toggle 开关：

```html
<label class="toggle-switch">
    <input type="checkbox" id="darkModeToggle">
    <span class="toggle-slider"></span>
</label>
```

### 平滑过渡

所有颜色变化都添加了 0.3s 的过渡动画：

```css
body {
    transition: background-color 0.3s ease, color 0.3s ease;
}
```

## 扩展建议

如需进一步扩展，可以考虑：

1. 添加系统主题跟随（使用 `prefers-color-scheme` 媒体查询）
2. 添加更多主题选项（如高对比度模式）
3. 添加主题切换动画效果
4. 添加主题预览功能
