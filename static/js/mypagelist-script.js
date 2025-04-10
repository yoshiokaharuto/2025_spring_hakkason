// 出席データ
const data = [
  { subject: "システム設計論1", koma: 160, absent: 0 },
  { subject: "システム設計論2", koma: 160, absent: 1 },
  { subject: "システム設計論3", koma: 160, absent: 1 },
  { subject: "システム設計論4", koma: 160, absent: 2 },
  { subject: "システム設計論5", koma: 160, absent: 0 },
  { subject: "システム設計論6", koma: 160, absent: 1 },
  { subject: "システム設計論7", koma: 160, absent: 0 },
  { subject: "システム設計論8", koma: 160, absent: 2 },
  { subject: "システム設計論9", koma: 160, absent: 0 }, // ←ここまでで奇数件
];

const leftTable = document.getElementById("leftTable");
const rightTable = document.getElementById("rightTable");

// データを交互に分ける
data.forEach((item, index) => {
  const row = document.createElement("tr");
  const attendanceRate = Math.round(
    ((item.koma - item.absent) / item.koma) * 100
  );

  row.innerHTML = `
      <td>${item.subject}</td>
      <td>${item.koma}コマ</td>
      <td>${item.absent}コマ</td>
      <td>${attendanceRate}%</td>
    `;

  if (index % 2 === 0) {
    leftTable.appendChild(row);
  } else {
    rightTable.appendChild(row);
  }
});

// データ数が奇数なら、右側に空行追加
if (data.length % 2 !== 0) {
  const emptyRow = document.createElement("tr");
  emptyRow.innerHTML = `
      <td colspan="4" style="height: 53px;"></td>
    `;
  rightTable.appendChild(emptyRow);
}
