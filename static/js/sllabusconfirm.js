const ctx = document.getElementById("radarChart").getContext("2d");

const radarChart = new Chart(ctx, {
  type: "radar",
  data: {
    labels: ["難易度", "スピード", "興味関心", "理解度", "課題"],
    datasets: [
      {
        label: "授業評価",
        data: [5, 2, 5, 4, 3], // 初期値。必要に応じて動的に更新可能
        backgroundColor: "rgba(255, 174, 66, 0.6)", // 塗りつぶし色
        borderColor: "#FFAE42", // 線の色
        pointBackgroundColor: "#FFAE42",
        borderWidth: 2,
      },
    ],
  },
  options: {
    responsive: true,
    scales: {
      r: {
        angleLines: {
          color: "#48A6A7",
        },
        grid: {
          color: "#48A6A7",
        },
        suggestedMin: 0,
        suggestedMax: 5,
        ticks: {
          stepSize: 1,
          backdropColor: "transparent",
          color: "#000",
        },
        pointLabels: {
          color: "#000",
          font: {
            size: 14,
          },
        },
      },
    },
    plugins: {
      legend: {
        display: false,
      },
    },
  },
});
