document.addEventListener('DOMContentLoaded', () => {
    const courseSelect = document.getElementById('course');
    const professorSelect = document.getElementById('professor');
    if (options.length > 0) {
        const filterCourses = (selectedProfessor) => {
            courseSelect.innerHTML = '';
            options.forEach((opt) => {
                if (opt.professor === selectedProfessor) {
                    const option = document.createElement('option');
                    option.value = opt.id;
                    option.textContent = opt.name;
                    option.dataset.professor = opt.professor;
                    courseSelect.append(option);
                }
            });
            // this basically like gives a default n/a option if the professor doesn't have any assigned classes
            if (courseSelect.options.length === 0) {
                const option = document.createElement('option');
                option.text = 'No Courses';
                option.value = 'N/A';
                option.disabled = true;
                option.selected = true;
                courseSelect.append(option);
            }
        }
        filterCourses(professorSelect.value);
        professorSelect.addEventListener('change', () => {
            filterCourses(professorSelect.value);
        });
    }
});