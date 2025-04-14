const leftTable = document.getElementById("leftTable");
const rightTable = document.getElementById("rightTable");

// データを交互に分ける
dictSubject.forEach((item, index) => {
  const koma = item.credit / 2;
  const name = item.subject_name;
  const attendance = item.attendance;
  const attendanceRate = Math.round(((koma - attendance) / koma) * 100);
  const row = document.createElement("tr");

  row.innerHTML = `
      <td>${name}</td>
      <td>${koma}コマ</td>
      <td>${attendance}コマ</td>
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
