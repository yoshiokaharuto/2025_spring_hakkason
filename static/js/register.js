document.addEventListener('DOMContentLoaded', function () {
    const yearSelect = document.querySelector('select[name="year"]');
    const departmentSelect = document.querySelector('select[name="department"]');
    const infoSystemOption = departmentSelect.querySelector('option[value="1"]');

    function updateDepartmentOptions() {
        const selectedYear = yearSelect.value;
        if (selectedYear === '3' || selectedYear === '4') {
            infoSystemOption.disabled = true;
            if (departmentSelect.value === '1') {
                departmentSelect.value = ''; 
            }
        } else {
            infoSystemOption.disabled = false;
        }
    }

    yearSelect.addEventListener('change', updateDepartmentOptions);
    updateDepartmentOptions();
});
