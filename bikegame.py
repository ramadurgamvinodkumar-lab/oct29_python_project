
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>APEX - 3D Superbike Racing</title>

<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Arial,sans-serif;background:#05070b;color:white;overflow:hidden}
#game{position:fixed;inset:0}
canvas{display:block}
#menu{
 position:fixed;inset:0;z-index:10;
 display:flex;align-items:center;justify-content:center;
 background:linear-gradient(120deg,rgba(0,0,0,.94),rgba(5,20,30,.75));
 text-align:center
}
.panel{padding:35px;width:min(450px,92%);border:1px solid #16d9ff;
 background:rgba(5,12,20,.92);border-radius:18px;
 box-shadow:0 0 35px #00bfff33}
h1{font-size:42px;color:#13dfff;letter-spacing:5px}
.subtitle{color:#aaa;margin:12px 0 25px}
button{
 border:0;border-radius:8px;padding:13px 24px;
 background:#00cfff;color:#001018;font-weight:bold;
 cursor:pointer;margin:7px;font-size:15px
}
button:hover{background:white}
#hud{position:fixed;inset:0;pointer-events:none;display:none}
.stat{
 position:absolute;top:18px;padding:12px 17px;
 background:#07121dcc;border:1px solid #13cfff66;
 border-radius:9px;font-weight:bold
}
#speed{left:18px}
#distance{left:155px}
#level{right:18px}
#nitro{right:18px;top:80px;color:#00e5ff}
#message{
 position:absolute;top:22%;width:100%;text-align:center;
 font-size:30px;font-weight:bold;color:#00e5ff;
 text-shadow:0 0 15px #00cfff
}
#controls{
 position:absolute;bottom:20px;width:100%;
 display:flex;justify-content:space-between;padding:0 25px
}
.control{
 pointer-events:auto;width:65px;height:65px;
 border-radius:50%;background:#00bfff88;
 border:2px solid #fff;color:white;font-size:24px
}
#nitroBtn{background:#ff6b0088}
#pause{position:absolute;right:18px;bottom:25px;pointer-events:auto}
#help{position:absolute;bottom:100px;left:20px;color:#ccc;font-size:12px}
@media(max-width:600px){
 h1{font-size:32px}.stat{font-size:12px;padding:8px}
 #distance{left:105px}
}
</style>
</head>

<body>
<div id="game"></div>

<div id="menu">
 <div class="panel">
  <h1>APEX RACING</h1>
  <p class="subtitle">3D SUPERBIKE CHAMPIONSHIP</p>
  <p>Race through three extreme environments.</p>
  <p style="margin:12px;color:#00dfff">SNOW • MUD • HIGHWAY</p>
  <button onclick="startGame()">START RACE</button>
  <p style="color:#999;font-size:12px;margin-top:15px">
   W / ↑ Accelerate · A / D Steer · SPACE Nitro
  </p>
 </div>
</div>

<div id="hud">
 <div class="stat" id="speed">0 KM/H</div>
 <div class="stat" id="distance">0 M</div>
 <div class="stat" id="level">LEVEL 1</div>
 <div class="stat" id="nitro">NITRO: 100%</div>
 <div id="message"></div>

 <div id="help">Keyboard: W/↑ accelerate | A/D steer | SPACE nitro</div>

 <div id="controls">
  <div>
   <button class="control" id="left">◀</button>
   <button class="control" id="right">▶</button>
  </div>
  <div>
   <button class="control" id="nitroBtn">N</button>
   <button class="control" id="accelerate">▲</button>
  </div>
 </div>
 <button id="pause" onclick="pauseGame()">PAUSE</button>
</div>

<script type="module">
import * as THREE from
'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x91c9e8);
scene.fog = new THREE.Fog(0x91c9e8,35,180);

const camera = new THREE.PerspectiveCamera(
 65,window.innerWidth/window.innerHeight,.1,500
);
camera.position.set(0,5,10);

const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(window.innerWidth,window.innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled = true;
document.getElementById('game').appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xffffff,0x526070,2));

const sun = new THREE.DirectionalLight(0xffffff,2.2);
sun.position.set(-10,20,10);
sun.castShadow = true;
scene.add(sun);

const material = (color,metalness=0,roughness=.7) =>
 new THREE.MeshStandardMaterial({color,metalness,roughness});

const roadMat = material(0x252a30);
const lineMat = material(0xffffff);
const black = material(0x090b0e);
const metal = material(0x9ba8b4,.8,.25);

let bike, wheels=[];
let obstacles=[];
let decorations=[];
let coins=[];
let running=false, gameOver=false;
let speed=0, distance=0, nitro=100, score=0;
let playerX=0, steering=0;
let currentLevel=0;
let spawnTimer=0, coinTimer=0;
let paused=false;

const keys={left:false,right:false,accelerate:false,nitro:false};

const levels=[
 {name:'SNOW MOUNTAIN',bike:'APEX S1000',color:0x00cfff,
  ground:0xe5f2ff,sky:0x9bc9e9,road:0x59616b},
 {name:'MUD FOREST',bike:'APEX R1000',color:0xff4d19,
  ground:0x493b29,sky:0x78926a,road:0x493b30},
 {name:'HIGHWAY',bike:'APEX HYPER-X',color:0xffcf00,
  ground:0x26323b,sky:0x6b9ec5,road:0x252a30}
];

function box(parent,x,y,z,sx,sy,sz,mat){
 const mesh=new THREE.Mesh(
  new THREE.BoxGeometry(sx,sy,sz),mat
 );
 mesh.position.set(x,y,z);
 mesh.castShadow=true;
 mesh.receiveShadow=true;
 parent.add(mesh);
 return mesh;
}

function cylinder(parent,x,y,z,r1,r2,length,mat,rotation=0){
 const mesh=new THREE.Mesh(
  new THREE.CylinderGeometry(r1,r2,length,20),mat
 );
 mesh.position.set(x,y,z);
 mesh.rotation.z=rotation;
 mesh.castShadow=true;
 parent.add(mesh);
 return mesh;
}

function makeBike(color){
 const group=new THREE.Group();
 const bodyMat=material(color,.65,.25);

 // Wheels
 for(const z of [-.9,.95]){
  const wheel=new THREE.Mesh(
   new THREE.TorusGeometry(.43,.12,12,28),
   black
  );
  wheel.position.set(0,.48,z);
  group.add(wheel);
  wheels.push(wheel);

  const hub=new THREE.Mesh(
   new THREE.CylinderGeometry(.13,.13,.22,20),
   metal
  );
  hub.rotation.x=Math.PI/2;
  hub.position.set(0,.48,z);
  group.add(hub);
 }

 // Bike body
 box(group,0,1.05,0,.48,.42,1.3,bodyMat);
 box(group,0,1.32,-.18,.42,.12,.65,black);

 // Fuel tank
 const tank=new THREE.Mesh(
  new THREE.SphereGeometry(.38,20,16),bodyMat
 );
 tank.scale.set(1,.7,1.25);
 tank.position.set(0,1.45,.05);
 group.add(tank);

 // Seat and tail
 box(group,0,1.35,.72,.4,.16,.55,black);
 box(group,0,1.62,.95,.4,.22,.32,bodyMat);

 // Front fork
 for(const x of [-.16,.16]){
  cylinder(group,x,.95,-.8,.045,.045,.95,metal);
 }

 // Handlebars
 box(group,0,1.62,-.85,.95,.07,.09,metal);

 // Headlight
 const lamp=new THREE.Mesh(
  new THREE.SphereGeometry(.16,16,12),
  material(0xffffff,0,.1)
 );
 lamp.position.set(0,1.35,-.78);
 group.add(lamp);

 // Rider
 const rider= new THREE.Mesh(
  new THREE.SphereGeometry(.28,16,16),
  material(0x151a25)
 );
 rider.position.set(0,1.9,.15);
 rider.scale.set(.85,1.15,.85);
 group.add(rider);

 const helmet=new THREE.Mesh(
  new THREE.SphereGeometry(.23,18,16),
  material(0x101820,.3,.2)
 );
 helmet.position.set(0,2.25,.05);
 group.add(helmet);

 group.position.set(0,0,0);
 scene.add(group);
 return group;
}

function clearObjects(){
 for(const obj of [...obstacles,...decorations,...coins]){
  scene.remove(obj);
 }
 obstacles=[];decorations=[];coins=[];
}

let ground, road, laneLines=[];

function createWorld(){
 clearObjects();

 if(ground) scene.remove(ground);
 if(road) scene.remove(road);
 laneLines.forEach(x=>scene.remove(x));
 laneLines=[];

 const data=levels[currentLevel];
 scene.background=new THREE.Color(data.sky);
 scene.fog.color=new THREE.Color(data.sky);

 ground=new THREE.Mesh(
  new THREE.PlaneGeometry(500,500),
  material(data.ground)
 );
 ground.rotation.x=-Math.PI/2;
 ground.position.y=-.12;
 scene.add(ground);

 road=new THREE.Mesh(
  new THREE.PlaneGeometry(12,500),
  material(data.road)
 );
 road.rotation.x=-Math.PI/2;
 road.position.set(0,0,-150);
 road.receiveShadow=true;
 scene.add(road);

 for(let z=-350;z<30;z+=12){
  const line=new THREE.Mesh(
   new THREE.BoxGeometry(.12,.025,5),
   lineMat
  );
  line.position.set(0,.025,z);
  scene.add(line);
  laneLines.push(line);
 }

 // Road edges
 for(const x of [-6,6]){
  const edge=new THREE.Mesh(
   new THREE.BoxGeometry(.18,.08,500),
   material(0xffffff)
  );
  edge.position.set(x,.04,-150);
  scene.add(edge);
 }

 // Mountains / trees / highway lights
 for(let i=0;i<45;i++){
  const side=Math.random()<.5?-1:1;
  const x=side*(9+Math.random()*30);
  const z=-Math.random()*350;

  let obj;
  if(currentLevel===0){
   obj=new THREE.Mesh(
    new THREE.ConeGeometry(3+Math.random()*3,9+Math.random()*10,5),
    material(0xdce8f2)
   );
  }else if(currentLevel===1){
   obj=new THREE.Group();
   const trunk=new THREE.Mesh(
    new THREE.CylinderGeometry(.2,.35,4,8),
    material(0x51351e)
   );
   trunk.position.y=2;
   obj.add(trunk);
   const leaves=new THREE.Mesh(
    new THREE.ConeGeometry(2.1,5,8),
    material(0x174d27)
   );
   leaves.position.y=5;
   obj.add(leaves);
  }else{
   obj=new THREE.Group();
   const pole=box(obj,0,3,0,.15,6,.15,metal);
   box(obj,0,5.9,0,2,.15,.15,material(0xffd65a));
  }

  obj.position.set(x,0,z);
  scene.add(obj);
  decorations.push(obj);
 }
}

function resetBike(){
 wheels=[];
 if(bike) scene.remove(bike);
 bike=makeBike(levels[currentLevel].color);
 bike.position.set(0,0,0);
}

function makeObstacle(){
 const type=Math.random();
 let obj;

 if(type<.5){
  obj=new THREE.Mesh(
   new THREE.BoxGeometry(1.5,1.3,1.4),
   material(currentLevel===0?0xeeeeee:0x9b3b20)
  );
  obj.position.y=.65;
 }else{
  obj=new THREE.Mesh(
   new THREE.SphereGeometry(.8,12,10),
   material(0x343b44)
  );
  obj.position.y=.8;
 }

 obj.position.x=(Math.floor(Math.random()*3)-1)*3.5;
 obj.position.z=-120;
 scene.add(obj);
 obstacles.push(obj);
}

function makeCoin(){
 const coin=new THREE.Mesh(
  new THREE.TorusGeometry(.4,.12,10,24),
  material(0xffd000,.7,.2)
 );
 coin.position.set((Math.floor(Math.random()*3)-1)*3.5,1.4,-120);
 scene.add(coin);
 coins.push(coin);
}

function updateLevel(){
 const next=distance<1000?0:distance<2200?1:2;
 if(next!==currentLevel){
  currentLevel=next;
  createWorld();
  resetBike();
  document.getElementById('message').textContent=
   'LEVEL '+(currentLevel+1)+' - '+levels[currentLevel].name;
  setTimeout(()=>{
   document.getElementById('message').textContent='';
  },2500);
 }
}

function crash(){
 running=false;
 gameOver=true;
 document.getElementById('menu').style.display='flex';
 document.querySelector('#menu h1').textContent='RACE OVER';
 document.querySelector('#menu .subtitle').textContent=
  'FINAL SCORE: '+score;
 document.querySelector('#menu button').textContent='RACE AGAIN';
}

function startGame(){
 distance=0;score=0;speed=0;nitro=100;
 currentLevel=0;playerX=0;
 gameOver=false;paused=false;
 spawnTimer=0;coinTimer=0;
 clearObjects();
 createWorld();
 resetBike();
 document.getElementById('menu').style.display='none';
 document.getElementById('hud').style.display='block';
 document.getElementById('message').textContent='';
 document.getElementById('pause').textContent='PAUSE';
 running=true;
}

function pauseGame(){
 if(gameOver||!running && !paused) return;
 paused=!paused;
 if(paused){
  running=false;
  document.getElementById('pause').textContent='RESUME';
  document.getElementById('message').textContent='PAUSED';
 }else{
  running=true;
  document.getElementById('pause').textContent='PAUSE';
  document.getElementById('message').textContent='';
 }
}

function updateHUD(){
 document.getElementById('speed').textContent=
  Math.round(speed*22)+' KM/H';
 document.getElementById('distance').textContent=
  Math.floor(distance)+' M';
 document.getElementById('level').textContent=
  'LEVEL '+(currentLevel+1)+' - '+levels[currentLevel].bike;
 document.getElementById('nitro').textContent=
  'NITRO: '+Math.floor(nitro)+'%';
}

function update(dt){
 if(!running)return;

 const accelerating=keys.accelerate;
 const boosting=keys.nitro && nitro>0;

 const maxSpeed=boosting?2.4:1.5;
 if(accelerating) speed=Math.min(maxSpeed,speed+dt*.65);
 else speed=Math.max(.45,speed-dt*.25);

 if(boosting){
  nitro=Math.max(0,nitro-dt*24);
 }else{
  nitro=Math.min(100,nitro+dt*5);
 }

 if(keys.left) playerX-=dt*5;
 if(keys.right) playerX+=dt*5;
 playerX=THREE.MathUtils.clamp(playerX,-4.8,4.8);

 bike.position.x=THREE.MathUtils.lerp(bike.position.x,playerX,.15);
 bike.rotation.z=THREE.MathUtils.lerp(
  bike.rotation.z,
  keys.left?.28:keys.right?-.28:0,.12
 );

 wheels.forEach(w=>w.rotation.y-=speed*.08);

 distance+=speed*dt*30;
 score=Math.floor(distance)+coins.length*100;

 updateLevel();

 spawnTimer+=dt;
 coinTimer+=dt;

 if(spawnTimer>1.25){
  makeObstacle();
  spawnTimer=0;
 }
 if(coinTimer>2.2){
  makeCoin();
  coinTimer=0;
 }

 obstacles.forEach((obj)=>{
  obj.position.z+=speed*dt*30;
  if(obj.position.z>1 && !obj.userData.passed){
   obj.userData.passed=true;
   if(Math.abs(obj.position.x-playerX)<1.5){
    crash();
   }
  }
 });

 coins.forEach((coin)=>{
  coin.position.z+=speed*dt*30;
  coin.rotation.y+=dt*4;
  if(Math.abs(coin.position.z)<1.5 &&
     Math.abs(coin.position.x-playerX)<1.5){
   coin.position.z=1000;
   nitro=Math.min(100,nitro+15);
   score+=100;
  }
 });

 obstacles=obstacles.filter(obj=>{
  if(obj.position.z>15){
   scene.remove(obj);return false;
  }
  return true;
 });
 coins=coins.filter(obj=>{
  if(obj.position.z>15 || obj.position.z>500){
   scene.remove(obj);return false;
  }
  return true;
 });

 // Follow camera
 camera.position.x=THREE.MathUtils.lerp(
  camera.position.x,bike.position.x*.45,.04
 );
 camera.position.y=5.2;
 camera.position.z=10;
 camera.lookAt(bike.position.x*.3,1,-5);

 updateHUD();
}

const clock=new THREE.Clock();

function animate(){
 requestAnimationFrame(animate);
 const dt=Math.min(clock.getDelta(),.04);
 update(dt);
 renderer.render(scene,camera);
}
animate();

window.addEventListener('keydown',e=>{
 if(e.key==='ArrowLeft'||e.key.toLowerCase()==='a')keys.left=true;
 if(e.key==='ArrowRight'||e.key.toLowerCase()==='d')keys.right=true;
 if(e.key==='ArrowUp'||e.key.toLowerCase()==='w')keys.accelerate=true;
 if(e.code==='Space')keys.nitro=true;
});
window.addEventListener('keyup',e=>{
 if(e.key==='ArrowLeft'||e.key.toLowerCase()==='a')keys.left=false;
 if(e.key==='ArrowRight'||e.key.toLowerCase()==='d')keys.right=false;
 if(e.key==='ArrowUp'||e.key.toLowerCase()==='w')keys.accelerate=false;
 if(e.code==='Space')keys.nitro=false;
});

function holdButton(id,key){
 const el=document.getElementById(id);
 el.addEventListener('pointerdown',e=>{
  e.preventDefault();keys[key]=true;
 });
 ['pointerup','pointerleave','pointercancel'].forEach(event=>{
  el.addEventListener(event,()=>keys[key]=false);
 });
}
holdButton('left','left');
holdButton('right','right');
holdButton('accelerate','accelerate');
holdButton('nitroBtn','nitro');

window.addEventListener('resize',()=>{
 camera.aspect=window.innerWidth/window.innerHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(window.innerWidth,window.innerHeight);
});

createWorld();
resetBike();
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/health")
def health():
    return {"status": "APEX Racing is running"}

if __name__ == "__main__":
    app.run(debug=True)
