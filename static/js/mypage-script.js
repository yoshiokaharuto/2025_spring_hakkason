document.querySelectorAll(".score-box").forEach((box) => {
  const subject = box.dataset.subject;
  const score = parseInt(box.dataset.score, 10); // 分子
  const allScore = parseInt(box.dataset.allscore, 10); // 分母（追加）

  const rate = (score / allScore) * 100; // 得点率（%）

  const radius = 85;
  const circumference = 2 * Math.PI * radius;
  const dashArray = circumference;
  const offset = circumference;

  // SVGとテキストのHTMLを生成
  box.innerHTML = `
    <div class="circle-wrapper">
      <svg viewBox="0 0 200 200">
        <circle class="base" cx="100" cy="100" r="${radius}"></circle>
        <circle class="line" cx="100" cy="100" r="${radius}" 
                style="stroke-dasharray:${dashArray}; stroke-dashoffset:${offset};"></circle>
      </svg>
      <div class="content">
        <h4 class="subject">${subject.replace(/\\n/g, "<br>")}</h4>
        <p class="score">${score} / ${allScore}</p>
      </div>
    </div>
  `;

  // アニメーション処理（得点率に応じて描画）
  const line = box.querySelector("circle.line");
  setTimeout(() => {
    const newOffset = circumference - (circumference * rate) / 100;
    line.style.transition = "stroke-dashoffset 1.5s ease";
    line.style.strokeDashoffset = newOffset;
  }, 200);
});
