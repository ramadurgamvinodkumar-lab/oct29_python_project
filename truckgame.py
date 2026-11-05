
from flask import Flask, render_template_string, request, jsonify
import json
import os

app = Flask(__name__)

SCORE_FILE = "scores.json"

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Road Titans 3D Truck Game</title>
<script src="https://cdn.tailwindcss.com"></script>

<style>
*{box-sizing:border-box}
body{margin:0;overflow:hidden;background:#111827;color:white;font-family:Arial}
canvas{display:block}
#ui{position:absolute;inset:0;pointer-events:none}
.panel{background:#101827dd;border:1px solid #ffffff30;border-radius:12px;padding:12px}
button{pointer-events:auto;cursor:pointer;background:#f97316;padding:12px 20px;border-radius:10px;font-weight:bold}
.control{width:65px;height:65px;border-radius:50%;background:#ffffff30;border:2px solid white;font-size:22px;touch-action:none}
#screen{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:#000b;pointer-events:auto}
.hidden{display:none!important}
.bar{height:8px;background:#ffffff30;border-radius:10px;overflow:hidden;margin-top:5px}
.fill{height:100%;background:#22c55e;width:100%}
</style>
</head>

<body>

<div id="ui">

<div class="absolute top-3 left-3 panel">
<h1 class="text-2xl font-black text-orange-400">ROAD TITANS</h1>
<p id="truckName">Standard Cargo Truck</p>
<p>Level: <b id="level">1</b> / 3</p>
<p>Zone: <b id="zone">SNOW</b></p>
</div>

<div class="absolute top-3 right-3 panel text-right">
<p>Speed: <b id="speed">0</b> km/h</p>
<p>Distance: <b id="distance">0</b> m</p>
<p>Score: <b id="score">0</b></p>
<p>Fuel: <b id="fuelText">100</b>%</p>
<div class="bar w-32"><div id="fuelBar" class="fill"></div></div>
<p class="mt-2">Damage: <b id="damage">0</b>%</p>
<div class="bar w-32"><div id="damageBar" class="fill"></div></div>
</div>

<div class="absolute bottom-5 left-5 flex gap-3">
<button class="control" id="left">◀</button>
<button class="control" id="right">▶</button>
</div>

<div class="absolute bottom-5 right-5 flex gap-3">
<button class="control" id="brake">▼</button>
<button class="control" id="accelerate">▲</button>
</div>

<div class="absolute bottom-2 left-1/2 -translate-x-1/2 text-xs text-white/70">
W/↑ Accelerate | S/↓ Brake | A/← Left | D/→ Right
</div>

<div id="screen">
<div class="panel text-center max-w-sm mx-4">
<h1 id="screenTitle" class="text-4xl font-black text-orange-400">ROAD TITANS</h1>
<p id="screenText" class="my-5">Drive your truck through Snow, Mud and Highway. Complete all three levels!</p>
<button id="startButton">START GAME</button>
</div>
</div>

</div>

<script type="module">
import * as THREE from
'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x9bc9e8);
scene.fog = new THREE.Fog(0x9bc9e8,40,180);

const camera = new THREE.PerspectiveCamera(
65,innerWidth/innerHeight,0.1,500
);
camera.position.set(0,7,13);

const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(innerWidth,innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled=true;
document.body.appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xffffff,0x52606d,2));

const sun=new THREE.DirectionalLight(0xffffff,2);
sun.position.set(-10,20,10);
sun.castShadow=true;
scene.add(sun);

const material=(color)=>new THREE.MeshStandardMaterial({color});
const truck=new THREE.Group();
scene.add(truck);

function box(parent,x,y,z,w,h,d,color){
 const mesh=new THREE.Mesh(
  new THREE.BoxGeometry(w,h,d),material(color)
 );
 mesh.position.set(x,y,z);
 mesh.castShadow=true;
 mesh.receiveShadow=true;
 parent.add(mesh);
 return mesh;
}

function createTruck(level){
 truck.clear();

 const colors=[0xf97316,0x1677dd,0x8b35db];
 const body=colors[level-1];
 const trim=level===3?0x00ffff:0xffffff;

 // Cargo container
 box(truck,0,1.65,0.5,3,2.7,4.4,body);

 // Container lines
 for(let z=-1.5;z<2.6;z+=0.5){
  box(truck,0,1.65,z,3.03,2.72,0.04,trim);
 }

 // Driver cabin
 box(truck,0,1.2,3.1,2.9,2.2,1.8,body);

 // Windshield
 box(truck,0,1.8,4.02,2.3,0.8,0.06,0x66c9ef);

 // Front bumper
 box(truck,0,0.5,4.1,3.1,0.3,0.3,0x222222);

 // Headlights
 for(const x of [-1.1,1.1]){
  box(truck,x,0.8,4.1,0.4,0.3,0.1,0xffffcc);
 }

 // Wheels
 for(const x of [-1.6,1.6]){
  for(const z of [-1.2,1.5,3.2]){
   const wheel=new THREE.Mesh(
    new THREE.CylinderGeometry(0.55,0.55,0.35,24),
    material(0x111111)
   );
   wheel.rotation.z=Math.PI/2;
   wheel.position.set(x,0.55,z);
   truck.add(wheel);
  }
 }

 truck.position.set(0,0,0);
}

const ground=box(scene,0,-0.5,-70,200,1,250,0xeaf5ff);
const road=box(scene,0,0.02,-70,12,0.08,250,0x555555);

const lines=[];
for(let z=20;z>-250;z-=12){
 lines.push(box(scene,0,0.08,z,0.15,0.03,5,0xffffff));
}

// Trees and roadside scenery
const scenery=[];

function createTree(x,z){
 const tree=new THREE.Group();

 box(tree,0,1,0,0.5,2,0.5,0x68452b);

 const leaves=new THREE.Mesh(
  new THREE.ConeGeometry(1.8,4,8),
  material(0x236b37)
 );
 leaves.position.y=3.5;
 tree.add(leaves);

 tree.position.set(x,0,z);
 scene.add(tree);
 scenery.push(tree);
}

for(let z=20;z>-250;z-=12){
 createTree(-11,z);
 createTree(11,z-5);
}

// Obstacles and fuel
const objects=[];

function spawnObstacle(z){
 const obstacle=new THREE.Group();
 box(obstacle,0,0.9,0,2,1.8,2,0xc0392b);
 obstacle.position.set((Math.random()-.5)*7,0,z);
 scene.add(obstacle);
 objects.push({mesh:obstacle,type:"obstacle",passed:false});
}

function spawnFuel(z){
 const fuel=new THREE.Mesh(
  new THREE.BoxGeometry(1,1,1),
  material(0x22dd66)
 );
 fuel.position.set((Math.random()-.5)*7,1,z);
 scene.add(fuel);
 objects.push({mesh:fuel,type:"fuel",passed:false});
}

for(let z=-30;z>-230;z-=25){
 spawnObstacle(z);
 if(Math.random()>0.4)spawnFuel(z-12);
}

const state={
 running:false,
 speed:0,
 distance:0,
 score:0,
 fuel:100,
 damage:0,
 level:1,
 steer:0
};

const $=id=>document.getElementById(id);
const keys={};

window.addEventListener("keydown",e=>{
 keys[e.key.toLowerCase()]=true;
});

window.addEventListener("keyup",e=>{
 keys[e.key.toLowerCase()]=false;
});

function holdButton(id,key){
 const button=$(id);
 button.addEventListener("pointerdown",e=>{
  e.preventDefault();
  keys[key]=true;
 });
 ["pointerup","pointerleave","pointercancel"].forEach(event=>{
  button.addEventListener(event,()=>keys[key]=false);
 });
}

holdButton("left","a");
holdButton("right","d");
holdButton("accelerate","w");
holdButton("brake","s");

function updateUI(){
 $("speed").textContent=Math.round(state.speed);
 $("distance").textContent=Math.floor(state.distance);
 $("score").textContent=state.score;
 $("fuelText").textContent=Math.round(state.fuel);
 $("fuelBar").style.width=Math.max(0,state.fuel)+"%";
 $("damage").textContent=Math.round(state.damage);
 $("damageBar").style.width=state.damage+"%";
 $("level").textContent=state.level;

 $("truckName").textContent=[
  "Standard Cargo Truck",
  "Cyber Heavy Hauler",
  "Monster Freight"
 ][state.level-1];

 $("zone").textContent=
  state.distance<450?"SNOW":
  state.distance<1100?"MUD":"HIGHWAY";
}

async function saveScore(){
 try{
  await fetch("/save-score",{
   method:"POST",
   headers:{"Content-Type":"application/json"},
   body:JSON.stringify({
    score:state.score,
    distance:Math.floor(state.distance),
    level:state.level
   })
  });
 }catch(error){
  console.log("Score saving failed",error);
 }
}

function endGame(title){
 if(!state.running)return;

 state.running=false;
 $("screenTitle").textContent=title;
 $("screenText").textContent=
  `Distance: ${Math.floor(state.distance)} m | Score: ${state.score}`;

 $("startButton").textContent="PLAY AGAIN";
 $("screen").classList.remove("hidden");
 saveScore();
}

function resetGame(){
 Object.assign(state,{
  running:true,
  speed:0,
  distance:0,
  score:0,
  fuel:100,
  damage:0,
  level:1,
  steer:0
 });

 objects.forEach(obj=>{
  obj.passed=false;
  obj.mesh.visible=true;
 });

 createTruck(1);

 $("screen").classList.add("hidden");
 updateUI();
}

$("startButton").addEventListener("click",resetGame);

function changeLevel(){
 const next=
  state.distance<750?1:
  state.distance<1500?2:3;

 if(next!==state.level){
  state.level=next;
  createTruck(next);
 }
}

const clock=new THREE.Clock();

function updatePhysics(dt){
 if(!state.running)return;

 // Acceleration and braking
 if(keys.w||keys.arrowup){
  state.speed+=25*dt;
 }else{
  state.speed-=8*dt;
 }

 if(keys.s||keys.arrowdown){
  state.speed-=40*dt;
 }

 state.speed=THREE.MathUtils.clamp(state.speed,0,150);

 // Fuel
 state.fuel-=state.speed*dt*0.0018;

 // Steering
 if(keys.a||keys.arrowleft)state.steer-=3*dt;
 if(keys.d||keys.arrowright)state.steer+=3*dt;

 state.steer*=0.92;

 truck.position.x+=state.steer*state.speed*0.035*dt;
 truck.position.x=THREE.MathUtils.clamp(truck.position.x,-5,5);
 truck.rotation.z=-state.steer*0.08;

 const movement=state.speed*dt*0.09;
 state.distance+=movement;
 state.score+=Math.floor(movement);

 // Road movement
 road.position.z+=movement;
 if(road.position.z>55)road.position.z=-70;

 lines.forEach(line=>{
  line.position.z+=movement;
  if(line.position.z>25)line.position.z-=250;
 });

 // Scenery movement
 scenery.forEach(tree=>{
  tree.position.z+=movement;
  if(tree.position.z>25)tree.position.z-=250;
 });

 // Object collision and collection
 objects.forEach(obj=>{
  obj.mesh.position.z+=movement;

  if(obj.type==="fuel"){
   obj.mesh.rotation.y+=dt*2;
  }

  if(!obj.passed &&
     Math.abs(obj.mesh.position.z)<2.1 &&
     Math.abs(obj.mesh.position.x-truck.position.x)<2){

   obj.passed=true;

   if(obj.type==="fuel"){
    state.fuel=Math.min(100,state.fuel+25);
    state.score+=100;
   }else{
    state.damage+=20;
    state.speed*=0.55;
   }

   obj.mesh.visible=false;
  }

  if(obj.mesh.position.z>20){
   obj.mesh.position.z=-220-Math.random()*30;
   obj.mesh.position.x=(Math.random()-.5)*7;
   obj.mesh.visible=true;
   obj.passed=false;
  }
 });

 // Three environment zones
 if(state.distance<450){
  ground.material.color.set(0xe9f4ff);
  scene.background.set(0x9bc9e8);
 }else if(state.distance<1100){
  ground.material.color.set(0x79502c);
  scene.background.set(0x9aafba);
 }else{
  ground.material.color.set(0x444444);
  scene.background.set(0x7194a8);
 }

 changeLevel();

 if(state.distance>=2200){
  endGame("DELIVERY COMPLETE");
 }

 if(state.fuel<=0){
  state.fuel=0;
  endGame("OUT OF FUEL");
 }

 if(state.damage>=100){
  endGame("TRUCK DESTROYED");
 }

 updateUI();
}

function animate(){
 requestAnimationFrame(animate);

 const dt=Math.min(clock.getDelta(),0.05);

 updatePhysics(dt);

 camera.position.x+=(truck.position.x*0.35-camera.position.x)*0.05;
 camera.lookAt(truck.position.x,1,-5);

 renderer.render(scene,camera);
}

createTruck(1);
animate();

window.addEventListener("resize",()=>{
 camera.aspect=innerWidth/innerHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(innerWidth,innerHeight);
});
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/save-score", methods=["POST"])
def save_score():
    data = request.get_json(silent=True) or {}

    scores = []
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, "r") as file:
                scores = json.load(file)
        except (json.JSONDecodeError, OSError):
            scores = []

    scores.append({
        "score": int(data.get("score", 0)),
        "distance": int(data.get("distance", 0)),
        "level": int(data.get("level", 1))
    })

    with open(SCORE_FILE, "w") as file:
        json.dump(scores, file, indent=4)

    return jsonify({
        "message": "Score saved successfully"
    })


@app.route("/scores")
def get_scores():
    if not os.path.exists(SCORE_FILE):
        return jsonify([])

    try:
        with open(SCORE_FILE, "r") as file:
            return jsonify(json.load(file))
    except (json.JSONDecodeError, OSError):
        return jsonify([])


if __name__ == "__main__":
    app.run(debug=True, port=5000)
