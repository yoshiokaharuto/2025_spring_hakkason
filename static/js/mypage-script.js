document.querySelectorAll(".score-box").forEach((box) => {
  const subject = box.dataset.subject;
  const score = parseInt(box.dataset.score, 10);
  const allScore = parseInt(box.dataset.allscore, 10);

  const rate = (score / allScore) * 100;

  const radius = 85;
  const circumference = 2 * Math.PI * radius;
  const dashArray = circumference;
  const offset = circumference;

  // SVGとテキストのHTMLを生成（exceed-line 追加）
  box.innerHTML = `
    <div class="circle-wrapper">
      <svg viewBox="0 0 200 200">
        <circle class="base" cx="100" cy="100" r="${radius}"></circle>
        <circle class="line" cx="100" cy="100" r="${radius}" 
                style="stroke-dasharray:${dashArray}; stroke-dashoffset:${offset};"></circle>
        <circle class="exceed-line" cx="100" cy="100" r="${radius}" 
                style="stroke-dasharray:${dashArray}; stroke-dashoffset:${offset}; display: none;"></circle>
      </svg>
      <div class="content">
        <h4 class="subject">${subject.replace(/\\n/g, "<br>")}</h4>
        <p class="score">${score} / ${allScore}</p>
      </div>
    </div>
  `;

  const line = box.querySelector("circle.line");
  const exceedLine = box.querySelector("circle.exceed-line");

  setTimeout(() => {
    // 通常の円グラフ
    const normalRate = Math.min(rate, 100);
    const newOffset = circumference - (circumference * normalRate) / 100;
    line.style.transition = "stroke-dashoffset 1.5s ease";
    line.style.strokeDashoffset = newOffset;

    // 100%を超えた場合の追加円
    if (rate > 100) {
      const exceedRate = rate - 100;
      const exceedOffset = circumference - (circumference * exceedRate) / 100;
      exceedLine.style.display = "block";
      exceedLine.style.transition = "stroke-dashoffset 3s ease 3.5s"; // 少し遅らせて出現
      exceedLine.style.strokeDashoffset = exceedOffset;
    }
  }, 200);
});
