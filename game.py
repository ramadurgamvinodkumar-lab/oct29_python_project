@ -0,0 +1,817 @@

from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DINO RUN | Power Off Edition</title>

<style>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

:root {
    --gold: #ffbd4a;
    --orange: #ff642e;
    --glass: rgba(12, 17, 32, .76);
}

body {
    min-height: 100vh;
    overflow: hidden;
    background: #080d19;
    color: #fff;
    font-family: "Segoe UI", Arial, sans-serif;
}

.game {
    position: relative;
    width: 100%;
    height: 100vh;
    min-height: 440px;
    overflow: hidden;
    isolation: isolate;
    background:
        radial-gradient(ellipse at 70% 43%,
            #ffb653 0%, #e66b43 16%,
            #60354f 42%, #17213c 72%, #080d19 100%);
}

.stars {
    position: absolute;
    inset: 0;
    opacity: .7;
    background-image:
        radial-gradient(2px 2px at 10% 16%, white, transparent),
        radial-gradient(2px 2px at 26% 10%, white, transparent),
        radial-gradient(1px 1px at 47% 21%, white, transparent),
        radial-gradient(2px 2px at 81% 13%, white, transparent),
        radial-gradient(1px 1px at 92% 27%, white, transparent),
        radial-gradient(2px 2px at 60% 8%, white, transparent);
}

.sun {
    position: absolute;
    width: 180px;
    height: 180px;
    border-radius: 50%;
    left: 66%;
    top: 23%;
    background: #ffd68a;
    box-shadow: 0 0 70px #ff8c46, 0 0 180px #f05b38;
    opacity: .88;
}

.mountain {
    position: absolute;
    bottom: 28%;
    width: 0;
    height: 0;
    border-left: 180px solid transparent;
    border-right: 180px solid transparent;
    border-bottom: 260px solid #402c47;
    filter: drop-shadow(0 0 18px #36263f);
}

.m1 { left: 12%; transform: scale(.85); }
.m2 { left: 38%; transform: scale(1.2); border-bottom-color: #57354a; }
.m3 { right: 2%; transform: scale(1.5); border-bottom-color: #32283f; }

.mountain:after {
    content: "";
    position: absolute;
    left: -40px;
    top: 45px;
    border-left: 40px solid transparent;
    border-right: 40px solid transparent;
    border-bottom: 58px solid #a17a80;
    opacity: .35;
}

.ruins {
    position: absolute;
    left: 3%;
    bottom: 26%;
    width: 150px;
    height: 210px;
    opacity: .65;
    border: 12px solid #18242d;
    border-bottom: 0;
    transform: skewY(-5deg);
    background: repeating-linear-gradient(
        0deg, transparent 0 35px, #18242d 36px 43px);
}

.ruins:before {
    content: "";
    position: absolute;
    width: 65px;
    height: 75px;
    left: 28px;
    top: 65px;
    border: 8px solid #18242d;
    background: #301e30;
    box-shadow: 0 0 25px #ff412d;
}

.header {
    position: absolute;
    z-index: 5;
    top: 22px;
    left: 4%;
    right: 4%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 15px;
}

.logo {
    font-size: clamp(24px, 4vw, 48px);
    font-weight: 1000;
    font-style: italic;
    letter-spacing: -2px;
    color: #ffcc69;
    text-shadow: 0 4px 0 #8b3d19, 0 0 25px #ff7b35;
}

.logo small {
    display: block;
    font-size: 11px;
    letter-spacing: 4px;
    text-align: center;
    color: #fff1cf;
    text-shadow: none;
}

.hud {
    display: flex;
    gap: 10px;
    align-items: center;
}

.panel {
    background: var(--glass);
    border: 1px solid rgba(255, 198, 110, .35);
    border-radius: 15px;
    padding: 10px 17px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 30px #080d1933;
}

.panel span {
    display: block;
    color: #bdc9df;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.panel strong {
    font-size: 22px;
    color: var(--gold);
}

.pause {
    border: 1px solid var(--gold);
    border-radius: 50%;
    width: 44px;
    height: 44px;
    margin-left: 5px;
    background: #111629;
    color: var(--gold);
    cursor: pointer;
    font-size: 20px;
}

.ground {
    position: absolute;
    bottom: 0;
    height: 27%;
    width: 100%;
    background:
        linear-gradient(180deg, #334332 0%, #182a28 8%,
        #101b21 28%, #080d19 100%);
    border-top: 5px solid #b6a66a;
    box-shadow: 0 -10px 30px #ffb64b30;
}

.ground:before {
    content: "";
    position: absolute;
    inset: 0;
    opacity: .6;
    background: repeating-linear-gradient(
        110deg, transparent 0 65px, #b9a87533 66px 69px);
}

.ground:after {
    content: "";
    position: absolute;
    top: 18px;
    width: 200%;
    height: 10px;
    background: repeating-linear-gradient(
        90deg, #c7b17a 0 4px, transparent 4px 85px);
    animation: groundMove .55s linear infinite;
}

@keyframes groundMove {
    to { transform: translateX(-85px); }
}

#world {
    position: absolute;
    z-index: 2;
    inset: 0;
    width: 100%;
    height: 100%;
}

.center-message {
    position: absolute;
    z-index: 6;
    top: 39%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: min(90%, 480px);
    text-align: center;
    padding: 26px;
    background: rgba(8, 13, 25, .78);
    border: 1px solid #ffbc6755;
    border-radius: 24px;
    backdrop-filter: blur(14px);
    box-shadow: 0 0 55px #ff9d3020;
}

.center-message h1 {
    font-size: clamp(25px, 4vw, 43px);
    color: var(--gold);
    text-shadow: 0 0 24px #ff783d66;
}

.center-message p {
    color: #d0d9e9;
    line-height: 1.8;
    margin: 8px 0 18px;
    font-size: 14px;
}

.main-button {
    padding: 13px 29px;
    border: 0;
    border-radius: 9px;
    color: #1a1220;
    font-size: 14px;
    font-weight: 900;
    letter-spacing: 2px;
    cursor: pointer;
    background: linear-gradient(110deg, #ffd57c, #ff853e);
    box-shadow: 0 0 28px #ff813d55;
    transition: transform .2s;
}

.main-button:hover { transform: scale(1.05); }

.instructions {
    position: absolute;
    z-index: 4;
    bottom: 8%;
    left: 50%;
    transform: translateX(-50%);
    padding: 12px 20px;
    border: 1px solid #ffffff22;
    border-radius: 12px;
    background: #080d19b8;
    color: #dce3f0;
    text-align: center;
    font-size: 12px;
    white-space: nowrap;
}

.instructions b { color: var(--gold); }

.footer {
    position: absolute;
    bottom: 15px;
    right: 25px;
    color: #c3c8d4;
    font-size: 11px;
    z-index: 4;
}

.hidden { display: none !important; }

@media(max-width: 700px) {
    .header {
        top: 12px;
        left: 12px;
        right: 12px;
        align-items: flex-start;
        flex-direction: column;
    }

    .logo { font-size: 27px; }
    .logo small { text-align: left; font-size: 8px; }
    .hud { gap: 6px; }
    .panel { padding: 7px 10px; }
    .panel strong { font-size: 17px; }
    .panel span { font-size: 8px; letter-spacing: 1px; }
    .pause { width: 37px; height: 37px; }
    .sun { width: 100px; height: 100px; top: 30%; }
    .instructions { bottom: 5%; font-size: 10px; }
    .footer { display: none; }
}
</style>
</head>

<body>
<div class="game" id="game">
    <div class="stars"></div>
    <div class="sun"></div>
    <div class="mountain m1"></div>
    <div class="mountain m2"></div>
    <div class="mountain m3"></div>
    <div class="ruins"></div>

    <header class="header">
        <div class="logo">
            DINO RUN
            <small>POWER OFF EDITION</small>
        </div>

        <div class="hud">
            <div class="panel">
                <span>Score</span>
                <strong id="score">00000</strong>
            </div>
            <div class="panel">
                <span>Best</span>
                <strong id="best">00000</strong>
            </div>
            <div class="panel">
                <span>Coins</span>
                <strong id="coins">0</strong>
            </div>
            <button class="pause" id="pause" aria-label="Pause">Ⅱ</button>
        </div>
    </header>

    <canvas id="world"></canvas>
    <div class="ground"></div>

    <div class="center-message" id="overlay">
        <h1 id="messageTitle">THE WORLD WENT DARK</h1>
        <p id="messageText">
            No internet. No electricity. No problem.<br>
            Become the last survivor of the prehistoric world.
        </p>
        <button class="main-button" id="start">START RUN</button>
    </div>

    <div class="instructions">
        <b>SPACE / ↑</b> JUMP &nbsp; • &nbsp;
        <b>↓</b> DUCK &nbsp; • &nbsp;
        COLLECT COINS &nbsp; • &nbsp; AVOID OBSTACLES
    </div>

    <div class="footer">FLASK × PYTHON &nbsp; | &nbsp; OFFLINE RUNNER</div>
</div>

<script>
const canvas = document.getElementById("world");
const ctx = canvas.getContext("2d");

const $ = id => document.getElementById(id);

let W = 0, H = 0, groundY = 0;
let running = false, paused = false, started = false;
let score = 0, coins = 0, speed = 6, frame = 0;
let obstacles = [], pickups = [], particles = [];
let lastTime = 0, spawnTimer = 0, pickupTimer = 0;
let best = Number(localStorage.getItem("dinoBest") || 0);

const dino = {
    x: 100, y: 0, vy: 0,
    w: 52, h: 56,
    duck: false, grounded: true
};

$("best").textContent = String(best).padStart(5, "0");

function resize() {
    const rect = canvas.getBoundingClientRect();
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = rect.width;
    H = rect.height;
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    groundY = H * .73;
    if (dino.grounded) dino.y = groundY - dino.h;
}

window.addEventListener("resize", resize);
resize();

function roundedRect(x, y, w, h, r, color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.roundRect(x, y, w, h, r);
    ctx.fill();
}

function drawDino() {
    const x = dino.x;
    const y = dino.y;
    const h = dino.duck ? 31 : dino.h;
    const w = dino.w;

    ctx.save();
    ctx.shadowColor = "#ffb94f";
    ctx.shadowBlur = 18;

    // Tail
    ctx.fillStyle = "#c67a38";
    ctx.beginPath();
    ctx.moveTo(x + 8, y + h * .65);
    ctx.lineTo(x - 22, y + h * .8);
    ctx.lineTo(x + 7, y + h * .88);
    ctx.fill();

    // Body
    roundedRect(x + 4, y + h * .34, w * .66, h * .55, 9, "#b96b32");

    // Back spikes
    ctx.fillStyle = "#e4a34c";
    for (let i = 0; i < 4; i++) {
        ctx.beginPath();
        ctx.moveTo(x + 13 + i * 8, y + h * .34);
        ctx.lineTo(x + 17 + i * 8, y + h * .15);
        ctx.lineTo(x + 22 + i * 8, y + h * .34);
        ctx.fill();
    }

    // Head and snout
    roundedRect(x + 23, y + 2, 29, 23, 7, "#df9a4d");
    roundedRect(x + 35, y + 15, 22, 12, 4, "#d5843a");

    // Eye
    ctx.shadowBlur = 0;
    ctx.fillStyle = "#fff0bc";
    ctx.beginPath();
    ctx.arc(x + 42, y + 10, 5, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#16121a";
    ctx.beginPath();
    ctx.arc(x + 43, y + 10, 2, 0, Math.PI * 2);
    ctx.fill();

    // Teeth
    ctx.fillStyle = "#fff3ce";
    ctx.fillRect(x + 47, y + 23, 3, 4);
    ctx.fillRect(x + 53, y + 23, 3, 4);

    // Animated legs
    ctx.fillStyle = "#c67a38";
    const step = running && dino.grounded ? Math.sin(frame * .3) * 6 : 0;
    roundedRect(x + 13, y + h * .78, 10, 15 + step, 3, "#c67a38");
    roundedRect(x + 35, y + h * .78, 10, 15 - step, 3, "#c67a38");

    ctx.restore();
}

function drawObstacle(o) {
    ctx.save();
    ctx.shadowColor = o.type === "cactus" ? "#8dff82" : "#ff6a43";
    ctx.shadowBlur = 12;

    if (o.type === "cactus") {
        roundedRect(o.x + 12, o.y + 5, 18, o.h - 5, 6, "#467f53");
        roundedRect(o.x, o.y + 23, 14, 20, 5, "#5e9d60");
        roundedRect(o.x + 29, o.y + 15, 13, 25, 5, "#5e9d60");

        ctx.fillStyle = "#c6e9a0";
        for (let i = 0; i < 5; i++) {
            ctx.fillRect(o.x + 17, o.y + 12 + i * 9, 2, 4);
        }
    } else {
        ctx.fillStyle = "#5d5966";
        ctx.beginPath();
        ctx.moveTo(o.x, o.y + o.h);
        ctx.lineTo(o.x + 5, o.y + 12);
        ctx.lineTo(o.x + 18, o.y);
        ctx.lineTo(o.x + o.w, o.y + 9);
        ctx.lineTo(o.x + o.w + 5, o.y + o.h);
        ctx.closePath();
        ctx.fill();

        ctx.strokeStyle = "#a59ba0";
        ctx.lineWidth = 2;
        ctx.stroke();
    }
    ctx.restore();
}

function drawCoin(p) {
    ctx.save();
    ctx.shadowColor = "#ffca47";
    ctx.shadowBlur = 18;
    ctx.fillStyle = "#ffc94d";
    ctx.beginPath();
    ctx.ellipse(p.x, p.y, 9, 12, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#fff1a4";
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.fillStyle = "#8b541b";
    ctx.font = "bold 12px Arial";
    ctx.textAlign = "center";
    ctx.fillText("$", p.x, p.y + 4);
    ctx.restore();
}

function burst(x, y, color) {
    for (let i = 0; i < 9; i++) {
        particles.push({
            x, y,
            vx: (Math.random() - .5) * 6,
            vy: (Math.random() - .7) * 6,
            life: 30,
            color
        });
    }
}

function drawParticles() {
    particles.forEach(p => {
        ctx.globalAlpha = p.life / 30;
        ctx.fillStyle = p.color;
        ctx.fillRect(p.x, p.y, 4, 4);
        p.x += p.vx;
        p.y += p.vy;
        p.life--;
    });
    ctx.globalAlpha = 1;
    particles = particles.filter(p => p.life > 0);
}

function spawnObstacle() {
    const type = Math.random() > .43 ? "cactus" : "rock";
    const h = type === "cactus" ? 43 + Math.random() * 15 : 28;
    const w = type === "cactus" ? 42 : 40;

    obstacles.push({
        x: W + 20,
        y: groundY - h,
        w, h, type,
        passed: false
    });
}

function spawnCoins() {
    const baseY = groundY - 90 - Math.random() * 45;
    for (let i = 0; i < 4; i++) {
        pickups.push({
            x: W + 30 + i * 34,
            y: baseY - Math.sin(i / 3 * Math.PI) * 20,
            taken: false
        });
    }
}

function intersects(a, b) {
    return a.x + a.w > b.x + 5 &&
           a.x + 5 < b.x + b.w &&
           a.y + a.h > b.y + 5 &&
           a.y < b.y + b.h;
}

function update(dt) {
    const step = dt / 16.67;
    frame += step;
    score += .12 * step * (speed / 6);
    speed = Math.min(13, 6 + score / 140);

    dino.vy += .62 * step;
    dino.y += dino.vy * step;

    if (dino.y + dino.h >= groundY) {
        dino.y = groundY - dino.h;
        dino.vy = 0;
        dino.grounded = true;
    }

    spawnTimer -= dt;
    pickupTimer -= dt;

    if (spawnTimer <= 0) {
        spawnObstacle();
        spawnTimer = Math.max(650, 1450 - speed * 48) +
                     Math.random() * 650;
    }

    if (pickupTimer <= 0) {
        spawnCoins();
        pickupTimer = 2200 + Math.random() * 1300;
    }

    obstacles.forEach(o => {
        o.x -= speed * step;
        if (!o.passed && o.x + o.w < dino.x) {
            o.passed = true;
            score += 5;
        }
    });

    pickups.forEach(p => {
        p.x -= speed * step;
        const dx = p.x - (dino.x + dino.w / 2);
        const dy = p.y - (dino.y + dino.h / 2);

        if (!p.taken && Math.hypot(dx, dy) < 34) {
            p.taken = true;
            coins++;
            score += 10;
            burst(p.x, p.y, "#ffca47");
        }
    });

    const hitbox = {
        x: dino.x + 8,
        y: dino.y + 7,
        w: dino.w - 12,
        h: dino.h - 9
    };

    for (const o of obstacles) {
        if (intersects(hitbox, o)) {
            endGame();
            return;
        }
    }

    obstacles = obstacles.filter(o => o.x > -80);
    pickups = pickups.filter(p => p.x > -30 && !p.taken);

    $("score").textContent = String(Math.floor(score)).padStart(5, "0");
    $("coins").textContent = coins;
}

function render() {
    ctx.clearRect(0, 0, W, H);

    // Glowing atmospheric haze
    const glow = ctx.createRadialGradient(
        W * .68, H * .47, 10, W * .68, H * .47, W * .48
    );
    glow.addColorStop(0, "#ffb34a17");
    glow.addColorStop(1, "#ffb34a00");
    ctx.fillStyle = glow;
    ctx.fillRect(0, 0, W, H);

    pickups.forEach(drawCoin);
    obstacles.forEach(drawObstacle);
    drawDino();
    drawParticles();
}

function loop(time) {
    const dt = Math.min(time - (lastTime || time), 35);
    lastTime = time;

    if (running && !paused) update(dt);
    render();
    requestAnimationFrame(loop);
}

function startGame() {
    score = 0;
    coins = 0;
    speed = 6;
    frame = 0;
    spawnTimer = 800;
    pickupTimer = 1400;
    obstacles = [];
    pickups = [];
    particles = [];

    dino.duck = false;
    dino.grounded = true;
    dino.vy = 0;
    dino.y = groundY - dino.h;

    running = true;
    paused = false;
    started = true;

    $("overlay").classList.add("hidden");
    $("pause").textContent = "Ⅱ";
}

function endGame() {
    running = false;

    const finalScore = Math.floor(score);
    if (finalScore > best) {
        best = finalScore;
        localStorage.setItem("dinoBest", best);
    }

    $("best").textContent = String(best).padStart(5, "0");
    $("messageTitle").textContent = "EXTINCTION EVENT!";
    $("messageText").innerHTML =
        "Your score: <b style='color:#ffbd4a'>" + finalScore +
        "</b> &nbsp; | &nbsp; Coins: <b style='color:#ffbd4a'>" +
        coins + "</b><br>Every legend deserves another run.";

    $("start").textContent = "PLAY AGAIN";
    $("overlay").classList.remove("hidden");
}

function jump() {
    if (!running || paused) return;

    if (dino.grounded) {
        dino.vy = -13.5;
        dino.grounded = false;
        burst(dino.x + 15, groundY - 4, "#e6b36c");
    }
}

window.addEventListener("keydown", e => {
    if (["Space", "ArrowUp", "ArrowDown"].includes(e.code)) {
        e.preventDefault();
    }

    if (e.repeat) return;

    if (e.code === "Space" || e.code === "ArrowUp") {
        if (!started || !running) {
            startGame();
        } else {
            jump();
        }
    }

    if (e.code === "ArrowDown" && running && !paused) {
        dino.duck = true;
    }

    if (e.code === "Escape" && running) {
        togglePause();
    }
});

window.addEventListener("keyup", e => {
    if (e.code === "ArrowDown") dino.duck = false;
});

canvas.addEventListener("pointerdown", () => {
    if (!started || !running) startGame();
    else jump();
});

$("start").addEventListener("click", startGame);

function togglePause() {
    if (!running) return;
    paused = !paused;
    $("pause").textContent = paused ? "▶" : "Ⅱ";

    if (paused) {
        $("messageTitle").textContent = "TIME STANDS STILL";
        $("messageText").textContent =
            "Take a breath. The prehistoric world is waiting.";
        $("start").textContent = "RESUME RUN";
        $("overlay").classList.remove("hidden");
    } else {
        $("overlay").classList.add("hidden");
    }
}

$("pause").addEventListener("click", () => {
    if (!started) return;
    togglePause();
});

requestAnimationFrame(loop);
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)# oct29_python_project
