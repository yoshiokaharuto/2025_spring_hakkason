document.addEventListener('DOMContentLoaded', function () {
    const yearSelect = document.querySelector('select[name="year"]');
    const departmentSelect = document.querySelector('select[name="department"]');
    const infoSystemOption = departmentSelect.querySelector('option[value="1"]');
    const integratedSystemOption = departmentSelect.querySelector('option[value="2"]');

    function updateDepartmentOptions() {
        const selectedYear = yearSelect.value;

        // すべてのオプションを有効化
        infoSystemOption.disabled = false;
        integratedSystemOption.disabled = false;

        // ４年生なら value="1"とvalue="2" を無効にする
        if (selectedYear === '4') {
            infoSystemOption.disabled = true;
            integratedSystemOption.disabled = true;

            if (departmentSelect.value === '1' || departmentSelect.value === '2') {
                departmentSelect.value = '';
            }
        } else if (selectedYear === '3') {
            // ３年生なら value="1"（情報システム科）のみ無効
            infoSystemOption.disabled = true;

            if (departmentSelect.value === '1') {
                departmentSelect.value = '';
            }
        }
    }

    yearSelect.addEventListener('change', updateDepartmentOptions);
    updateDepartmentOptions();
});
