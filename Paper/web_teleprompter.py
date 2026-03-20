from flask import Flask, render_template_string, request
from pathlib import Path

app = Flask(__name__)

# ===== 配置你的论文目录 =====
BASE_DIR = Path("/Users/adam/Library/Mobile Documents/com~apple~CloudDocs/Documents/高项相关/论文2026")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>提词器</title>
<style>
body {
    margin: 0;
    background: #000;
    color: #fff;
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif;
    overflow: hidden;
}

#container {
    position: absolute;
    width: 60%;
    left: 50%;
    transform: translateX(-50%);
    bottom: -100%;
    font-size: 40px;
    line-height: 1.8;
    text-align: center;
    letter-spacing: 1px;
    will-change: transform;
}

#menu {
    position: fixed;
    top: 15px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 999;
}

select {
    font-size: 18px;
    padding: 8px 12px;
    border-radius: 8px;
    border: none;
    background: rgba(255,255,255,0.1);
    color: #fff;
}

/* 渐隐效果 */
body::before,
body::after {
    content: "";
    position: fixed;
    left: 0;
    width: 100%;
    height: 120px;
    z-index: 10;
    pointer-events: none;
}

body::before {
    top: 0;
    background: linear-gradient(to bottom, black, transparent);
}

body::after {
    bottom: 0;
    background: linear-gradient(to top, black, transparent);
}

/* 中间高亮区域 */
#focus-line {
    position: fixed;
    top: 50%;
    left: 0;
    width: 100%;
    height: 80px;
    margin-top: -40px;
    border-top: 2px solid rgba(255,255,255,0.2);
    border-bottom: 2px solid rgba(255,255,255,0.2);
    pointer-events: none;
}

.sentence {
    display: block;
    opacity: 0.3;
    transform: scale(0.95);
    transition: opacity 0.35s ease, transform 0.35s ease;
}

.sentence.focus {
    opacity: 1;
    transform: scale(1.12);
    color: #ffffff;
    background: rgba(255,255,255,0.08);
    border-radius: 10px;
}

.sentence.active {
    opacity: 1;
    transform: scale(1.05);
    font-size: 48px;
    text-shadow: 0 0 10px rgba(255,255,255,0.8), 0 0 20px rgba(255,255,255,0.6);
}
.sentence.near {
    opacity: 0.6;
    transform: scale(1.0);
}

@keyframes glowPulse {
    0% { text-shadow: 0 0 6px rgba(255,255,255,0.6); }
    50% { text-shadow: 0 0 18px rgba(255,255,255,1); }
    100% { text-shadow: 0 0 6px rgba(255,255,255,0.6); }
}

.sentence.active {
    animation: glowPulse 2s ease-in-out infinite;
}

button {
    margin-left: 8px;
    padding: 6px 12px;
    border-radius: 6px;
    border: none;
    background: rgba(255,255,255,0.1);
    color: #fff;
    cursor: pointer;
    transition: all 0.2s;
}

button:hover {
    background: rgba(255,255,255,0.3);
}
#speedDisplay {
    margin-left: 8px;
    font-size: 18px;
    vertical-align: middle;
    color: #fff;
}
</style>
</head>
<body>
<div id="menu">
<form method="post" style="display:inline-block;">
<select name="filename" onchange="this.form.submit()">
{% for f in files %}
<option value="{{f}}" {% if f == current %}selected{% endif %}>{{f}}</option>
{% endfor %}
</select>
</form>

<button onclick="resetScroll()">重置</button>
<button id="pauseBtn" onclick="togglePause()">暂停</button>
<button onclick="prevSentence()">上一句</button>
<button onclick="nextSentence()">下一句</button>
<button onclick="increaseSpeed()">+</button>
<button onclick="decreaseSpeed()">-</button>
<span id="speedDisplay">1.0x</span>
</div>

<div id="container"></div>
<script id="raw-text" type="text/plain">{{ text | safe }}</script>
<div id="focus-line"></div>

<script>
let speed = 0.8;
let container = document.getElementById('container');

// ===== 文本拆句（核心升级） =====
let raw = document.getElementById('raw-text').innerText;
let sentences = raw.split(/(?<=[，。！？])/);

function formatSentence(s) {
    if (s.length > 24) {
        return s.replace(/(.{20})/g, '$1<br>');
    }
    return s;
}

container.innerHTML = sentences.map(s => `<div class="sentence">${formatSentence(s)}</div>`).join('');

let offsetY = 0;
container.style.transform = `translate3d(-50%, ${offsetY}px, 0)`;
// 初始将第一句居中
setTimeout(() => {
    scrollToSentence(0);
}, 0);

let sentenceNodes = document.querySelectorAll('.sentence');

// 🔥 预计算每一句的中心位置（彻底消灭抖动）
let sentencePositions = [];
function computePositions() {
    sentencePositions = [];
    let total = 0;
    sentenceNodes.forEach(node => {
        let h = node.offsetHeight;
        sentencePositions.push(total + h / 2);
        total += h;
    });
}

computePositions();
window.addEventListener('resize', computePositions);

let currentIndex = 0;
let lastIndex = -1;
let pauseTimer = 0;

function updateHighlight() {
    const focusTop = window.innerHeight / 2 - 40;   // 上边线
    const focusBottom = window.innerHeight / 2 + 40; // 下边线

    sentenceNodes.forEach((node, idx) => {
        const rect = node.getBoundingClientRect();
        const center = rect.top + rect.height / 2;

        node.classList.remove('focus');

        // ⭐ 判断是否在两条线之间
        if (center >= focusTop && center <= focusBottom) {
            node.classList.add('focus');
        }
    });
}

// 手机滑动控制速度（核心升级）
let startY = 0;
document.addEventListener('touchstart', (e) => {
    startY = e.touches[0].clientY;
});

document.addEventListener('touchmove', (e) => {
    let delta = startY - e.touches[0].clientY;
    speed += delta * 0.002;
    speed = Math.max(0.05, Math.min(3, speed));
    startY = e.touches[0].clientY;
});

// 暂停状态
let paused = false;

function togglePause() {
    paused = !paused;
    let btn = document.getElementById('pauseBtn');
    btn.innerText = paused ? '继续' : '暂停';
}

let frameCount = 0;
let lastTime = performance.now();

function scrollText(now) {
    let deltaTime = (now - lastTime) / 16; // 标准化到60fps
    lastTime = now;

    if (!paused) {
        if (pauseTimer > 0) {
            pauseTimer -= 16 * deltaTime;
            // 暂停时完全停止（避免抖动）
            window.currentVelocity = 0;
        } else {
            // ✅ 简化为稳定连续滚动（核心修复）
            if (!window.currentVelocity) window.currentVelocity = speed;
            // 轻微加速到目标速度（不会抖）
            window.currentVelocity += (speed - window.currentVelocity) * 0.08 * deltaTime;
            offsetY -= window.currentVelocity * deltaTime;
        }
        container.style.transform = `translate3d(-50%, ${offsetY}px, 0)`;
    }

    frameCount++;
    if (frameCount % 6 === 0) {
        updateHighlight();
    }

    requestAnimationFrame(scrollText);
}

window.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowUp') speed += 0.1;
    if (e.key === 'ArrowDown') speed = Math.max(0.1, speed - 0.1);
});
updateHighlight();

function animateTo(targetOffset, duration = 300) {
    let start = offsetY;
    let startTime = null;

    function step(timestamp) {
        if (!startTime) startTime = timestamp;
        let progress = (timestamp - startTime) / duration;
        progress = Math.min(progress, 1);

        // easeOut
        let ease = 1 - Math.pow(1 - progress, 3);
        offsetY = start + (targetOffset - start) * ease;
        container.style.transform = `translate3d(-50%, ${offsetY}px, 0)`;

        if (progress < 1) {
            requestAnimationFrame(step);
        }
    }

    requestAnimationFrame(step);
}

function scrollToSentence(index) {
    if (index < 0 || index >= sentenceNodes.length) return;

    let target = sentenceNodes[index];
    let rect = target.getBoundingClientRect();
    let center = window.innerHeight / 2;
    let delta = center - (rect.top + rect.height / 2);

    let targetOffset = offsetY + delta;
    animateTo(targetOffset);
}

function resetScroll() {
    currentIndex = 0;
    offsetY = 0;
    container.style.transform = `translate3d(-50%, ${offsetY}px, 0)`;
    // 居中到第一句
    scrollToSentence(0);
}

function prevSentence() {
    scrollToSentence(currentIndex - 1);
}

function nextSentence() {
    scrollToSentence(currentIndex + 1);
}

function updateSpeedDisplay() {
    document.getElementById('speedDisplay').innerText = speed.toFixed(2) + 'x';
}

function increaseSpeed() {
    speed = Math.min(3, speed + 0.2);
    updateSpeedDisplay();
}

function decreaseSpeed() {
    speed = Math.max(0.1, speed - 0.2);
    updateSpeedDisplay();
}

updateSpeedDisplay();

scrollText();
</script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    files = [f.name for f in BASE_DIR.glob("*.md")]
    files.sort()

    current = files[0] if files else None

    if request.method == "POST":
        current = request.form.get("filename", current)

    text = "未找到文件"

    if current:
        file_path = BASE_DIR / current
        if file_path.exists():
            text = file_path.read_text(encoding="utf-8")

    return render_template_string(
        HTML_TEMPLATE,
        text=text,
        files=files,
        current=current
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)