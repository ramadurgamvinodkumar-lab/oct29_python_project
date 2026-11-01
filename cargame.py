@ -0,0 +1,1074 @@
from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>APEX RUSH 3D | Supercar Racing</title>

<style>
*{margin:0;padding:0;box-sizing:border-box}
body{
    background:#050912;color:white;
    font-family:Arial,Helvetica,sans-serif;
    overflow:hidden
}
#game{position:fixed;inset:0}
canvas{display:block;width:100%;height:100%}

.topbar{
    position:absolute;top:18px;left:3%;right:3%;
    display:flex;justify-content:space-between;
    align-items:center;z-index:5;pointer-events:none
}
.logo{
    font-size:30px;font-weight:1000;font-style:italic;
    letter-spacing:3px;color:#fff;
    text-shadow:0 0 20px #00c8ff
}
.logo small{display:block;font-size:10px;letter-spacing:6px;color:#91cce9}
.hud{display:flex;gap:9px;flex-wrap:wrap;justify-content:flex-end}
.hudbox{
    background:#091421d9;border:1px solid #ffffff35;
    padding:10px 16px;border-radius:10px;
    min-width:95px;backdrop-filter:blur(12px)
}
.hudbox span{
    display:block;color:#8faabe;font-size:9px;
    letter-spacing:2px;margin-bottom:5px
}
.hudbox strong{font-size:20px;color:#fff}
#speed{color:#00eaff}
#nitroBar{
    width:100%;height:5px;background:#263644;
    margin-top:6px;border-radius:5px;overflow:hidden
}
#nitroFill{height:100%;width:100%;background:#00eaff}

.level-label{
    position:absolute;top:110px;left:3%;
    font-size:12px;letter-spacing:3px;color:#d4e5f1;
    text-shadow:0 2px 8px #000;z-index:4
}
.level-label b{color:#00eaff;font-size:17px}

.bottom-help{
    position:absolute;bottom:18px;left:50%;
    transform:translateX(-50%);
    background:#07121cdd;border:1px solid #ffffff30;
    padding:12px 20px;border-radius:12px;
    color:#b8d0df;font-size:11px;
    letter-spacing:1px;z-index:4;
    white-space:nowrap
}
.bottom-help b{color:#00eaff}

.overlay{
    position:absolute;inset:0;z-index:10;
    display:flex;justify-content:center;align-items:center;
    background:linear-gradient(120deg,#030710dd,#07182bdc);
    backdrop-filter:blur(7px);
    padding:20px
}
.modal{
    width:min(650px,100%);
    text-align:center;
    background:linear-gradient(145deg,#132335ee,#070d19f5);
    border:1px solid #5b839d77;
    border-radius:22px;padding:35px;
    box-shadow:0 0 90px #00aaff22
}
.eyebrow{
    color:#00d9ff;font-size:11px;
    letter-spacing:5px;font-weight:bold
}
.modal h1{
    font-size:clamp(38px,7vw,72px);
    font-weight:1000;font-style:italic;
    margin:12px 0;color:white;
    text-shadow:0 0 30px #00bfff55
}
.modal p{color:#a8bacb;line-height:1.8;font-size:14px}
.mainbtn{
    border:0;padding:16px 35px;margin-top:23px;
    background:linear-gradient(100deg,#00d9ff,#167aff);
    color:#00101c;font-weight:1000;letter-spacing:3px;
    border-radius:7px;cursor:pointer;
    transition:.2s;font-size:14px
}
.mainbtn:hover{transform:scale(1.06);box-shadow:0 0 30px #00cfff88}
.level-cards{
    display:grid;grid-template-columns:repeat(3,1fr);
    gap:9px;margin-top:24px;text-align:left
}
.level-card{
    border:1px solid #ffffff25;background:#ffffff08;
    border-radius:10px;padding:12px
}
.level-card strong{display:block;font-size:12px;color:#fff}
.level-card small{color:#8faabe;font-size:10px}
.hidden{display:none!important}
#pauseBtn{
    position:absolute;right:3%;top:120px;z-index:5;
    border:1px solid #ffffff55;color:white;
    background:#071421bb;padding:10px 17px;
    border-radius:8px;cursor:pointer
}
#toast{
    position:absolute;top:44%;left:50%;
    transform:translate(-50%,-50%);
    font-size:clamp(22px,4vw,44px);
    font-weight:1000;font-style:italic;
    color:#fff;text-shadow:0 0 30px #00cfff;
    z-index:6;text-align:center;pointer-events:none
}
#touchControls{
    position:absolute;bottom:75px;left:0;right:0;
    display:none;justify-content:space-between;
    padding:0 20px;z-index:6;pointer-events:none
}
.touchgroup{display:flex;gap:10px}
.touchbtn{
    width:57px;height:57px;border-radius:50%;
    background:#061728cc;border:1px solid #00d9ff88;
    color:#fff;font-size:22px;pointer-events:auto;
    touch-action:none
}
@media(max-width:700px){
    .topbar{align-items:flex-start}
    .logo{font-size:20px}
    .hudbox{padding:7px;min-width:65px}
    .hudbox strong{font-size:14px}
    .hudbox span{font-size:7px}
    .level-label{top:95px;font-size:9px}
    #pauseBtn{top:145px}
    .bottom-help{font-size:8px;padding:10px}
    .modal{padding:23px}
    .level-cards{grid-template-columns:1fr}
    #touchControls{display:flex}
}
</style>
</head>

<body>
<div id="game">

    <div class="topbar">
        <div class="logo">
            APEX RUSH
            <small>ULTIMATE SUPERCAR EXPERIENCE</small>
        </div>

        <div class="hud">
            <div class="hudbox">
                <span>SPEED KM/H</span>
                <strong id="speed">000</strong>
            </div>
            <div class="hudbox">
                <span>DISTANCE</span>
                <strong id="distance">0 m</strong>
            </div>
            <div class="hudbox">
                <span>COINS</span>
                <strong id="coins">0</strong>
            </div>
            <div class="hudbox">
                <span>NITRO</span>
                <strong id="nitroText">100%</strong>
                <div id="nitroBar"><div id="nitroFill"></div></div>
            </div>
        </div>
    </div>

    <div class="level-label">
        CURRENT RACE<br>
        <b id="levelName">01 / SNOW MOUNTAIN</b>
    </div>

    <button id="pauseBtn" onclick="togglePause()">Ⅱ PAUSE</button>
    <div id="toast"></div>

    <div id="touchControls">
        <div class="touchgroup">
            <button class="touchbtn" data-control="left">◀</button>
            <button class="touchbtn" data-control="right">▶</button>
        </div>
        <div class="touchgroup">
            <button class="touchbtn" data-control="brake">▼</button>
            <button class="touchbtn" data-control="nitro">⚡</button>
        </div>
    </div>

    <div class="bottom-help">
        <b>W / ↑</b> ACCELERATE &nbsp;
        <b>S / ↓</b> BRAKE &nbsp;
        <b>A / D</b> STEER &nbsp;
        <b>SHIFT</b> NITRO
    </div>

    <div class="overlay" id="overlay">
        <div class="modal">
            <div class="eyebrow">THREE WORLDS. THREE MACHINES. ONE CHAMPION.</div>
            <h1 id="modalTitle">APEX RUSH</h1>
            <p id="modalText">
                Experience extreme supercar racing.<br>
                Conquer the snow, survive the mud and dominate the highway.
            </p>

            <div class="level-cards">
                <div class="level-card">
                    <strong>01 · SNOW</strong>
                    <small>APEX GT · STARTER</small>
                </div>
                <div class="level-card">
                    <strong>02 · MUD</strong>
                    <small>APEX R · UPGRADED</small>
                </div>
                <div class="level-card">
                    <strong>03 · HIGHWAY</strong>
                    <small>APEX X · ULTIMATE</small>
                </div>
            </div>

            <button class="mainbtn" id="startBtn" onclick="startGame()">START ENGINE</button>
        </div>
    </div>
</div>

<script type="module">
import * as THREE from
'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';

/* ---------------- BASIC THREE.JS SETUP ---------------- */

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x9eb9ce);
scene.fog = new THREE.Fog(0x9eb9ce, 45, 180);

const camera = new THREE.PerspectiveCamera(
    65, window.innerWidth/window.innerHeight, 0.1, 500
);
camera.position.set(0, 5.5, 11);

const renderer = new THREE.WebGLRenderer({
    antialias:true,
    powerPreference:"high-performance"
});
renderer.setSize(window.innerWidth,window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio,1.7));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
document.getElementById("game").prepend(renderer.domElement);

const hemi = new THREE.HemisphereLight(0xd9edff,0x303c45,2);
scene.add(hemi);

const sun = new THREE.DirectionalLight(0xffffff,3);
sun.position.set(-15,25,10);
sun.castShadow = true;
sun.shadow.mapSize.set(1024,1024);
scene.add(sun);

/* ---------------- MATERIALS ---------------- */

const mat = (color,roughness=.5,metalness=.1) =>
    new THREE.MeshStandardMaterial({color,roughness,metalness});

const materials = {
    road:mat(0x30353b,.9),
    line:mat(0xffffff,.5),
    snow:mat(0xe9f5ff,.8),
    mud:mat(0x59402d,.95),
    grass:mat(0x233b2a,1),
    building:mat(0x27394b,.8),
    glass:new THREE.MeshPhysicalMaterial({
        color:0x142b42,metalness:.7,roughness:.12,
        transparent:true,opacity:.88
    }),
    rubber:mat(0x090b0e,.95),
    chrome:mat(0xbcc9d2,.2,.9),
    light:new THREE.MeshBasicMaterial({color:0x9eeaff}),
    redLight:new THREE.MeshBasicMaterial({color:0xff182a})
};

/* ---------------- ENVIRONMENT ---------------- */

let worldObjects=[];
let laneLines=[];
let environmentItems=[];
let environmentGroup=new THREE.Group();
scene.add(environmentGroup);

const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(500,500),
    materials.snow
);
ground.rotation.x=-Math.PI/2;
ground.position.y=-.14;
scene.add(ground);

const road = new THREE.Mesh(
    new THREE.PlaneGeometry(15,350),
    materials.road
);
road.rotation.x=-Math.PI/2;
road.position.set(0,-.1,-100);
scene.add(road);

function box(parent,x,y,z,w,h,d,material){
    const mesh=new THREE.Mesh(
        new THREE.BoxGeometry(w,h,d),material
    );
    mesh.position.set(x,y,z);
    mesh.castShadow=true;
    mesh.receiveShadow=true;
    parent.add(mesh);
    return mesh;
}

function makeCone(parent,x,y,z,r,h,material){
    const mesh=new THREE.Mesh(
        new THREE.ConeGeometry(r,h,8),material
    );
    mesh.position.set(x,y,z);
    mesh.castShadow=true;
    parent.add(mesh);
    return mesh;
}

function makeTree(x,z){
    const group=new THREE.Group();
    const trunk= new THREE.Mesh(
        new THREE.CylinderGeometry(.22,.35,2,8),
        mat(0x493323)
    );
    trunk.position.y=1;
    group.add(trunk);

    for(let i=0;i<3;i++){
        makeCone(group,0,2.1+i*.8,0,1.3-i*.2,2,
            currentLevel===0?mat(0xd9efff):mat(0x174c31));
    }

    group.position.set(x,0,z);
    environmentGroup.add(group);
    environmentItems.push(group);
}

function makeMountain(x,z,size){
    const mountain=new THREE.Mesh(
        new THREE.ConeGeometry(size, size*2.2, 6),
        mat(currentLevel===0?0x728ca3:0x344a43)
    );
    mountain.position.set(x,size*.9,z);
    mountain.rotation.y=Math.random()*2;
    environmentGroup.add(mountain);
    environmentItems.push(mountain);
}

function makeBuilding(x,z){
    const h=12+Math.random()*35;
    const b=box(environmentGroup,x,h/2,z,
        7+Math.random()*7,h,8+Math.random()*5,
        materials.building);
    environmentItems.push(b);

    const windows=box(environmentGroup,x,h/2,z-4,
        5,h*.8,.04,mat(0x456d86,.3,.4));
}

function clearEnvironment(){
    while(environmentGroup.children.length){
        const item=environmentGroup.children[0];
        environmentGroup.remove(item);
        item.traverse?.(obj=>{
            if(obj.geometry)obj.geometry.dispose();
        });
    }
    environmentItems=[];
    laneLines.forEach(o=>scene.remove(o));
    laneLines=[];
    worldObjects.forEach(o=>scene.remove(o));
    worldObjects=[];
}

let currentLevel=0;

function setupEnvironment(level){
    currentLevel=level;
    clearEnvironment();

    const configs=[
        {sky:0x9bbbd2,fog:0xb9d0df,ground:0xe9f5ff,road:0x65737c},
        {sky:0x647c68,fog:0x657c65,ground:0x493a2b,road:0x493b30},
        {sky:0x080f26,fog:0x111b33,ground:0x101722,road:0x242a33}
    ];

    const c=configs[level];
    scene.background=new THREE.Color(c.sky);
    scene.fog=new THREE.Fog(c.fog,35,170);
    ground.material=mat(c.ground,.95);
    road.material=mat(c.road,.9);

    // Highway lane markings
    for(let z=-180;z<30;z+=12){
        for(let x of [-2.5,2.5]){
            const line=new THREE.Mesh(
                new THREE.BoxGeometry(.13,.035,5),
                mat(level===2?0xffd77a:0xffffff)
            );
            line.position.set(x,-.035,z);
            scene.add(line);
            laneLines.push(line);
        }
    }

    // Road edge rails
    for(let x of [-7.6,7.6]){
        const rail=box(scene,x,.35,-80,.25,.7,210,
            mat(level===0?0xc5d6e2:level===1?0x65472e:0x8a9aa8));
        worldObjects.push(rail);
    }

    // Side environment
    for(let i=0;i<32;i++){
        const z=-190+i*7;
        if(level===2){
            makeBuilding(-14-Math.random()*5,z);
            makeBuilding(14+Math.random()*5,z-3);
        }else{
            makeTree(-12-Math.random()*6,z);
            makeTree(12+Math.random()*6,z-2);
        }
    }

    for(let i=0;i<8;i++){
        makeMountain(-35+i*10,-100-Math.random()*30,8+Math.random()*10);
    }

    if(level===2){
        // Decorative highway lights
        for(let z=-170;z<20;z+=25){
            for(let x of [-9,9]){
                const pole=box(environmentGroup,x,3,z,.18,6,.18,
                    mat(0x8998a8));
                const lamp= new THREE.Mesh(
                    new THREE.SphereGeometry(.4,8,8),
                    new THREE.MeshBasicMaterial({color:0x00bfff})
                );
                lamp.position.set(x,6,z);
                environmentGroup.add(lamp);
            }
        }
        sun.color.set(0x5d9cff);
        sun.intensity=1.3;
    }else{
        sun.color.set(0xffffff);
        sun.intensity=3;
    }
}

/* ---------------- PROCEDURAL SUPERCAR MODELS ---------------- */

const carSpecs=[
    {name:"APEX GT",color:0x06a9e8,top:180,accel:20,nitro:1},
    {name:"APEX R",color:0xe63a23,top:240,accel:27,nitro:1.2},
    {name:"APEX X",color:0x8d6bff,top:330,accel:36,nitro:1.5}
];

let playerCar;
let wheels=[];
let carBodyMaterial;

function createCar(level){
    const group=new THREE.Group();
    const spec=carSpecs[level];

    carBodyMaterial= new THREE.MeshPhysicalMaterial({
        color:spec.color,
        metalness:.78,
        roughness:.2,
        clearcoat:1,
        clearcoatRoughness:.1
    });

    // Main aerodynamic body
    box(group,0,.62,0,2.15,.48,4.3,carBodyMaterial);

    // Front nose
    const hood=box(group,0,.83,-1.35,1.9,.25,1.5,carBodyMaterial);
    hood.rotation.x=-.08;

    // Rear engine cover
    box(group,0,.85,1.15,1.85,.27,1.1,carBodyMaterial);

    // Cabin
    const cabin=new THREE.Mesh(
        new THREE.BoxGeometry(1.48,.75,1.85),
        materials.glass
    );
    cabin.position.set(0,1.22,.05);
    group.add(cabin);

    // Roof
    box(group,0,1.63,.05,1.42,.12,1.55,carBodyMaterial);

    // Windshield
    const windshield=box(group,0,1.27,-.76,1.42,.52,.08,
        materials.glass);
    windshield.rotation.x=-.32;

    // Rear glass
    const rearGlass=box(group,0,1.25,.85,1.35,.42,.08,
        materials.glass);
    rearGlass.rotation.x=.32;

    // Front bumper
    box(group,0,.48,-2.12,2.05,.24,.2,mat(0x11161d,.4,.6));

    // Rear diffuser
    box(group,0,.4,2.12,1.85,.25,.3,mat(0x10141a,.5,.5));

    // Headlights
    for(let x of [-.73,.73]){
        const light=box(group,x,.78,-2.17,.45,.12,.06,materials.light);
        const tail=box(group,x,.76,2.18,.43,.12,.06,materials.redLight);
    }

    // Side mirrors
    for(let x of [-1.12,1.12]){
        box(group,x,1.03,-.65,.25,.12,.35,carBodyMaterial);
    }

    // Rear spoiler
    box(group,0,1.35,1.9,2.15,.09,.32,carBodyMaterial);
    box(group,0,1.18,1.9,.12,.3,.12,materials.chrome);

    // Front splitter
    box(group,0,.32,-2.2,2.3,.08,.45,mat(0x15191d));

    // Wheels with rotating cylinder geometry
    wheels=[];
    for(let x of [-1.08,1.08]){
        for(let z of [-1.38,1.38]){
            const wheel=new THREE.Group();
            wheel.position.set(x,.46,z);

            const tire=new THREE.Mesh(
                new THREE.CylinderGeometry(.43,.43,.28,24),
                materials.rubber
            );
            tire.rotation.z=Math.PI/2;
            wheel.add(tire);

            const rim=new THREE.Mesh(
                new THREE.CylinderGeometry(.25,.25,.30,12),
                materials.chrome
            );
            rim.rotation.z=Math.PI/2;
            wheel.add(rim);

            const hub=new THREE.Mesh(
                new THREE.CylinderGeometry(.09,.09,.32,12),
                mat(0x27313a,.3,.9)
            );
            hub.rotation.z=Math.PI/2;
            wheel.add(hub);

            group.add(wheel);
            wheels.push(wheel);
        }
    }

    // Level 3 special neon trim
    if(level===2){
        const neon=box(group,0,.51,0,2.2,.035,3.5,
            new THREE.MeshBasicMaterial({color:0x8b5cff}));
        neon.material.transparent=true;
        neon.material.opacity=.9;
    }

    group.position.set(0,0,4);
    group.scale.setScalar(1);
    group.traverse(obj=>{
        if(obj.isMesh)obj.castShadow=true;
    });

    return group;
}

function replaceCar(level){
    if(playerCar){
        scene.remove(playerCar);
    }
    playerCar=createCar(level);
    scene.add(playerCar);
}

/* ---------------- OBSTACLES AND COINS ---------------- */

let obstacles=[];
let pickups=[];
let obstacleTimer=0;
let pickupTimer=0;

function spawnObstacle(){
    const group=new THREE.Group();
    const type=Math.random();

    let material;
    if(currentLevel===0)material=mat(0xd7e9f3);
    else if(currentLevel===1)material=mat(0x68452c);
    else material=mat(0xd7e1ee,.4,.5);

    if(type<.5){
        const rock=new THREE.Mesh(
            new THREE.DodecahedronGeometry(1,1),material
        );
        rock.scale.set(1.1,.7,1.1);
        rock.position.y=.65;
        group.add(rock);
    }else{
        box(group,0,.65,0,1.8,1.3,1.6,material);
        box(group,0,1.35,0,1.2,.15,1.2,mat(0x30353b));
    }

    const lane=[-4.5,0,4.5][Math.floor(Math.random()*3)];
    group.position.set(lane,0,-100);
    scene.add(group);

    obstacles.push({group,lane});
}

function spawnPickup(){
    const group=new THREE.Group();
    const coin=new THREE.Mesh(
        new THREE.TorusGeometry(.45,.13,10,20),
        new THREE.MeshStandardMaterial({
            color:0xffd044,metalness:.8,roughness:.2,
            emissive:0x775000
        })
    );
    group.add(coin);
    group.position.set([-4.5,0,4.5][Math.floor(Math.random()*3)],
        1.4,-95);
    scene.add(group);
    pickups.push({group,coin});
}

/* ---------------- GAME STATE ---------------- */

let state="menu";
let currentDistance=0;
let coins=0;
let speed=0;
let nitro=100;
let steering=0;
let gameTime=0;
let score=0;
let best=Number(localStorage.getItem("apexBest")||0);

const roadLimit=5.6;
const levelDistance=850;

const controls={
    left:false,right:false,accelerate:false,
    brake:false,nitro:false
};

function updateHUD(){
    document.getElementById("speed").textContent=
        String(Math.round(speed*1.25)).padStart(3,"0");

    document.getElementById("distance").textContent=
        Math.floor(currentDistance)+" m";

    document.getElementById("coins").textContent=coins;

    document.getElementById("nitroText").textContent=
        Math.round(nitro)+"%";

    document.getElementById("nitroFill").style.width=nitro+"%";
}

function clearRaceObjects(){
    obstacles.forEach(o=>scene.remove(o.group));
    pickups.forEach(o=>scene.remove(o.group));
    obstacles=[];
    pickups=[];
}

function resetRace(){
    currentDistance=0;
    coins=0;
    score=0;
    speed=0;
    nitro=100;
    gameTime=0;
    steering=0;
    obstacleTimer=1;
    pickupTimer=3;

    clearRaceObjects();

    playerCar.position.set(0,0,4);
    playerCar.rotation.set(0,0,0);

    updateHUD();
}

function showOverlay(title,text,button){
    document.getElementById("modalTitle").textContent=title;
    document.getElementById("modalText").innerHTML=text;
    document.getElementById("startBtn").textContent=button;
    document.getElementById("overlay").classList.remove("hidden");
}

function hideOverlay(){
    document.getElementById("overlay").classList.add("hidden");
}

function setLevel(level){
    currentLevel=level;
    setupEnvironment(level);
    replaceCar(level);

    const names=[
        "01 / SNOW MOUNTAIN",
        "02 / MUD ADVENTURE",
        "03 / HIGHWAY EXTREME"
    ];

    document.getElementById("levelName").textContent=names[level];
    resetRace();
}

window.startGame=function(){
    if(state==="levelcomplete"){
        if(currentLevel<2){
            setLevel(currentLevel+1);
        }
    }else if(state==="gameover"||state==="won"){
        setLevel(0);
    }

    state="running";
    hideOverlay();
    document.getElementById("toast").textContent="";
    document.getElementById("pauseBtn").textContent="Ⅱ PAUSE";
};

window.togglePause=function(){
    if(state==="running"){
        state="paused";
        showOverlay("RACE PAUSED","Your supercar is waiting. Get ready to race again.","RESUME RACE");
        document.getElementById("startBtn").onclick=()=>{
            state="running";
            hideOverlay();
            document.getElementById("startBtn").onclick=startGame;
        };
    }else if(state==="paused"){
        state="running";
        hideOverlay();
    }
};

/* ---------------- COLLISION ---------------- */

function crash(){
    state="gameover";
    speed=0;

    if(score>best){
        best=score;
        localStorage.setItem("apexBest",best);
    }

    showOverlay(
        "RACE OVER",
        "Your car has been damaged.<br>Distance: "+
        Math.floor(currentDistance)+" m<br>Score: "+score+
        "<br>Best score: "+best,
        "RESTART RACE"
    );
}

function levelComplete(){
    state="levelcomplete";
    speed=0;

    const next=currentLevel+1;
    if(next<3){
        showOverlay(
            "LEVEL COMPLETE",
            "Outstanding driving!<br>"+
            carSpecs[currentLevel].name+
            " has conquered this track.<br>"+
            "Your next supercar: <b style='color:#00eaff'>"+
            carSpecs[next].name+"</b><br>"+
            "Get ready for the next environment.",
            "UNLOCK NEXT CAR"
        );
    }else{
        state="won";
        showOverlay(
            "APEX CHAMPION",
            "You conquered all three worlds!<br>"+
            "Final score: "+score+
            "<br>Coins collected: "+coins,
            "RACE AGAIN"
        );
    }
}

/* ---------------- MOVEMENT AND GAMEPLAY ---------------- */

function updateGame(dt){
    if(state!=="running")return;

    gameTime+=dt;

    const spec=carSpecs[currentLevel];
    const maxSpeed=spec.top/1.25;

    if(controls.accelerate){
        speed=Math.min(maxSpeed,speed+spec.accel*dt);
    }else{
        speed=Math.max(0,speed-7*dt);
    }

    if(controls.brake){
        speed=Math.max(0,speed-35*dt);
    }

    if(controls.nitro && nitro>0 && speed>10){
        speed=Math.min(maxSpeed*1.25,speed+35*dt);
        nitro=Math.max(0,nitro-27*dt);
    }else{
        nitro=Math.min(100,nitro+5*dt);
    }

    const steeringSpeed=5.5;
    if(controls.left)steering-=steeringSpeed*dt;
    if(controls.right)steering+=steeringSpeed*dt;

    steering=Math.max(-roadLimit,Math.min(roadLimit,steering));
    playerCar.position.x=THREE.MathUtils.damp(
        playerCar.position.x,steering,8,dt
    );

    const move=speed*dt*.65;

    currentDistance+=move;
    score=Math.floor(currentDistance+coins*50);

    // Rotate wheels
    wheels.forEach(w=>w.rotation.x-=move*1.8);

    // Car steering tilt
    playerCar.rotation.z=THREE.MathUtils.damp(
        playerCar.rotation.z,
        controls.left?.10:controls.right?-.10:0,
        7,dt
    );

    // Move road lines and side scenery
    laneLines.forEach(line=>{
        line.position.z+=move;
        if(line.position.z>12)line.position.z-=192;
    });

    environmentItems.forEach(item=>{
        item.position.z+=move;
        if(item.position.z>25)item.position.z-=230;
    });

    obstacleTimer-=dt;
    pickupTimer-=dt;

    if(obstacleTimer<=0 && speed>12){
        spawnObstacle();
        obstacleTimer=Math.max(.65,2.1-speed/140)+Math.random()*.5;
    }

    if(pickupTimer<=0){
        spawnPickup();
        pickupTimer=3+Math.random()*2;
    }

    // Obstacles move toward the car
    for(let i=obstacles.length-1;i>=0;i--){
        const o=obstacles[i];
        o.group.position.z+=move;

        if(Math.abs(o.group.position.z-4)<1.5 &&
           Math.abs(o.group.position.x-playerCar.position.x)<1.6){
            crash();
            return;
        }

        if(o.group.position.z>18){
            scene.remove(o.group);
            obstacles.splice(i,1);
        }
    }

    // Collect coins
    for(let i=pickups.length-1;i>=0;i--){
        const p=pickups[i];
        p.group.position.z+=move;
        p.coin.rotation.y+=dt*3;

        if(Math.abs(p.group.position.z-4)<2 &&
           Math.abs(p.group.position.x-playerCar.position.x)<1.5){
            coins++;
            scene.remove(p.group);
            pickups.splice(i,1);
            continue;
        }

        if(p.group.position.z>18){
            scene.remove(p.group);
            pickups.splice(i,1);
        }
    }

    // Off-road penalty
    if(Math.abs(playerCar.position.x)>5){
        speed=Math.max(0,speed-12*dt);
    }

    // Level progression
    if(currentDistance>=levelDistance){
        levelComplete();
        return;
    }

    updateHUD();
}

/* ---------------- CAMERA ---------------- */

const desiredCamera=new THREE.Vector3();

function updateCamera(dt){
    if(!playerCar)return;

    desiredCamera.set(
        playerCar.position.x*.28,
        5.2,
        11
    );

    camera.position.lerp(
        desiredCamera,1-Math.exp(-3*dt)
    );

    camera.lookAt(
        playerCar.position.x*.18,1,-10
    );
}

/* ---------------- KEYBOARD CONTROLS ---------------- */

window.addEventListener("keydown",e=>{
    const key=e.key.toLowerCase();

    if(["arrowup","arrowdown","arrowleft","arrowright"," "].includes(key)){
        e.preventDefault();
    }

    if(key==="w"||key==="arrowup")controls.accelerate=true;
    if(key==="s"||key==="arrowdown")controls.brake=true;
    if(key==="a"||key==="arrowleft")controls.left=true;
    if(key==="d"||key==="arrowright")controls.right=true;
    if(key==="shift")controls.nitro=true;
    if(key==="escape")togglePause();
});

window.addEventListener("keyup",e=>{
    const key=e.key.toLowerCase();

    if(key==="w"||key==="arrowup")controls.accelerate=false;
    if(key==="s"||key==="arrowdown")controls.brake=false;
    if(key==="a"||key==="arrowleft")controls.left=false;
    if(key==="d"||key==="arrowright")controls.right=false;
    if(key==="shift")controls.nitro=false;
});

document.querySelectorAll(".touchbtn").forEach(btn=>{
    const control=btn.dataset.control;

    btn.addEventListener("pointerdown",e=>{
        e.preventDefault();
        controls[control]=true;
        btn.setPointerCapture(e.pointerId);
    });

    const release=()=>{
        controls[control]=false;
    };

    btn.addEventListener("pointerup",release);
    btn.addEventListener("pointercancel",release);
    btn.addEventListener("lostpointercapture",release);
});

/* ---------------- RENDER LOOP ---------------- */

let lastTime=performance.now();

function animate(now){
    requestAnimationFrame(animate);

    const dt=Math.min((now-lastTime)/1000,.04);
    lastTime=now;

    updateGame(dt);
    updateCamera(dt);

    // Small camera vibration at high speed
    if(state==="running" && speed>80){
        camera.position.y+=Math.sin(now*.035)*.008;
    }

    renderer.render(scene,camera);
}

window.addEventListener("resize",()=>{
    camera.aspect=window.innerWidth/window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth,window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio,1.7));
});

/* ---------------- INITIALIZATION ---------------- */

setLevel(0);
requestAnimationFrame(animate);

</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(PAGE)

@app.route("/health")
def health():
    return {"status": "online", "game": "APEX RUSH 3D"}

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
