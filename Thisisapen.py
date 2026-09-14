<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>キャッチゲーム</title>
<style>
  html,body{height:100%;margin:0;display:flex;justify-content:center;align-items:center;background:#1a1a2e;}
  canvas{background:#16213e;border-radius:8px;box-shadow:0 0 30px rgba(76,201,240,.3);}
</style>
</head>
<body>
<canvas id="game" width="400" height="600"></canvas>
<script>
const ctx = document.getElementById('game').getContext('2d');
const W = 400, H = 600;

const player = { w: 80, h: 14, x: W/2 - 40, y: H - 40, speed: 7 };
const keys = {};
let items = [], score = 0, lives = 3, gameOver = false, frame = 0;

addEventListener('keydown', e => {
  keys[e.key] = true;
  if (gameOver && (e.key === 'r' || e.key === 'R')) reset();
  if (['ArrowLeft', 'ArrowRight', ' '].includes(e.key)) e.preventDefault();
});
addEventListener('keyup', e => keys[e.key] = false);

function reset() {
  items = []; score = 0; lives = 3; gameOver = false; frame = 0;
  player.x = W/2 - player.w/2;
}

function spawn() {
  const size = 18;
  items.push({
    x: Math.random() * (W - size),
    y: -size,
    size,
    speed: 2 + Math.random() * 2 + Math.min(score * 0.05, 3)
  });
}

function update() {
  if (gameOver) return;
  frame++;
  if (frame % 40 === 0) spawn();

  // プレイヤーの移動
  if (keys['ArrowLeft'] || keys['a']) player.x -= player.speed;
  if (keys['ArrowRight'] || keys['d']) player.x += player.speed;
  player.x = Math.max(0, Math.min(W - player.w, player.x));

  // アイテムの落下と当たり判定
  for (let i = items.length - 1; i >= 0; i--) {
    const it = items[i];
    it.y += it.speed;

    const hit = it.y + it.size > player.y && it.y < player.y + player.h &&
                it.x + it.size > player.x && it.x < player.x + player.w;
    if (hit) { items.splice(i, 1); score++; continue; }

    if (it.y > H) {          // 取り逃したらライフ減少
      items.splice(i, 1);
      if (--lives <= 0) gameOver = true;
    }
  }
}

function draw() {
  ctx.clearRect(0, 0, W, H);

  // アイテム
  ctx.fillStyle = '#f9c74f';
  for (const it of items) {
    ctx.beginPath();
    ctx.arc(it.x + it.size/2, it.y + it.size/2, it.size/2, 0, Math.PI*2);
    ctx.fill();
  }

  // プレイヤー
  ctx.fillStyle = '#4cc9f0';
  ctx.fillRect(player.x, player.y, player.w, player.h);

  // UI
  ctx.fillStyle = '#fff';
  ctx.font = '20px sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText('Score: ' + score, 12, 32);
  ctx.textAlign = 'right';
  ctx.fillText('♥'.repeat(Math.max(lives, 0)), W - 12, 32);

  // ゲームオーバー画面
  if (gameOver) {
    ctx.fillStyle = 'rgba(0,0,0,0.75)';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#fff';
    ctx.textAlign = 'center';
    ctx.font = 'bold 36px sans-serif';
    ctx.fillText('GAME OVER', W/2, H/2 - 30);
    ctx.font = '20px sans-serif';
... （残り 16 行）
